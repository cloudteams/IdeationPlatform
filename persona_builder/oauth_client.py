from requests_oauthlib import OAuth1Session


class PersonaBuilderOAuthClient:

    def __init__(self):
        self.oauth_url = 'https://cloudteams.fit.fraunhofer.de/bscw/bscw.cgi?op=OAuth'
        self.client_key = 'Persona Builder'
        self.client_secret = '0d22c6dfccef7ca8160b73512a485eaf'

        self.oauth = OAuth1Session(self.client_key, client_secret=self.client_secret)
        #fetch_response = oauth.fetch_request_token(self.oauth_url)

    def get(self, url, **kwargs):
        return self.oauth.get(url=url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.oauth.post(self, url=url, data=data, json=json, **kwargs)

