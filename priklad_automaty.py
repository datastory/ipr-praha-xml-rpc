# -*- coding: utf-8 -*-
# Python 3

#Priklad pouziti XML-RPC rozhrani IPR Praha. Po prihlaseni stahne a ulozi do csv informace z vrstvy parkovacich automatu.

import xmlrpc.client
import xml.etree.ElementTree as ET
import csv

proxy = xmlrpc.client.ServerProxy('http://app.urm.cz/ws/RPC2UTF8/') 
#ziska token pro uzivatele hackathon, heslo 'hackathon' (MD5)
token = proxy.authenticate('hackathon', 'c1d43a1b8cfa81c6b26fa036e328af0b')

#vypise schema dostupnych datovych sad v XML
#print(proxy.getschema(token))

#stahne sadu z ulozeneho dotazu c. 21 (automaty), viz. getschema -> storedqueries a vyexportuje ji do csv
#souradnicovy system S-JTSK (Greenwich) / Krovak East North (EPSG: 102067)
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
        x = automat[0].text.replace(',','.')
        y = automat[1].text.replace(',','.')
        hodiny = automat[2].text
        tarif_kc_h = automat[3].text.replace(',','.')
        tarif_eur = automat[4].text.replace(',','.')
        typ = automat[5].text
        poznamka = automat[6].text
    
        writer.writerow([x, y, hodiny, tarif_kc_h, tarif_eur, typ, poznamka])

#zahodi token
proxy.deauthenticate(token)