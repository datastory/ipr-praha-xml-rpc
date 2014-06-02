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
        for schema in response.tables.userschema:

            print("%s: %s" % ('Schema', schema.attrib['name']))

            for table in schema.table:
                print("\t- %s" % (table.attrib['name']))

    def get_data(self, schema, table):
        """Get data from table
        """

        response = objectify.fromstring(self.proxy.getschema(self.token).encode("utf-8"))
        for schema in response.tables.userschema:

            print("%s: %s" % ('Schema', schema.attrib['name']))

            for table in schema.table:
                print("\t- %s" % (table.attrib['name']))




def main():
    """Main method parses arguments
    """

    parser = argparse.ArgumentParser(description='IPR database connector')
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

    args = parser.parse_args()

    if args.password and\
       args.url and\
       args.user:
        proxy = Proxy(args.url, args.user, args.password)
        proxy.connect()

        if args.list:
            proxy.list_datasets()

        elif args.schema and\
            args.table:
            print(proxy.get_data(
                args.schema, args.table))


        proxy.unconnect()

if __name__ == '__main__':
    main()
