import xmlrpc_oauth


def authorize(request):
    auth_url = request.build_absolute_uri()
    print auth_url
    if '?' in auth_url:
        auth_url = auth_url.split('?')[0]

    return xmlrpc_oauth.BscwApi(auth_url).handle(request)
