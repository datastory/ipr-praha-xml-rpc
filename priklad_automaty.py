# -*- coding: utf-8 -*-
# Python 3

#Priklad pouziti XML-RPC rozhrani IPR Praha. Po prihlaseni stahne a ulozi do csv informace z vrstvy parkovacich automatu.

import xmlrpc.client
import xml.etree.ElementTree as ET
import csv

proxy = xmlrpc.client.ServerProxy('http://app.urm.cz/ws/RPC2UTF8/') 
#ziska token pro uzivatele anonymous@ipr.praha.eu, heslo 'anonymous' (MD5)
token = proxy.authenticate('anonymous@ipr.praha.eu', '294de3557d9d00b3d2d8a1e6aab028cf')

#vypise schema dostupnych datovych sad v XML
#print(proxy.getschema(token))

#stahne sadu z ulozeneho dotazu c. 21 (automaty), viz. getschema -> storedqueries a vyexportuje ji do csv
#souradnicovy system S-JTSK
xmlparams = '<?xml version="1.0" encoding="UTF-8"?> \
<request>\
<params>\
</params>\
</request>'


response = proxy.getstoredqueryresult(token, 21, 1000, 0, xmlparams, False)
root = ET.fromstring(response)

with open('./automaty.csv', 'w', newline='') as out:
    writer = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['x', 'y', 'hodiny', 'tarif_kc_h', 'tarif_eur', 'typ', 'poznamka'])
    
    for automat in root[1]:
        x = automat[0].text
        y = automat[1].text
        hodiny = automat[2].text
        tarif_kc_h = automat[3].text
        tarif_eur = automat[4].text
        typ = automat[5].text
        poznamka = automat[6].text
    
        writer.writerow([x, y, hodiny, tarif_kc_h, tarif_eur, typ, poznamka])

#zahodi token
proxy.deauthenticate(token)