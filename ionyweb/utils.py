# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType

from ionyweb.decorators import singleton
from ionyweb.page.models import Page
from ionyweb.page.sitemap import PagesSitemap


def get_sitemaps():
    sitemaps = {'pages': PagesSitemap}
    for page in Page.objects.all():
        app_sitemap = page.app_page_object.get_sitemap()
        if app_sitemap:
            sitemaps[page.slug] = app_sitemap
    return sitemaps

#
def coerce_put_post(request):
    """
    Django doesn't particularly understand REST.
    In case we send data over PUT, Django won't
    actually look at the data and load it. We need
    to twist its arm here.
    
    The try/except abominiation here is due to a bug
    in mod_python. This should fix it.
    """
    if request.method == "PUT":
        # Bug fix: if _load_post_and_files has already been called, for
        # example by middleware accessing request.POST, the below code to
        # pretend the request is a POST instead of a PUT will be too late
        # to make a difference. Also calling _load_post_and_files will result 
        # in the following exception:
        #   AttributeError: You cannot set the upload handlers after the upload has been processed.
        # The fix is to check for the presence of the _post field which is set 
        # the first time _load_post_and_files is called (both by wsgi.py and 
        # modpython.py). If it's set, the request has to be 'reset' to redo
        # the query value parsing in POST mode.
        if hasattr(request, '_post'):
            del request._post
            del request._files
        
        try:
            request.method = "POST"
            request._load_post_and_files()
            request.method = "PUT"
        except AttributeError:
            request.META['REQUEST_METHOD'] = 'POST'
            request._load_post_and_files()
            request.META['REQUEST_METHOD'] = 'PUT'
            
        request.PUT = request.POST

#
def coerce_delete_post(request):
    """
    Django doesn't particularly understand REST.
    In case we send data over DELETE, Django won't
    actually look at the data and load it. We need
    to twist its arm here.
    
    The try/except abominiation here is due to a bug
    in mod_python. This should fix it.
    """
    if request.method == "DELETE":
        # Bug fix: if _load_post_and_files has already been called, for
        # example by middleware accessing request.POST, the below code to
        # pretend the request is a POST instead of a PUT will be too late
        # to make a difference. Also calling _load_post_and_files will result 
        # in the following exception:
        #   AttributeError: You cannot set the upload handlers after the upload has been processed.
        # The fix is to check for the presence of the _post field which is set 
        # the first time _load_post_and_files is called (both by wsgi.py and 
        # modpython.py). If it's set, the request has to be 'reset' to redo
        # the query value parsing in POST mode.
        if hasattr(request, '_post'):
            del request._post
            del request._files
        
        try:
            request.method = "POST"
            request._load_post_and_files()
            request.method = "DELETE"
        except AttributeError:
            request.META['REQUEST_METHOD'] = 'POST'
            request._load_post_and_files()
            request.META['REQUEST_METHOD'] = 'DELETE'
            
        request.DELETE = request.POST



@singleton
class ContentTypeAccessor(object):

    def __init__(self):
        self._CT_MODELS = {}
        self._CT_NAMED_MODELS = {}
        self._CT_PK_MODELS = {}

    def _set_ct(self, ct):
        self._CT_MODELS[ct.model_class()] = ct
        self._CT_NAMED_MODELS[(ct.app_label, ct.model)] = ct
        self._CT_PK_MODELS[ct.pk] = ct

    def get_for_model(self, model):
        if model not in self._CT_MODELS:
            tmp_ct = ContentType.objects.get_for_model(model)
            self._set_ct(tmp_ct)
        return self._CT_MODELS[model]
    
    def get_for_names(self, app_name, model_name):
        if (app_name, model_name) not in self._CT_NAMED_MODELS:
            tmp_ct = ContentType.objects.get(app_label=app_name, model=model_name)
            self._set_ct(tmp_ct)
        return self._CT_NAMED_MODELS[(app_name, model_name)]

    def get_for_pk(self, pk):
        if int(pk) not in self._CT_PK_MODELS:
            tmp_ct = ContentType.objects.get(pk=pk)
            self._set_ct(tmp_ct)
        return self._CT_PK_MODELS[int(pk)]

    @property
    def page(self):
        return self.get_for_names('page', 'page')

    @property
    def website(self):
        return self.get_for_names('website', 'website')


def generate_plugins_list():
    """
        Return list of content based on
    """
    return ()