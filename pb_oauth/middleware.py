from django.shortcuts import redirect

from pb_oauth.xmlrpc_oauth import BscwApi


class AuthorizationMiddleware(object):

    # Check if client IP is allowed
    def process_request(self, request):
        # except authorization pages
        if request.path == '/persona-builder/authorize/':
            return None

        # make sure user has already authorized the app through customer platform
        if 'bswc_token' not in request.session:
            return redirect(BscwApi.authorization_url())

        return None
