from requests_oauthlib import OAuth1Session


class PersonaBuilderOAuthClient:

    def __init__(self):
        self.oauth_url = 'https://cloudteams.fit.fraunhofer.de/bscw/bscw.cgi?op=OAuth'
        self.client_key = 'Persona Builder'
        self.client_secret = '0d22c6dfccef7ca8160b73512a485eaf'

        self.oauth = OAuth1Session(self.client_key, client_secret=self.client_secret)
        fetch_response = self.oauth.fetch_request_token(self.oauth_url)
        self.resource_owner_key = fetch_response.get('oauth_token')
        self.resource_owner_secret = fetch_response.get('oauth_token_secret')

    def get_authorization_url(self):
        import pdb;pdb.set_trace()
        return self.oauth.authorization_url(self.oauth_url)

    def authorize(self):
        pass


