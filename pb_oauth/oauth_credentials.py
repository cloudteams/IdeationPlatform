import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from ct_anonymizer.settings import SERVER_URL

consumer_keys = {
    'cloudteams.epu.ntua.gr': 'Persona Builder',
    'cloudteams.epu.ntua.gr%3A': 'Persona Builder',
    'customers.cloudteams.eu%3A': 'Persona Builder',
}

consumer_secrets = {
    'cloudteams.epu.ntua.gr': '60a6420a6e1e0b95719ffef43903e329',
    'cloudteams.epu.ntua.gr%3A': '60a6420a6e1e0b95719ffef43903e329',
    'customers.cloudteams.eu%3A': '60a6420a6e1e0b95719ffef43903e329',
}
servers = {
    'cloudteams.epu.ntua.gr': SERVER_URL,
    'cloudteams.epu.ntua.gr%3A': SERVER_URL,
    'customers.cloudteams.eu%3A': SERVER_URL,
}
