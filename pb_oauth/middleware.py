from django.shortcuts import redirect, render

from ct_anonymizer.settings import PRODUCTION
from pb_oauth.xmlrpc_oauth import BscwApi


class AuthorizationMiddleware(object):

    # Check if client IP is allowed
    def process_request(self, request):

        # save information about current project, campaign & return point
        if 'pid' in request.GET:
            request.session['project_id'] = request.GET.get('pid')
        if 'cid' in request.GET:
            request.session['campaign_id'] = request.GET.get('cid')
        if 'back_url' in request.GET:
            request.session['dashboard_url'] = request.GET.get('back_url')

        # exclude authorization pages
        if request.path == '/team-ideation-tools/authorize/':
            return None

        # exclude api views
        if '/api/' in request.path:
            return None

        # make sure user has already authorized the app through customer platform
        if ('bswc_token' not in request.session) \
                or (request.path == '/team-ideation-tools/propagate/' and 'send_persona' in request.GET) \
                or (request.path == '/team-ideation-tools/propagate/' and 'delete_persona' in request.GET):

            # save information about the persona that has to be sent
            if 'send_persona' in request.GET:
                redirect_to = '/team-ideation-tools/perform-pending-action/?send_persona=%s' % \
                              request.GET.get('delete_persona')
                if 'next' in request.GET:
                    redirect_to += '&next=%s' % request.GET.get('next')
            elif 'delete_persona' in request.GET:
                redirect_to = '/team-ideation-tools/perform-pending-action/?delete_persona=%s' % \
                              request.GET.get('delete_persona')
                if 'next' in request.GET:
                    redirect_to += '&next=%s' % request.GET.get('next')
            else:
                redirect_to = request.get_full_path()

            return redirect(BscwApi.authorization_url(redirect_to=redirect_to))

        return None
