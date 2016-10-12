from django.shortcuts import redirect

from ct_anonymizer.settings import PRODUCTION
from pb_oauth.xmlrpc_oauth import BscwApi


class AuthorizationMiddleware(object):

    # Check if client IP is allowed
    def process_request(self, request):

        # except authorization pages
        if request.path == '/team-ideation-platform/authorize/':
            return None

        # exclude api views
        if '/api/' in request.path:
            return None

        # save information about the persona that has to be sent
        if 'send_persona' in request.GET:
            request.session['send_persona'] = request.GET.get('send_persona')
            if 'delete' in request.GET:
                request.session['delete_persona'] = True
            if 'next' in request.GET:
                request.session['next_page'] = request.GET.get('next')

        # save information about current project, campaign & return point
        if 'pid' in request.GET:
            request.session['project_id'] = request.GET.get('pid')
        if 'cid' in request.GET:
            request.session['campaign_id'] = request.GET.get('cid')
        if 'back_url' in request.GET:
            request.session['dashboard_url'] = request.GET.get('back_url')

        # make sure user has already authorized the app through customer platform
        if ('bswc_token' not in request.session) or ('send_persona' in request.GET):
            return redirect(BscwApi.authorization_url())

        return None
