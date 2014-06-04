#!/usr/bin/env python3
"""Example connector to database available at IPR Praha http://geoportalpraha.cz

The connector should be used as example, about how to connect to Oracle
database using XML-RPC method.
More detailed documentation can be found at http://app.urm.cz/ws/index.html
"""

__author__ = "Jan Cibulka, Jachym Cepicky, Vojtech Dubrovsky"
__copyright__ = "Copyright 2014"
__license__ = "BSD"
__version__ = "0.1-dev"
__maintainer__ = "Jachym Cepicky"
__email__ = "jachym.cepicky gmail"
__status__ = "Prototype"

import xmlrpc.client
import argparse
from lxml import etree
from lxml import objectify
from lxml.etree import tostring
from prettytable import PrettyTable


PROXY = 'http://app.urm.cz/ws/RPC2UTF8/'
USER = 'anonymous@ipr.praha.eu',
PASSWORD = '294de3557d9d00b3d2d8a1e6aab028cf'

class Proxy:
    """Simple class managing connection to database
    """
    def __init__ (self, url, user, password):

        self.token = None
        self.url = url
        self.user = user
        self.password = password

        self.proxy = xmlrpc.client.ServerProxy(url)

    def connect(self):
        """Provide connection to database

        :return: connection token
        """
        self.token =  self.proxy.authenticate(self.user, self.password)
        return self.token

    def unconnect(self):
        """Close connection
        """
        return self.proxy.deauthenticate(self.token)

    def list_datasets(self):
        """Print list of available datasets
        """

        response = objectify.fromstring(self.proxy.getschema(self.token).encode("utf-8"))

        print("Stored queries:\n")
        for query in response.storedqueries.query:
            print ("%s: %s" % (query.attrib['id'], query.qdescription.text))
            try:
                for param in query.qparam:
                    print("\t%s: %s" % (param.attrib['id'], param.qpdescription))
            except:
                pass

        print("\n----\nTables:\n")

        for schema in response.tables.userschema:

            print("%s: %s" % ('Schema', schema.attrib['name']))

            for table in schema.table:
                print("\t- %s" % (table.attrib['name']))

    def get_stored_queries(self, query, attrib=None, value=None):
        """Get data from table
        """

        #request = objectify.Element("request")
        #params = objectify.SubElement(request, "params")
        #if attrib:
        #    param = objectify.SubElement(params, "param")
        #    parid = objectify.SubElement(param, "parid")
        #    parval = objectify.SubElement(param, "content")
        #    parid = attrib
        #    parval = value

        request = '<?xml version="1.0" encoding="UTF-8"?> \
            <request>\
            <params>\
            </params>\
            </request>'

        response = objectify.fromstring(
            self.proxy.getstoredqueryresult(self.token, query, 1000, 0, request, False).encode("utf-8"))

        table_head = []
        for col in response.query.cols.col:
            table_head.append(col.name)
        table = PrettyTable(table_head)

        for row in response.rows.r:
            row_data = []
            for col in row.c:
                row_data.append(col.text)
            table.add_row(row_data)
        print(table)
        #response = objectify.fromstring(self.proxy.getschema(self.token).encode("utf-8"))
        #response = objectify.fromstring(
        #    self.proxy.getstoredqueryr(token, 21, 1000, 0, xmlparams, False)
        #for schema in response.tables.userschema:

        #    print("%s: %s" % ('Schema', schema.attrib['name']))

        #    for table in schema.table:
        #        print("\t- %s" % (table.attrib['name']))

    def get_xml(self, xml):
        print(
            objectify.fromstring(
            self.proxy.getcomposedqueryresult(self.token, open(xml).read(), False).encode("utf-8"))
        )




def main():
    """Main method parses arguments
    """

    parser = argparse.ArgumentParser(description='IPR database connector',
                                     epilog="""Example usage: |
                                     connector.py --l # print list of available queries |
                                     connector.py --query=21 # print result from pre-stored query nr.21
                                     """)
    parser.add_argument('--url', dest='url',
                        help='URL of the proxy', default=PROXY)
    parser.add_argument('--user', dest='user',
                        default='anonymous@ipr.praha.eu',
                        help='User of the proxy')
    parser.add_argument('--password', dest='password',
                        default=PASSWORD,
                        help='Password (md5 encoded)')
    parser.add_argument('--list', action='store_true',
                        help='List available tables')
    parser.add_argument('--schema', dest='schema',
                        help='Schema name')
    parser.add_argument('--table', dest='table',
                        help='Table name')
    parser.add_argument('--query', dest='query',
                        help='Stored query id')
    parser.add_argument('--attribute', dest='attribute',
                        help='Stored query attribute')
    parser.add_argument('--value', dest='value',
                        help='Stored query value')
    parser.add_argument('--xml', dest='xml',
                        help='Input XML request')

    args = parser.parse_args()

    if args.password and\
       args.url and\
       args.user:
        proxy = Proxy(args.url, args.user, args.password)
        proxy.connect()

        if args.list:
            proxy.list_datasets()
        elif args.query:
            proxy.get_stored_queries(args.query, args.attribute, args.value)
        elif args.xml:
            proxy.get_xml(args.xml)

        #elif args.schema and\
        #    args.table:
        #    print(proxy.get_data(
        #        args.schema, args.table))


        proxy.unconnect()

if __name__ == '__main__':
    main()
