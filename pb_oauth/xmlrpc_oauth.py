import os
import base64
import urllib
import urllib2

from django.shortcuts import render, redirect
from oauth_credentials import consumer_keys, consumer_secrets, servers
from xmlrpc_srv import XMLRPC_Server

bscw_oauth_args = {
    'op':'OAuth'
}
DEFAULT_HOST = 'cloudteams.epu.ntua.gr:8000'


def log(*val):
    import dump
    dump.line(*val)


def dump(val):
    import dump, os
    dump_file = os.environ.get('DUMP_FILE', '')
    os.environ['DUMP_FILE'] = ''
    dump.dump(val)
    os.environ['DUMP_FILE'] = dump_file


def toUTF8(s):
    if isinstance(s, unicode):
        return s.encode('utf-8')
    else:
        return str(s)


def quote(s):
    import urllib
    return urllib.quote(s, safe='~')


def quote_args(args):
    key_values = [(quote(toUTF8(k)), quote(toUTF8(v))) \
        for k,v in args.items()]
    key_values.sort()
    return '&'.join(['%s=%s' % (k, v) for k, v in key_values])


def signature_base_string(method, url, args):
    xargs = args.copy()
    try:
        del args['oauth_signature']
    except:
        pass
    xargs = quote_args(xargs)
    return '&'.join((method.upper(), quote(url), quote(xargs)))


def make_url(url, args={}):
    return args and '%s?%s' % (url, quote_args(args)) or url


class OAuthClient:
    def __init__(self, server, consumer_key, consumer_secret, hmac_sha1=0, portal=0):
        self.server = server
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.token = None
        self.token_secret = None
        self.hmac_sha1 = hmac_sha1
        self.portal = portal

    def get(self, url_args={}):
        import urllib2
        url = make_url(self.server, url_args)
        oauth = self.authorization_header(url_args, post=False)
        log('+++', url)
        log('Authorization:', repr(oauth['Authorization']))

        request = urllib2.Request(url, None, oauth)
        response = urllib2.urlopen(request)
        reply = response.read()

        log('Reply:', repr(reply))
        return reply

    def get_hmac_sha1(self, sig, args, post):
        import hmac, hashlib, base64
        base = signature_base_string(post and 'POST' or 'GET', self.server, args)
        hashed = hmac.new(sig, base, hashlib.sha1)
        return base64.b64encode(hashed.digest())

    def pack(self, d):
        return ','.join(((k + '="' + str(v) + '"') for (k,v) in d.items()))

    def authorization_header(self, url_args={}, post=False):
        import time, random
        oauth_signature = self.consumer_secret + '&'
        if self.token_secret:
            oauth_signature += self.token_secret

        oauth_args = {}
        oauth_args['oauth_consumer_key'] = self.consumer_key
        oauth_args['oauth_timestamp'] = int(time.time())
        oauth_args['oauth_nonce'] = random.randint(0, 2**32)
        oauth_args['oauth_version'] = '1.0'
        if self.token:
            oauth_args['oauth_token'] = self.token

        if self.hmac_sha1:
            oauth_args['oauth_signature_method'] = 'HMAC-SHA1'
            args = url_args.copy()
            args.update(oauth_args)
            oauth_args['oauth_signature'] = self.get_hmac_sha1(oauth_signature, args, post)
        else:
            oauth_args['oauth_signature_method'] = 'PLAINTEXT'
            oauth_args['oauth_signature'] = quote(oauth_signature)

        oauth_args = 'OAuth ' + self.pack(oauth_args)
        return {'Authorization': oauth_args}

    def split_reply(self, reply):
        args = reply.split('&')
        return dict((s.split('=') for s in args))

    # request oauth token
    def request_token(self):
        args = bscw_oauth_args.copy()
        if self.portal: args['portal'] = 1
        return self.split_reply(self.get(args))

    # request oauth access token
    def access_token(self):
        args = bscw_oauth_args.copy()
        if self.portal: args['portal'] = 1
        return self.split_reply(self.get(args))


class BscwApi:
    """
    BSCW-XML-RPC access with OAuth authentication.
    """

    def __init__(self, script_uri):
        self.script_uri = script_uri

    def show_form(self, request):
        return render(request, 'pb_oauth/index.html', {
            'title': 'CloudTeams Persona Builder',
            'form': True,
            'bscw_api': self,
        })

    def store_user_content(self, request, srv):
        # get id of authorized user/developer
        home_id = srv.get_attributes()[0]['__id__']
        attributes = ['__class__', '__id__', 'name']

        # get all software projects in user's home folder, only top level once
        result = srv.get_attributes(home_id, attributes, 2)

        project_lst = []
        campaign_lst = []
        for obj in result:
            classname = obj['__class__']
            if classname == 'bscw.core.cloudteams.cl_softwareproject.Softwareproject':
                project_lst.append(obj)
            elif classname == 'bscw.core.cloudteams.cl_campaign.Campaign':
                campaign_lst.append(obj)

        request.session['projects'] = [{
            'pid': p['__id__'],
            'title': p['name'],
        } for p in project_lst]
        request.session['campaigns'] = [{
            'cid': c['__id__'],
            'title': c['name'],
        } for c in campaign_lst]

    @staticmethod
    def authorization_url():
        return '/persona-builder/authorize/?action=authorize&host=%s' % quote(DEFAULT_HOST)

    def authorize(self, reply):
        import base64
        args = bscw_oauth_args.copy()

        args['action'] = 'doit'
        args['host'] = self.host
        args['a1'] = base64.encodestring(reply['oauth_token'])
        args['a2'] = base64.encodestring(reply['oauth_token_secret'])
        if self.verbose:
            args['verbose'] = self.verbose
        if self.portal:
            args['portal'] = self.portal
        if self.hmac_sha1:
            args['hmac_sha1'] = self.hmac_sha1

        callback_url = make_url(self.script_uri, args)

        args = bscw_oauth_args.copy()
        args['oauth_token'] = reply['oauth_token']
        args['oauth_callback'] = callback_url
        if self.portal:
            args['portal'] = self.portal
        if self.hmac_sha1:
            args['hmac_sha1'] = self.hmac_sha1
        url = make_url(self.oauth.server, args)

        return redirect(url)

    def store_token(self, request):
        oauth = self.oauth.authorization_header(post=True)
        request.session['bswc_token'] = oauth['Authorization']

        # also store user information in session
        srv = XMLRPC_Server(self.oauth.server, verbose=self.verbose, oauth=oauth['Authorization'])
        user_home_id = srv.get_attributes()[0]['__id__']  # get user's home folder
        user = srv.get_attributes(user_home_id, ['user', ])[0]['user']  # gets user's info

        # store common items in session
        request.session['user_id'] = user['__id__']
        request.session['username'] = user['name']
        self.store_user_content(request, srv)

    """
    def doit(self):

        oauth = self.oauth.authorization_header(post=True)
        srv = XMLRPC_Server(self.oauth.server, verbose=self.verbose, oauth=oauth['Authorization'])

        self.html_pre('access api with OAuth')
        print '<plaintext />'

        print '##### get home object of user: get_attributes()'
        result = srv.get_attributes()
        dump(result)

        print ''
        print "##### get direcory listing of user's home: get_attributes(__id__, ['name','owner'], 2)"
        h_id = result[0]['__id__']
        result = srv.get_attributes(h_id, ['name','owner'], 2)
        dump(result)
    """

    def show_error(self, request, e, title='error'):
        return render(request, 'pb_oauth/index.html', {
            'title': title,
            'error': e,
            'bscw_api': self,
        })

    def handle(self, request):
        # get POST & GET parameters
        form = request.GET.copy()
        form.update(request.POST)

        action = form.get('action')
        self.host = form.get('host')

        if self.host is None:
            self.host = DEFAULT_HOST
        else:
            # fix issue with a1 parameter not recognised
            for h in form.getlist('host'):
                if '?' in h:
                    _spl = h.split('?')
                    self.host = _spl[0]
                    _spl_eq = _spl[1].split('=')
                    form[_spl_eq[0]] = '='.join(_spl_eq[1:])

        if 'verbose' in form:
            self.verbose = int(form.get('verbose'))
        else:
            self.verbose = None
        if 'portal' in form:
            self.portal = int(form.get('portal'))
        else:
            self.portal = None
        if 'hmac_sha1' in form:
            self.hmac_sha1 = int(form.get('hmac_sha1', 'hmac'))
        else:
            self.hmac_sha1 = 0

        log('###', action, os.environ.get('REQUEST_METHOD', ''))
        log(self.script_uri+'?'+os.environ.get('QUERY_STRING', ''))

        self.oauth = OAuthClient(
            servers[self.host],
            consumer_keys[self.host],
            consumer_secrets[self.host],
            self.hmac_sha1,
            self.portal,
        )

        if action is None:
            return self.show_form(request)

        elif action == 'authorize':
            try:
                reply = self.oauth.request_token()   # A Comsumer Request - Request Token
            except urllib2.HTTPError, e:
                return self.show_error(request, e, 'Request token error')

            return self.authorize(reply)                    # C Consumer Directs User to Service Provider

        elif action == 'doit':
            self.oauth.token = base64.decodestring(form.get('a1'))
            self.oauth.token_secret = base64.decodestring(form.get('a2'))
            try:
                reply = self.oauth.access_token()    # E Comsumer Request - Access Token
            except urllib2.HTTPError, e:
                return self.show_error(request, e, 'Access token error')
            self.oauth.token = urllib.unquote(reply['oauth_token'])
            self.oauth.token_secret = urllib.unquote(reply['oauth_token_secret'])
            self.store_token(request)  # G Consumer Stores token in session (encrypted in db) for future use

            return redirect('/persona-builder/personas/')
