# -*- coding: utf-8 -*-

"""resolver_check.__main__:called as a script"""

import sys
import argparse
from random import shuffle
from .dns_test_loader import load_dnstests
from .resolver_check import run_test


def main():

    config = {}
    config['verbose'] = False
    config['quiet'] = False
    config['infile'] = ''
    config['shuffle_tests'] = False
    config['tests_to_run'] = 0
    resolvers = []
    tests = []

    ''' Parse args '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
            action='store_true',
            help='enable verbose output')

    parser.add_argument('-q', '--quiet',
            action='store_true',
            help='only output stats')

    parser.add_argument('-s', '--shuffle',
            action='store_true',
            help='shuffle tests')

    parser.add_argument('-c', '--count',
            type=int,
            metavar='N',
            help='number of tests to preform, zero runs all tests in file (default=0)')

    parser.add_argument('-f', '--file',
        dest='infile',
        required=True,
        metavar='INFILE',
        help='specify test file')

    args = parser.parse_args()

    if args.verbose:
        config['verbose'] = True

    if args.quiet:
        config['quiet'] = True

    if args.verbose and args.quiet:
        print('uncompatible args: verbose and quiet dont play')
        sys.exit(1)

    if args.infile:
        config['infile'] = args.infile


    if config['infile']:
        resolvers, tests = load_dnstests(config['infile'])

    if args.count:
        if args.count <= len(tests):
            config['tests_to_run'] = args.count

        else:
            print('error: not enough uniq tests in testfile!')
            sys.exit(1)

    if args.shuffle:
        config['shuffle_tests'] = True

    if config['shuffle_tests']:
        shuffle(tests)



    ''' Run tests '''
    total_querys = 0
    passed_querys = 0
    failed_querys = 0
    total_time = 0.0
    avg_time = 0.0
    max_time = None
    min_time = None

    if not config['quiet']:
        print('Running {} tests on {} nameservers'.format(len(tests) if not config['tests_to_run'] else config['tests_to_run'], len(resolvers)))

    for index,test in enumerate(tests):
        for resolver in resolvers:

            result = run_test(resolver, test)

            if not config['quiet']:
                print("{testid}: @{addr}:{port} ({proto}) {domain} {rdtype}...{result}{time}{result_details}".format(
                    testid=index,
                    addr=resolver.addr,
                    port=resolver.port,
                    proto=test.proto,
                    domain=test.domain,
                    rdtype=test.rdtype,
                    result='passed' if result['pass'] else 'failed',
                    time=' in {:.6f}s'.format(result['time']) if config['verbose'] else '',
                    result_details=' ({})'.format(result['msg']) if config['verbose'] else ''

                ))

            if result['pass']:
                passed_querys += 1
            else:
                failed_querys += 1

            total_time += result['time']
            if result['time'] > max_time or max_time == None:
                max_time = result['time']

            if result['time'] < min_time or min_time == None:
                min_time = result['time']

            resolver.add_to_metrics(result)

            total_querys += 1

        if config['tests_to_run'] and index+1 >= config['tests_to_run']:
            break

    if not config['quiet']:
        print('')


    for resolver in resolvers:
        print('Resolver ({}) {} tests processed in {}s ({} passed, {} failed)'.format(
            resolver.addr,
            resolver.total_querys,
            resolver.total_time,
            resolver.passed_querys,
            resolver.failed_querys))

        print('max query time {}s'.format(resolver.max_time))
        print('avg query time {}s'.format(resolver.total_time / resolver.total_querys))
        print('min query time {}s'.format(resolver.min_time))
        print('')


    print('Summary from {} resolvers with a total of {} tests processed in {}s ({} passed, {} failed)'.format(len(resolvers), total_querys, total_time, passed_querys, failed_querys))
    print('max query time {}s'.format(max_time))
    print('avg query time {}s'.format(total_time / total_querys))
    print('min query time {}s'.format(min_time))

