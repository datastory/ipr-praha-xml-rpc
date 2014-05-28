#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Find out, which metadata area available at IPR

Author: Jachym Cepicky <jachym.cepicky gmail com>
Licence: BSD
"""

import argparse
from owslib.csw import CatalogueServiceWeb
from owslib.fes import PropertyIsLike

SERVER_URL = "http://wgp.urm.cz/geoportal/csw"

def get_service():
    """Get service capabilities"""
    return CatalogueServiceWeb(SERVER_URL)

def get_wms(service):
    """Get wms records

    :param service: csw service
    """

    #keywords = PropertyIsLike(propertyname='anyText', literal="ortofotomapa")
    services = PropertyIsLike(propertyname='type', literal="liveData")
    service.getrecords2(constraints=[services])

    print "Found: %s records" % (service.results['matches'])

    while service.results['returned'] > 0:
        service.getrecords2(constraints = [services],
                            startposition=service.results['nextrecord'])
        for rec in service.records:
            record = service.records[rec]
            try:
                print record.title, record.type, record.format, record.uris
                #print record.xml
            except UnicodeEncodeError:
                pass

def get_records(service):
    """Get service records

    :param service: csw service
    """

    service.getrecords2()
    nrrecords = service.results['matches']

    print "Found: %s records" % (service.results['matches'])

def get_all_record(service):

    out_records = []

    while service.results['returned'] > 0:
        service.getrecords2(startposition=service.results['nextrecord'])
        for rec in service.records:
            out_records.append(service.records[rec])

    for record in out_records:
        try:
            print record.title, record.type, record.format, record.uris
        except UnicodeEncodeError:
            pass

def main():
    """Main program, parses arguments
    """

    parser = argparse.ArgumentParser()
    #parser.add_argument('--keyword', help='Key word')
    #args = parser.parse_args()

    service = get_service()

    get_records(service)
    get_wms(service)

if __name__ == '__main__':
    main()
