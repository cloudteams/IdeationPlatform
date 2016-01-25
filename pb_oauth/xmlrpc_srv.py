# configure a xmlrpclib server object for BSCW
# R. Ruland
#---------------------------------------------------------------------------
# All code contained herein is covered by the Copyright as distributed
# in the BSCW_COPYRIGHT file in the main directory of the distribution
# of the BSCW server.
#---------------------------------------------------------------------------

debug_level = 0

def XMLRPC_Server(uri, user_passwd=None, encoding=None,
                    verbose=None, allow_none=0, use_datetime=0, oauth=None):
    import urllib, xmlrpclib
    if verbose is None:
        verbose = debug_level

    if user_passwd or oauth:

        uri_type = urllib.splittype(uri)[0]
        if uri_type == "https":
            BaseTransport = xmlrpclib.SafeTransport
        else:
            BaseTransport = xmlrpclib.Transport

        class AuthorizedTransport(BaseTransport):
            def __init__(self, use_datetime=0, user_passwd='', oauth=None):
                import base64, string
                BaseTransport.__init__(self, use_datetime=use_datetime)
                if user_passwd:
                    self.auth = string.strip(base64.encodestring(user_passwd))
                self.oauth = oauth

            def send_host(self, connection, host):
                BaseTransport.send_host(self, connection, host)
                if self.oauth:
                    connection.putheader('Authorization', self.oauth)
                elif self.auth:
                    connection.putheader('Authorization',
                        'Basic %s'%self.auth)

        ServerTransport = AuthorizedTransport(use_datetime, user_passwd, oauth)

    else:

        ServerTransport = None

    #ServerTransport.user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20041107 Firefox/1.0'
    #ServerTransport.user_agent = 'Apache XML RPC 3.1.3'

    return xmlrpclib.Server(uri, ServerTransport,
        encoding=encoding, verbose=verbose, allow_none=allow_none)
