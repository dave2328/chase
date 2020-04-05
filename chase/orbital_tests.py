import os
import collections
from chase import Profile, Order, MarkForCapture, Reversal

merchant_id = os.environ.get('TEST_ORBITAL_MERCHANT_ID')
username = os.environ.get('TEST_ORBITAL_USERNAME')
password = os.environ.get('TEST_ORBITAL_PASSWORD')

def parse_result(step, result):
    parsed = '%s:' % step
    keyless = parsed
    for key in ['AuthCode', 'RespCode', 'AVSRespCode', 'CVV2RespCode',
                'TxRefNum', 'ApprovalStatus', 'TraceNumber',
                'CustomerRefNum']:
        if key in result:
            parsed = '%s %s:%s' % (parsed, key, result[key])
    if parsed == keyless:
        parsed = '%s raw:%s' % (parsed, result)
    return parsed

def section_a():
    """
    Auth Only, Mark for Capture, and Online Reversals Transactions
    """
    results = collections.OrderedDict()
    results['section'] = 'a'

    order = Order(merchant_id=merchant_id,
                  username=username,
                  password=password,
                  message_type='A',
                  cc_num='4788250000028291',
                  order_id='101',
                  cc_expiry='1116',
                  zip_code='11111',
                  cvd='111',
                  amount='30.00')
    results['1a'] = order.charge()
    if results['1a'] and 'TxRefNum' in results['1a']:
        tx_ref_num = results['1a']['TxRefNum']
        #tx_ref_idx = results['1a']['TxRefIdx']
        reversal = Reversal(tx_ref_num=tx_ref_num,
                            tx_ref_idx='0',
                            amount='30',
                            order_id=order.order_id)
        results['1b'] = reversal.reversal()

    order = Order(merchant_id=merchant_id,
                  username=username,
                  password=password,
                  message_type='A',
                  cc_num='4788250000028291',
                  order_id='102',
                  cc_expiry='1116',
                  zip_code='L6L2X9',
                  cvd='111',
                  amount='38.01')
    results['2'] = order.charge()

    order = Order(merchant_id=merchant_id,
                  username=username,
                  password=password,
                  message_type='A',
                  cc_num='4788250000028291',
                  order_id='103',
                  cc_expiry='1116',
                  zip_code='22222',
                  cvd='222',
                  amount='85.00')
    results['3a'] = order.charge()
    if results['3a'] and 'TxRefNum' in results['3a']:
        tx_ref_num = results['3a']['TxRefNum']
        #tx_ref_idx = results['3a']['TxRefIdx']
        capture = MarkForCapture(order_id=order.order_id,
                                 amount='85.00',
                                 tx_ref_num=tx_ref_num)
        results['3b'] = capture.request()

    order = Order(merchant_id=merchant_id,
                  username=username,
                  password=password,
                  message_type='A',
                  cc_num='4788250000028291',
                  order_id='104',
                  cc_expiry='1116',
                  zip_code='66666',
                  amount='0.00')
    results['4'] = order.charge()
    #tx_ref_num = results['4']['TxRefNum']
    #tx_ref_idx = results['4']['TxRefIdx']

    order = Order(merchant_id=merchant_id,
                  username=username,
                  password=password,
                  message_type='A',
                  cc_num='4788250000028291',
                  order_id='105',
                  cc_expiry='1116',
                  zip_code='11111',
                  cvd='555',
                  amount='125.00')
    results['5a'] = order.charge()
    if results['5a'] and "TxRefNum" in results['5a']:
        tx_ref_num = results['5a']['TxRefNum']
        #tx_ref_idx = results['5a']['TxRefIdx']
        capture = MarkForCapture(order_id=order.order_id,
                                 amount='75.00',
                                 tx_ref_num=tx_ref_num)
        results['5b'] = capture.request()

    order = Order(merchant_id=merchant_id,
                  username=username,
                  password=password,
                  message_type='A',
                  cc_num='5454545454545454',
                  order_id='106',
                  cc_expiry='1116',
                  zip_code='L6L2X9',
                  amount='41.00')
    results['6a'] = order.charge()
    if results['6a'] and "TxRefNum" in results['6a']:
        tx_ref_num = results['6a']['TxRefNum']
        #tx_ref_idx = results['6a']['TxRefIdx']
        reversal = Reversal(tx_ref_num=tx_ref_num,
                            tx_ref_idx='0',
                            amount='41.00',
                            order_id=order.order_id)
        results['6b'] = reversal.reversal()

    order = Order(merchant_id=merchant_id,
                  username=username,
                  password=password,
                  message_type='A',
                  cc_num='5454545454545454',
                  order_id='107',
                  cc_expiry='1116',
                  zip_code='88888',
                  cvd='666',
                  amount='11.02')
    results['7'] = order.charge()

    order = Order(merchant_id=merchant_id,
                  username=username,
                  password=password,
                  message_type='A',
                  cc_num='5454545454545454',
                  order_id='108',
                  cc_expiry='1116',
                  zip_code='L6L2X9',
                  cvd='666',
                  amount='70.00')
    results['8a'] = order.charge()
    if results['8a'] and "TxRefNum" in results['8a']:
        tx_ref_num = results['8a']['TxRefNum']
        #tx_ref_idx = results['8a']['TxRefIdx']
        capture = MarkForCapture(order_id=order.order_id,
                                 amount='70.00',
                                 tx_ref_num=tx_ref_num)
        results['8b'] = capture.request()

    order = Order(merchant_id=merchant_id,
                  username=username,
                  password=password,
                  message_type='A',
                  cc_num='5454545454545454',
                  order_id='109',
                  cc_expiry='1116',
                  zip_code='55555',
                  cvd='222',
                  amount='100.00')
    results['9a'] = order.charge()
    if results['9a'] and "TxRefNum" in results['9a']:
        tx_ref_num = results['9a']['TxRefNum']
        #tx_ref_idx = results['9a']['TxRefIdx']
        capture = MarkForCapture(order_id=order.order_id,
                                 amount='70.00',
                                 tx_ref_num=tx_ref_num)
        results['9b'] = capture.request()

    order = Order(merchant_id=merchant_id,
                  username=username,
                  password=password,
                  message_type='A',
                  cc_num='5454545454545454',
                  order_id='110',
                  cc_expiry='1116',
                  zip_code='88888',
                  amount='0.00')
    results['10'] = order.charge()

    order = Order(merchant_id=merchant_id,
                  username=username,
                  password=password,
                  message_type='A',
                  cc_num='371449635398431',
                  order_id='111',
                  cc_expiry='1116',
                  zip_code='L6L2X9',
                  amount='1055.00')
    results['11a'] = order.charge()
    if results['11a'] and "TxRefNum" in results['11a']:
        tx_ref_num = results['11a']['TxRefNum']
        #tx_ref_idx = results['11a']['TxRefIdx']
        capture = MarkForCapture(order_id=order.order_id,
                                amount='500.00',
                                tx_ref_num=tx_ref_num)
        results['11b'] = capture.request()

    order = Order(merchant_id=merchant_id,
                  username=username,
                  password=password,
                  message_type='A',
                  cc_num='371449635398431',
                  order_id='112',
                  cc_expiry='1116',
                  zip_code='44444',
                  amount='55.00')
    results['12a'] = order.charge()
    if results['12a'] and "TxRefNum" in results['12a']:
        tx_ref_num = results['12a']['TxRefNum']
        #tx_ref_idx = results['12a']['TxRefIdx']
        reversal = Reversal(tx_ref_num=tx_ref_num,
                            tx_ref_idx='0',
                            amount='55.00',
                            order_id=order.order_id)
        results['12b'] = reversal.reversal()

    order = Order(merchant_id=merchant_id,
                  username=username,
                  password=password,
                  message_type='A',
                  cc_num='371449635398431',
                  order_id='113',
                  cc_expiry='1116',
                  zip_code='44444',
                  cvd='2222',
                  amount='75.00')
    results['13a'] = order.charge()
    if results['13a'] and "TxRefNum" in results['13a']:
        tx_ref_num = results['13a']['TxRefNum']
        #tx_ref_idx = results['13a']['TxRefIdx']
        capture = MarkForCapture(order_id=order.order_id,
                                amount='75.00',
                                tx_ref_num=tx_ref_num)
        results['13b'] = capture.request()

    order = Order(merchant_id=merchant_id,
                  username=username,
                  password=password,
                  message_type='A',
                  cc_num='371449635398431',
                  order_id='114',
                  cc_expiry='1116',
                  zip_code='22222',
                  amount='0.00')
    results['14'] = order.charge()

    order = Order(merchant_id=merchant_id,
                  username=username,
                  password=password,
                  message_type='A',
                  cc_num='6011000995500000',
                  order_id='115',
                  cc_expiry='1116',
                  zip_code='77777',
                  amount='10.00')
    results['15a'] = order.charge()
    if results['15a'] and "TxRefNum" in results['15a']:
        tx_ref_num = results['15a']['TxRefNum']
        #tx_ref_idx = results['15a']['TxRefIdx']
        capture = MarkForCapture(order_id=order.order_id,
                                amount='10.00',
                                tx_ref_num=tx_ref_num)
        results['15b'] = capture.request()

    order = Order(merchant_id=merchant_id,
                  username=username,
                  password=password,
                  message_type='A',
                  cc_num='6011000995500000',
                  order_id='116',
                  cc_expiry='1116',
                  zip_code='77777',
                  amount='15.00')
    results['16a'] = order.charge()
    if results['16a'] and "TxRefNum" in results['16a']:
        tx_ref_num = results['16a']['TxRefNum']
        #tx_ref_idx = results['16a']['TxRefIdx']
        reversal = Reversal(tx_ref_num=tx_ref_num,
                            tx_ref_idx='0',
                            amount='15.00',
                            order_id=order.order_id)
        results['16b'] = reversal.reversal()

    order = Order(merchant_id=merchant_id,
                  username=username,
                  password=password,
                  message_type='A',
                  cc_num='6011000995500000',
                  order_id='117',
                  cc_expiry='1116',
                  zip_code='L6L2X9',
                  cvd='444',
                  amount='63.03')
    results['17'] = order.charge()

    order = Order(merchant_id=merchant_id,
                  username=username,
                  password=password,
                  message_type='A',
                  cc_num='6011000995500000',
                  order_id='118',
                  cc_expiry='1116',
                  zip_code='L6L2X9',
                  cvd='444',
                  amount='63.03')
    results['18'] = order.charge()

    order = Order(merchant_id=merchant_id,
                  username=username,
                  password=password,
                  message_type='A',
                  cc_num='3566002020140006',
                  order_id='119',
                  cc_expiry='1116',
                  zip_code='33333',
                  amount='29.00')
    results['19'] = order.charge()

    return results

def section_b():
    """
    Auth Capture and Online Reversal Transactions
    """
    results = collections.OrderedDict()
    results['section'] = 'b'

    order = Order(message_type='AC',
                  cc_num='4788250000028291',
                  order_id='201',
                  cc_expiry='1116',
                  zip_code='11111',
                  cvd='111',
                  amount='30.00')
    results['1a'] = order.charge()
    tx_ref_num = result['TxRefNum']
    tx_ref_idx = result['TxRefIdx']
    reversal = Reversal(tx_ref_num=tx_ref_num,
                        tx_ref_idx='0',
                        amount='30.00',
                        order_id=order.order_id)
    results['1b'] = reversal.reversal()

    order = Order(message_type='AC',
                  cc_num='4788250000028291',
                  order_id='202',
                  cc_expiry='1116',
                  zip_code='L6L2X9',
                  cvd='111',
                  amount='38.01')
    results['2'] = order.charge()

    order = Order(message_type='AC',
                  cc_num='4788250000028291',
                  order_id='203',
                  cc_expiry='1116',
                  zip_code='22222',
                  cvd='222',
                  amount='85.00')
    results['3'] = order.charge()
    
    order = Order(message_type='AC',
                  cc_num='4788250000028291',
                  order_id='204',
                  cc_expiry='1116',
                  zip_code='11111',
                  cvd='555',
                  amount='125.00')
    results['4'] = order.charge()

    order = Order(message_type='AC',
                  cc_num='5454545454545454',
                  order_id='205',
                  cc_expiry='1116',
                  zip_code='L6L2X9',
                  amount='41.00')
    results['5a'] = result = order.charge()
    tx_ref_num = result['TxRefNum']
    tx_ref_idx = result['TxRefIdx']
    reversal = Reversal(tx_ref_num=tx_ref_num,
                        tx_ref_idx='0',
                        amount='41.00',
                        order_id=order.order_id)
    results['5b'] = reversal.reversal()

    order = Order(message_type='AC',
                  cc_num='5454545454545454',
                  order_id='206',
                  cc_expiry='1116',
                  zip_code='88888',
                  cvd='666',
                  amount='11.02')
    results['6'] = order.charge()

    order = Order(message_type='AC',
                  cc_num='5454545454545454',
                  order_id='207',
                  cc_expiry='1116',
                  zip_code='L6L2X9',
                  cvd='666',
                  amount='70.00')
    results['7'] = order.charge()

    order = Order(message_type='AC',
                  cc_num='5454545454545454',
                  order_id='208',
                  cc_expiry='1116',
                  zip_code='55555',
                  cvd='222',
                  amount='100.00')
    results['8'] = order.charge()

    order = Order(message_type='AC',
                  cc_num='371449635398431',
                  order_id='209',
                  cc_expiry='1116',
                  zip_code='L6L2X9',
                  amount='1055.00')
    results['9'] = order.charge()

    order = Order(message_type='AC',
                  cc_num='371449635398431',
                  order_id='210',
                  cc_expiry='1116',
                  zip_code='44444',
                  amount='55.00')
    results['10a'] = result = order.charge()
    tx_ref_num = result['TxRefNum']
    tx_ref_idx = result['TxRefIdx']
    reversal = Reversal(tx_ref_num=tx_ref_num,
                        tx_ref_idx='0',
                        amount='55.00',
                        order_id=order.order_id)
    results['10b'] = reversal.reversal()

    order = Order(message_type='AC',
                  cc_num='371449635398431',
                  order_id='211',
                  cc_expiry='1116',
                  zip_code='66666',
                  cvd='2222',
                  amount='75.00')
    results['11'] = order.charge()

    order = Order(message_type='AC',
                  cc_num='6011000995500000',
                  order_id='212',
                  cc_expiry='1116',
                  zip_code='77777',
                  amount='10.00')
    results['12'] = order.charge()

    order = Order(message_type='AC',
                  cc_num='6011000995500000',
                  order_id='213',
                  cc_expiry='1116',
                  zip_code='77777',
                  amount='15.00')
    results['13a'] = result = order.charge()
    tx_ref_num = result['TxRefNum']
    tx_ref_idx = result['TxRefIdx']
    reversal = Reversal(tx_ref_num=tx_ref_num,
                        tx_ref_idx='0',
                        amount='15.00',
                        order_id=order.order_id)
    results['13b'] = reversal.reversal()

    order = Order(message_type='AC',
                  cc_num='6011000995500000',
                  order_id='214',
                  cc_expiry='1116',
                  zip_code='L6L2X9',
                  cvd='444',
                  amount='63.03')
    results['14'] = result = order.charge()

    order = Order(message_type='AC',
                  cc_num='3566002020140006',
                  order_id='215',
                  cc_expiry='1116',
                  zip_code='33333',
                  amount='29.00')
    results['15'] = result = order.charge()

    return results

def section_d():
    """
    Return Transactions
    """
    results = collections.OrderedDict()
    results['section'] = 'd'

    order = Order(message_type='R',
                  cc_num='4788250000028291',
                  order_id='401',
                  cc_expiry='1116',
                  amount='12.00')
    results['1a'] = result = order.charge()
    tx_ref_num = result['TxRefNum']
    tx_ref_idx = result['TxRefIdx']
    reversal = Reversal(tx_ref_num=tx_ref_num,
                        tx_ref_idx='0',
                        amount='12.00',
                        order_id=order.order_id)
    results['1b'] = reversal.void()

    order = Order(message_type='R',
                  cc_num='5454545454545454',
                  order_id='402',
                  cc_expiry='1116',
                  amount='11.00')
    results['2'] = order.charge()

    order = Order(message_type='R',
                  cc_num='371449635398431',
                  order_id='403',
                  cc_expiry='1116',
                  amount='1055.00')
    results['3a'] = result = order.charge()
    tx_ref_num = result['TxRefNum']
    tx_ref_idx = result['TxRefIdx']
    reversal = Reversal(tx_ref_num=tx_ref_num,
                        tx_ref_idx='0',
                        amount='1055.00',
                        order_id=order.order_id)
    results['3b'] = reversal.void()

    order = Order(message_type='R',
                  cc_num='6011000995500000',
                  order_id='404',
                  cc_expiry='1116',
                  amount='10.00')
    results['4'] = order.charge()

    order = Order(message_type='R',
                  cc_num='3566002020140006',
                  order_id='405',
                  cc_expiry='1116',
                  amount='29.00')
    results['5'] = order.charge()

    order = Order(message_type='AC',
                  cc_num='4788250000028291',
                  order_id='406',
                  cc_expiry='1116',
                  amount='25.00')
    results['6a'] = result = order.charge()
    tx_ref_num = result['TxRefNum']
    order = Order(message_type='R',
                  tx_ref_num=tx_ref_num,
                  order_id=order.order_id,
                  amount='25.00')
    results['6b'] = order.charge()

    order = Order(message_type='AC',
                  cc_num='5454545454545454',
                  order_id='407',
                  cc_expiry='1116',
                  amount='26.00')
    results['7a'] = result = order.charge()
    tx_ref_num = result['TxRefNum']
    order = Order(message_type='R',
                  tx_ref_num=tx_ref_num,
                  order_id=order.order_id,
                  amount='26.00')
    results['7b'] = order.charge()

    return results

def section_e():
    """
    Force
    """
    results = collections.OrderedDict()
    results['section'] = 'e'

    order = Order(message_type='FC',
                  cc_num='4788250000028291',
                  order_id='501',
                  cc_expiry='1116',
                  prior_auth_id='654544',
                  amount='12.00')
    results['1'] = order.charge()

    order = Order(message_type='FC',
                  cc_num='5454545454545454',
                  order_id='502',
                  cc_expiry='1116',
                  prior_auth_id='15X92Z',
                  amount='11.00')
    results['2a'] = result = order.charge()
    tx_ref_num = result['TxRefNum']
    tx_ref_idx = result['TxRefIdx']
    reversal = Reversal(tx_ref_num=tx_ref_num,
                        tx_ref_idx='0',
                        amount='11.00',
                        order_id=order.order_id)
    results['2b'] = reversal.void()

    order = Order(message_type='FC',
                  cc_num='371449635398431',
                  order_id='503',
                  cc_expiry='1116',
                  prior_auth_id='198543',
                  amount='1055.00')
    results['3'] = order.charge()

    order = Order(message_type='FC',
                  cc_num='6011000995500000',
                  order_id='504',
                  cc_expiry='1116',
                  prior_auth_id='098756',
                  amount='10.00')
    results['4a'] = result = order.charge()
    tx_ref_num = result['TxRefNum']
    tx_ref_idx = result['TxRefIdx']
    reversal = Reversal(tx_ref_num=tx_ref_num,
                        tx_ref_idx='0',
                        amount='10.00',
                        order_id=order.order_id)
    results['4b'] = reversal.reversal()

    order = Order(message_type='FC',
                  cc_num='3566002020140006',
                  order_id='505',
                  cc_expiry='1116',
                  prior_auth_id='8B957Y',
                  amount='29.00')
    results['5'] = order.charge()

    return results

def section_f():
    """
    Retry Logic for Credit Cards
    """
    results = collections.OrderedDict()
    results['section'] = 'f'

    order = Order(message_type='AC',
                  cc_num='4788250000028291',
                  order_id='601',
                  cc_expiry='1116',
                  amount='10.00')
    results['1a'] = order.charge()
    trace_number = order.trace_number
    results['1a']['TraceNumber'] = trace_number
    order = Order(message_type='AC',
                  cc_num='4788250000028291',
                  order_id='601',
                  cc_expiry='1116',
                  trace_number=trace_number,
                  amount='10.00')
    results['1b'] = order.charge()
    trace_number = order.trace_number
    results['1b']['TraceNumber'] = trace_number

    order = Order(message_type='AC',
                  cc_num='5454545454545454',
                  order_id='602',
                  cc_expiry='1116',
                  amount='15.00')
    results['2a'] = order.charge()
    trace_number = order.trace_number
    results['2a']['TraceNumber'] = trace_number
    results['2b'] = order.charge()
    results['2b']['TraceNumber'] = trace_number

    order = Order(message_type='AC',
                  cc_num='371449635398431',
                  order_id='603',
                  cc_expiry='1116',
                  amount='20.00')
    results['3a'] = order.charge()
    trace_number = order.trace_number
    results['3a']['TraceNumber'] = trace_number
    results['3b'] = order.charge()
    results['3b']['TraceNumber'] = trace_number

    order = Order(message_type='AC',
                  cc_num='371449635398431',
                  order_id='603',
                  cc_expiry='1116',
                  amount='20.00')
    results['3a'] = order.charge()
    trace_number = order.trace_number
    results['3a']['TraceNumber'] = trace_number
    results['3b'] = order.charge()
    results['3b']['TraceNumber'] = trace_number

    order = Order(message_type='AC',
                  cc_num='6011000995500000',
                  order_id='604',
                  cc_expiry='1116',
                  amount='10.00')
    results['4a'] = order.charge()
    trace_number = order.trace_number
    results['4a']['TraceNumber'] = trace_number
    results['4b'] = order.charge()
    results['4b']['TraceNumber'] = trace_number

    order = Order(message_type='AC',
                  cc_num='3566002020140006',
                  order_id='605',
                  cc_expiry='1116',
                  amount='100.00')
    results['5a'] = order.charge()
    trace_number = order.trace_number
    results['5a']['TraceNumber'] = trace_number
    results['5b'] = order.charge()
    results['5b']['TraceNumber'] = trace_number

    return results

def section_g():
    """
    Customer Profiles
    """
    results = collections.OrderedDict()
    results['section'] = 'g'

    profile = Profile(name="Alice Testerson",
                      address1="100 N Broad St.",
                      address2="",
                      city="Philadelphia",
                      zip_code="19107",
                      email="alice@example.com",
                      cc_num="4788250000028291",
                      cc_expiry="1116")
    results['1a'] = result = profile.create()
    customer_num = result['CustomerRefNum']
    profile = Profile(ident=customer_num,
                      cc_num = "371449635398431")
    results['1b'] = profile.update()
    profile = Profile(ident=customer_num)
    results['1c'] = profile.read()
    order = Order(message_type='AC',
                  order_id='711',
                  customer_num=customer_num,
                  amount='45.00')
    results['1d'] = order.charge()
    order_id = order.order_id
    order = Order(message_type='R',
                  customer_num=customer_num,
                  order_id=order_id,
                  amount='45.00')
    results['1e'] = order.charge()
    profile = Profile(ident=customer_num)
    results['1f'] = profile.destroy()

    profile = Profile(name="Bob Testerson",
                      zip_code="19107",
                      cc_num="5454545454545454",
                      cc_expiry="1116")
    results['2a'] = result = profile.create()
    customer_num = result['CustomerRefNum']
    profile = Profile(ident=customer_num,
                      cc_num="6011000995500000",
                      address1="200 N Broad St",
                      address2="",
                      city="Philadelphia",
                      phone="12156862840")
    results['2b'] = profile.update()
    order = Order(message_type="A",
                  order_id="721",
                  customer_num=customer_num,
                  address1="2200 Market St",
                  address2="Apt 4",
                  zip_code="19103",
                  amount="25.00")
    results['2c'] = result = order.charge()
    tx_ref_num = result['TxRefNum']
    tx_ref_idx = result['TxRefIdx']
    reversal = Reversal(tx_ref_num=tx_ref_num,
                        tx_ref_idx='0',
                        amount="25.00",
                        order_id=order.order_id)
    results['2d'] = reversal.void()
    profile = Profile(ident=customer_num)
    results['2e'] = profile.destroy()

    order = Order(message_type="A",
                  order_id="751",
                  new_customer=True,
                  name="George Exampleton",
                  address1="500 Market St",
                  zip_code="19103",
                  cc_num="6011000995500000",
                  cc_expiry="1116",
                  amount="65.00")
    results['5a'] = result = order.charge()
    customer_num = result['CustomerRefNum']
    order = Order(message_type="A",
                  order_id="752",
                  customer_num=customer_num,
                  amount="65.00")
    results['5b'] = result = order.charge()
    tx_ref_num = result['TxRefNum']
    tx_ref_idx = result['TxRefIdx']
    reversal = Reversal(tx_ref_num=tx_ref_num,
                        tx_ref_idx='0',
                        order_id=order.order_id)
    results['5c'] = reversal.void()

    order = Order(message_type="AC",
                  order_id="761",
                  new_customer=True,
                  name="Wimla Exampleton",
                  address1="600 Market St",
                  zip_code="19103",
                  cc_num="5454545454545454",
                  cc_expiry="1116",
                  amount="40.00")
    results['7a'] = result = order.charge()
    customer_num = result['CustomerRefNum']
    order = Order(message_type="AC",
                  order_id="762",
                  customer_num=customer_num,
                  amount="40.00")
    results['7b'] = order.charge()
    order = Order(message_type="R",
                  order_id="762",
                  customer_num=customer_num,
                  amount="40.00")
    results['7c'] = order.charge()

    return results

def test_section(section):
    results = section()
    for key, result in results.items():
        print("result: %s" % result)
        print("parsed result: %s" % parse_result(key, result))

if __name__ == '__main__':
    test_sections = [
        section_a, 
        #section_b,
        #section_d,
        #section_e,
        #section_f,
        #section_g,
    ]
    for section in test_sections:
        test_section(section)
