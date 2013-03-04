"""CAS authentication middleware"""

from urllib import urlencode

from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse

from django_cas.views import login as cas_login, logout as cas_logout, _service_url, _redirect_url

__all__ = ['CASMiddleware']

class CASMiddleware(object):
    """Middleware that allows CAS authentication on admin pages"""

    def process_request(self, request):
        """Logs in the user if a ticket is append as parameter"""

        ticket = request.REQUEST.get('ticket')

        if ticket:
            from django.contrib import auth
            user = auth.authenticate(ticket=ticket, service=_service_url(request), redirect_to=_redirect_url(request))
            if user is not None:
                auth.login(request, user)




    def process_view(self, request, view_func, view_args, view_kwargs):
        """Forwards unauthenticated requests to the admin page to the CAS
        login URL, as well as calls to django.contrib.auth.views.login and
        logout.
        """

        def is_admin_authentication(viewf, function_name):
            """
            The previous code here did not work with current admin functionality
            so we're matching in an admittedly nonpythonic way against the admin
            login/logout paths. Update to this function quite welcome!
            """
            return viewf.__module__.startswith('django.contrib.admin.sites') and viewf.__name__ is function_name

        if is_admin_authentication(view_func, 'login'):
            return cas_login(request, *view_args, **view_kwargs)
        elif is_admin_authentication(view_func, 'logout'):
            return cas_logout(request, *view_args, **view_kwargs)

        if settings.CAS_ADMIN_PREFIX:
            if not request.path.startswith(settings.CAS_ADMIN_PREFIX):
                return None
        elif not view_func.__module__.startswith('django.contrib.admin.'):
            return None

        if request.user.is_authenticated():
            if request.user.is_staff:
                return None
            else:
                error = ('<h1>Forbidden</h1><p>You do not have staff '
                         'privileges.</p>')
                return HttpResponseForbidden(error)
        params = urlencode({REDIRECT_FIELD_NAME: request.get_full_path()})
        return HttpResponseRedirect(reverse(cas_login) + '?' + params)
