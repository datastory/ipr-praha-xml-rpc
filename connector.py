# -*- coding: utf-8 -*-
# Python 3

import xmlrpc.client

proxy = xmlrpc.client.ServerProxy('http://app.urm.cz/ws/RPC2UTF8/') 
#ziska token pro uzivatele anonymous@ipr.praha.eu, heslo 'anonymous' (MD5)
token = proxy.authenticate('anonymous@ipr.praha.eu', '294de3557d9d00b3d2d8a1e6aab028cf')

#vypise schena dostupnych datovych sad v XML
print(proxy.getschema(token))

#vypise sadu z ulozeneho dotazu c. 21 (automaty), viz. getschema -> storedqueries
xmlparams = '<?xml version="1.0" encoding="UTF-8"?> \
<request>\
<params>\
</params>\
</request>'


a = proxy.getstoredqueryresult(token, 21, 1000, 0, xmlparams, False)
print (a)

#zahodi token
proxy.deauthenticate(token)