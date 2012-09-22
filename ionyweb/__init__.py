# -*- coding: utf-8 -*-
import sys
import os

VERSION = (0, 1, 0, 'beta', 0)
VERSION_INFO = '.'.join([str(i) for i in VERSION]).strip('0.')

def get_ionyweb_path():
    """
        Return full patt of ionyweb
    """
    fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
    template_dir = os.path.dirname(__file__)
    return template_dir.decode(fs_encoding)

