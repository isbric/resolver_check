# -*- coding: utf-8 -*-

"""resolver_check.resolver_check:"""


def run_test(resolver, test):
    import dns.name
    import dns.message
    import dns.query
    import dns.inet
    import dns.rcode

    from .timer import Timer

    query_timer = Timer()
    domain = dns.name.from_text(test.domain)
    if not domain.is_absolute():
        domain = domain.concatenate(dns.name.root)

    request = dns.message.make_query(domain, dns.rdatatype.from_text(test.rdtype))

    try:
        if test.proto == 'udp':
            query_timer.start()
            response = dns.query.udp(q=request, af=dns.inet.AF_INET, where=resolver.addr, port=resolver.port, timeout=test.timeout)
            query_timer.stop()

        elif test.proto == 'tcp':
            query_timer.start()
            response = dns.query.tcp(q=request, af=dns.inet.AF_INET, where=resolver.addr, port=resolver.port, timeout=test.timeout)
            query_timer.stop()

    except dns.exception.Timeout as e:
        query_timer.stop()
        return { 'pass': False, 'msg': e, 'time': query_timer.time() }


    '''
    Check query respons against expected results
    '''

    # Handle NXDOMAIN responses
    if response.rcode() == dns.rcode.NXDOMAIN:

        # Check for expected rcode NXDOMAIN
        if response.rcode() == getattr(dns.rcode, test.expected_rcode):
            return { 'pass': True, 'msg': 'got expected rcode NXDOMAIN', 'time': query_timer.time() }

        else:
            return { 'pass': False, 'msg': 'got unexpected rcode NXDOMAIN', 'time': query_timer.time() }



    # Handle non NXDOMAIN responses
    else:

        # Check if we got expected rcode
        if response.rcode() == getattr(dns.rcode, test.expected_rcode):

            # Check length of responses
            if len(response.answer):

                # Check is expected response is a list
                if isinstance(test.expected_data, list):

                    responsetext = []
                    for item in response.answer[0].items:
                        responsetext.append(item.to_text())

                    responsetext.sort()

                    # Check if list of responses is the same langth as the list of expected responses
                    if len(test.expected_data) == len(response.answer[0]):

                        # Check if responses are equal to the expected data
                        if test.expected_data == responsetext:
                            return { 'pass': True, 'msg': 'Got expected responses \'{}\' with rcode {}'.format(responsetext, response.rcode()), 'time': query_timer.time() }

                        else:
                            return { 'pass': False, 'msg': 'Got unexpected response \'{}\' != \'{}\' with rcode {}'.format(responsetext, test.expected_data, response.rcode()), 'time': query_timer.time() }

                    # Response and expected response is not the same length
                    else:
                        return { 'pass': False, 'msg': 'Got unexpected number of responses \'{}\' != \'{}\' with rcode {}'.format(response.answer[0].items[0], test.expected_data, response.rcode()), 'time': query_timer.time() }
                else:
                    # Check if response data is equal to the expected data
                    if test.expected_data == response.answer[0].items[0].to_text():
                        return { 'pass': True, 'msg': 'Got expected response \'{}\' with rcode {}'.format(response.answer[0].items[0], response.rcode()), 'time': query_timer.time() }

                    # Not equal to expected data
                    else:
                        return { 'pass': False, 'msg': 'Got unexpected response \'{}\' != \'{}\' with rcode {}'.format(response.answer[0].items[0], test.expected_data, response.rcode()), 'time': query_timer.time() }


            # Got empty response
            else:

                # Empty response expected but with good rcode
                if not isinstance(test.expected_data, list) and test.expected_data == '':
                        return { 'pass': True, 'msg': 'Got expected response \'\' with rcode {}'.format(response.rcode()), 'time': query_timer.time() }

                # Good rcode but missing expected response
                else:
                    return { 'pass': False, 'msg': 'Got empty response with rcode: {}'.format(response.rcode()), 'time': query_timer.time() }

        # Got unexpected rcode
        else:
            return { 'pass': False, 'msg': 'Got unexpected rcode {}'.format(response.rcode()), 'time': query_timer.time() }


    # Catch all return, shuld never be hit
    return { 'pass': False, 'msg': 'Unknown error', 'time': query_timer.time() }
