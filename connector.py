# -*- coding: utf-8 -*-
# Python 3

import xmlrpc.client

proxy = xmlrpc.client.ServerProxy('http://app.urm.cz/ws/RPC2UTF8/') 
#ziska token pro uzivatele anonymous@ipr.praha.eu, heslo 'anonymous' (MD5)
token = proxy.authenticate('anonymous@ipr.praha.eu', '294de3557d9d00b3d2d8a1e6aab028cf')

#vypise schena dostupnych datovych sad v XML
print(proxy.getschema(token))

#zahodi token
proxy.deauthenticate(token)