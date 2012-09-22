# -*- coding: utf-8 -*-
"Views of the authentication module"


from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, TemplateView

import hashlib

#
def auto_auth_js(request):
    "If there is a sessionid cookie, set it on, if not 404 error"
    if 'sessionid' in request.COOKIES and request.user.is_authenticated():
        return render_to_response('administration/authentication/log.js',
                                  {'cookie': request.COOKIES['sessionid']},
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden("<h1>Access Forbidden - Please log-in</h1>")

def crossdomain_login(request):
        return render_to_response('administration/authentication/crossdomain_login.html',
                                  context_instance=RequestContext(request))
    
