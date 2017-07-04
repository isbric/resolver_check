# -*- coding: utf-8 -*-

"""resolver_check.dnstest_loader:"""

from .dns_test_obj import DnsTestObj
from .resolver_obj import ResolverObj

def load_dnstests(infile = ''):
    import yaml
    import os
    import sys
    import dns.rcode

    resolvers = []
    dnstests = []

    with open(os.path.relpath(os.path.expanduser(infile)), 'r') as stream:
        try:
            yamldata = yaml.load(stream)
        except yaml.YAMLError as e:
            print('Configuration error: {}'.format(e))
            sys.exit(1)

        try:
            for resolver in yamldata['resolvers']:
                try:
                    resolvers.append(ResolverObj(
                        addr = resolver['addr'],
                        port = resolver['port'],
                        udp = resolver['udp'],
                        tcp = resolver['tcp']
                        ))
                except KeyError as e:
                    print('Configuration error: missing item {} while processing resolver -> {}'.format(e, resolver))
                    sys.exit(1)

        except KeyError as e:
            print('Configuration error: Could not find {} section in file!'.format(e))
            sys.exit(1)


        try:
            for test in yamldata['tests']:
                try:
                    dnstests.append(DnsTestObj(
                        domain = test['domain'],
                        rdtype = test['rdtype'],
                        expected_rcode = test['expected_rcode'],
                        expected_data = test['expected_data'],
                        proto = test['proto'],
                        timeout = test['timeout']
                        ))
                except KeyError as e:
                    print('Configuration error: failed to load item {} while processing test -> {}'.format(e, test))
                    sys.exit(1)

        except KeyError as e:
            print('Could not find {} section in file!'.format(e))
            sys.exit(1)


    for test in dnstests:
        try:
            getattr(dns.rcode, test.expected_rcode)
        except AttributeError as e:
            print('Configuration error: rcode {} not found in dns.rcode while validating test:'.format(test.expected_rcode))
            print(' domain -> {}'.format(test.domain))
            print(' rdtype -> {}'.format(test.rdtype))
            print(' expected_rcode -> {}'.format(test.expected_rcode))
            print(' expected_data -> {}'.format(test.expected_data))
            print(' proto -> {}'.format(test.proto))
            print(' timeout -> {}'.format(test.timeout))
            print('')

            print('Valid rcodes are:')
            for rcode in [attr for attr in dir(dns.rcode) if not callable(getattr(dns.rcode, attr)) and not attr.startswith("_") and attr.isupper()]:
                print(' {}'.format(rcode))
            sys.exit(1)


    # Sort data to make it easyer to compare later
    for test in dnstests:
        if isinstance(test.expected_data, list):
            test.expected_data.sort()

    return resolvers, dnstests
