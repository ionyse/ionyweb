# -*- coding: utf-8 -*-

# Python imports
import os.path
from tempfile import NamedTemporaryFile

# Django imports
from django.conf import settings
from django.core.files.storage import DefaultStorage
from django.core.files import File

# PIL import
try:
    from PIL import Image
except ImportError:
    import Image

storage = DefaultStorage()
storage.location = settings.MEDIA_ROOT
storage.base_url = settings.MEDIA_URL


def path_strip(path, root):
    if not path or not root:
        return path
    path = os.path.normcase(path)
    root = os.path.normcase(root)
    if path.startswith(root):
        return path[len(root):]
    return path

def get_version_path(value, version_prefix, root):
    """
    Construct the PATH to an Image version.
    value has to be a path relative to the location of 
    the site's storage.
    
    version_filename = filename + version_prefix + ext
    Returns a relative path to the location of the site's storage.
    
    >>> get_version_path('website/<slug/storage/file.jpg', 'croppedthumbnail', 'website/slug/storage/')
    website/<slug/storage/file_croppedthumbnail.jpg
    """
    

    if value.startswith(root) and storage.exists(value):
        path, filename = os.path.split(value)
        filename, ext = os.path.splitext(filename)
        version_filename = filename + "_" + version_prefix + ext
        return os.path.join(root, version_filename)
    else:
        return None

def version_generator(value, version_prefix, root, force=None):
    """
    Generate Version for an Image.
    value has to be a serverpath relative to MEDIA_ROOT.
    """
    
    # PIL's Error "Suspension not allowed here" work around:
    # s. http://mail.python.org/pipermail/image-sig/1999-August/000816.html
    try:
        from PIL import ImageFile
    except ImportError:
        import ImageFile
    ImageFile.MAXBLOCK = settings.IMAGE_MAXBLOCK # default is 64k


    if storage.exists(value):
        tmpfile = File(NamedTemporaryFile())
        try:
            orig_file = storage.open(value)
            im = Image.open(orig_file)
            version_path = get_version_path(value, version_prefix, root)
            path, version_basename = os.path.split(version_path)
            root, ext = os.path.splitext(version_basename)
            version = scale_and_crop(im, settings.VERSIONS[version_prefix]['width'], 
                                     settings.VERSIONS[version_prefix]['height'], 
                                     settings.VERSIONS[version_prefix]['opts'])
            if not version:
                version = im
            if 'methods' in settings.VERSIONS[version_prefix].keys():
                for method in settings.VERSIONS[version_prefix]['methods']:
                    if callable(method):
                        version = method(version)
            try:
                version.save(tmpfile, format=Image.EXTENSION[ext], 
                             quality=settings.VERSION_QUALITY, 
                             optimize=(os.path.splitext(version_path)[1].lower() != '.gif'))
            except IOError:
                version.save(tmpfile, format=Image.EXTENSION[ext], quality=settings.VERSION_QUALITY)
            # Remove the old version, if there's any
            if version_path != storage.get_available_name(version_path):
                storage.delete(version_path)
            storage.save(version_path, tmpfile)
            return version_path
        except:
            raise
        finally:
            tmpfile.close()
            try:
                orig_file.close()
            except:
                pass
    return None

def get_path_or_create(value, version_prefix, root, force=None):
    """
        Return path of thumbnail based on version_prefix
        If file does not exist, version generate one
    """
    thumb = get_version_path(value, version_prefix, root)
    if not storage.exists(thumb):
        version_generator(value, version_prefix, root, force)
    return thumb

def scale_and_crop(im, width, height, opts):
    """
    Scale and Crop.
    """
    
    x, y   = [float(v) for v in im.size]
    
    if 'upscale' not in opts and x < width:
        # version would be bigger than original
        # no need to create this version, because "upscale" isn't defined.
        return False
    
    if width:
        xr = float(width)
    else:
        xr = float(x*height/y)
    if height:
        yr = float(height)
    else:
        yr = float(y*width/x)
    
    if 'crop' in opts:
        r = max(xr/x, yr/y)
    else:
        r = min(xr/x, yr/y)
    
    if r < 1.0 or (r > 1.0 and 'upscale' in opts):
        im = im.resize((int(x*r), int(y*r)), resample=Image.ANTIALIAS)
    
    if 'crop' in opts:
        x, y   = [float(v) for v in im.size]
        ex, ey = (x-min(x, xr))/2, (y-min(y, yr))/2
        if ex or ey:
            im = im.crop((int(ex), int(ey), int(x-ex), int(y-ey)))
    return im
    
scale_and_crop.valid_options = ('crop', 'upscale')
