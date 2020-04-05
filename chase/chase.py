import os
from uuid import uuid4
import xml.etree.ElementTree as ET
import re
import unicodedata
from time import sleep

import requests

PROCSTATUS_INVALID_RETRY_TRACE = '9714'
PROCSTATUS_USER_NOT_FOUND = '9581'

CARD_TYPE_VISA = 'VISA'
CARD_TYPE_MC = 'MC'
CARD_TYPE_AMEX = 'Amex'
CARD_TYPE_DISCOVER = 'Discover'
CARD_TYPE_JCB = 'JCB'
CARD_TYPES = [
    CARD_TYPE_VISA,
    CARD_TYPE_MC,
    CARD_TYPE_AMEX,
    CARD_TYPE_DISCOVER,
    CARD_TYPE_JCB,
]

TEST_ENDPOINT_URL_1 = "https://orbitalvar1.chasepaymentech.com"
TEST_ENDPOINT_URL_2 = "https://orbitalvar2.chasepaymentech.com"
ENDPOINT_URL_1 = "https://orbital1.chasepaymentech.com"
ENDPOINT_URL_2 = "https://orbital2.chasepaymentech.com"

CURRENT_DTD_VERSION = "PTI68"

AUTH_PLATFORM_BIN = {
    'salem': '000001',
    'pns': '000002',
}

valid_credit_pattern = re.compile("""
    ^(?:4[0-9]{12}(?:[0-9]{3})?          # Visa
     |  5[1-5][0-9]{14}                  # MasterCard
     |  3[47][0-9]{13}                   # American Express
     |  3(?:0[0-5]|[68][0-9])[0-9]{11}   # Diners Club
     |  6(?:011|5[0-9]{2})[0-9]{12}      # Discover
     |  (?:2131|1800|35\d{3})\d{11}      # JCB
    )$
""", re.VERBOSE)


def remove_control_characters(s):
    """
    Remove unicode characters that will endanger xml parsing on Chase's end
    """
    ue = s.encode('unicode-escape', 'ignore').decode()
    return "".join(ch for ch in ue if unicodedata.category(ch)[0] != "C")


def sanitize_address_field(s):
    """
    Address fields hould not include any of the following characters:
    % | ^ \ /
    """
    chars = ["%", "|", "^", "\\", "/"]
    return "".join(ch for ch in s if ch not in chars)


def sanitize_phone_field(s):
    """
        Phone Number Format
        AAAEEENNNNXXXX, where
        AAA = Area Code
        EEE = Exchange
        NNNN = Number
        XXXX = Extension
    """
    chars = ["(", ")", "-", "."]
    return "".join(ch for ch in s if ch not in chars)


class Endpoint(object):
    def __init__(self, **kwargs):
        """
        Endpoint takes the following constructor params:
            merchant_id
            username
            password
            trace_number
            production
        """
        self.merchant_id = os.getenv('ORBITAL_MERCHANT_ID') or kwargs.get('merchant_id')
        self.username = os.getenv('ORBITAL_USERNAME') or kwargs.get('username')
        self.password = os.getenv('ORBITAL_PASSWORD') or kwargs.get('password')
        self.trace_number = kwargs.get('trace_number', str(uuid4().node))
        self.production = kwargs.get('production', False)
        if self.production:
            self.url = ENDPOINT_URL_1
            self.url2 = ENDPOINT_URL_2
        else:
            self.url = TEST_ENDPOINT_URL_1
            self.url2 = TEST_ENDPOINT_URL_2
        self.dtd_version = 'application/%s' % CURRENT_DTD_VERSION
        self.headers = {
            'MIME-Version': "1.1",
            'Content-type': self.dtd_version,
            'Content-transfer-encoding': "text",
            'Request-number': "1",
            'Document-type': "Request",
            'Trace-number': self.trace_number,
            'Interface-Version': "MooreBro 1.1.0",
            'MerchantID': str(self.merchant_id),
        }
        # there are 2 platform options defined in the orbital gateway chase
        # Salem - BIN 000001
        # PNS - BIN 000002
        self.platform = kwargs.pop('platform', 'pns')

    def get_platform_bin(self):
        try:
            return AUTH_PLATFORM_BIN[self.platform.lower()]

        except KeyError:
            raise KeyError('You have supplied an invalid platform identification,'
                           'you can choose `Salem` (Stratus) or `PNS`')

    def make_request(self, xml):
        result = None
        # try the first url endpoint, then if there's no success, go to the second
        for url in [self.url, self.url2]:
            for i in range(3):
                if result is not None and result.text is not None:
                    return result.text
                try:
                    result = requests.post(
                        url,
                        data=xml,
                        headers=self.headers)
                    if result is not None and result.text is not None:
                        return result.text
                except:
                    pass
                # sleep for 250 ms to avoid rate limiting
                sleep(0.25)
        return "Could not communicate with Chase"

    def convert_amount(self, amount):
        """
        Remove decimal, pad zeros for ints.
        45.25 -> 4525
        54 -> 5400
        """
        a = amount.split(".")
        if len(a) > 1:
            dec = a[1]
            if len(dec) == 1:
                dec = dec + "0"
            amount = a[0] + dec
        else:
            amount = amount + "00"
        return amount

    def card_type(self, cc_num):
        card = None
        try:
            if cc_num[0] == "4":
                card = "Visa"
            elif cc_num[0] == "5":
                card = "MC"
            elif cc_num[0] == "6":
                card = "Discover"
            elif cc_num[0:1] in ("34", "37"):
                card = "Amex"
            elif cc_num[0:3] in ("2131", "1800"):
                card = "JCB"
        except IndexError:
            card = None
        return card

    def parse_xml(self, xml_file_name, values, default_value=None):
        xml_file = os.path.join(os.path.dirname(__file__), xml_file_name)
        tree = ET.parse(xml_file)
        root = tree.getroot()
        values['OrbitalConnectionUsername'] = self.username
        values['OrbitalConnectionPassword'] = self.password
        values['BIN'] = self.get_platform_bin()
        values['CustomerBin'] = self.get_platform_bin()
        for key, value in values.items():
            elem = root.find(".//%s" % key)
            if elem is not None:
                elem.text = value or default_value
                if elem.text is not None:
                    elem.text = remove_control_characters(elem.text)
        return ET.tostring(root)

    def parse_result(self, result):
        root = ET.fromstring(result)
        resp_elem = root.getchildren()[0]
        values = {}
        for child_elem in resp_elem:
            values[child_elem.tag] = child_elem.text
        return values


class Profile(Endpoint):
    def __init__(self, **kwargs):
        super(Profile, self).__init__(**kwargs)
        self.ident = kwargs.get('ident')
        self.name = kwargs.get('name')
        self.address1 = kwargs.get('address1')
        self.address2 = kwargs.get('address2')
        self.city = kwargs.get('city')
        self.state = kwargs.get('state')
        self.zipCode = kwargs.get('zip_code')
        self.email = kwargs.get('email')
        self.phone = kwargs.get('phone')
        self.cc_num = kwargs.get('cc_num')
        self.cc_expiry = kwargs.get('cc_expiry')
        self.xml = None

    def sanitize(self):
        if self.name is not None:
            self.name = self.name[:30]
        if self.address1 is not None:
            address1 = sanitize_address_field(self.address1)
            self.address1 = address1[:30]
        if self.address2 is not None:
            address2 = sanitize_address_field(self.address2)
            self.address2 = address2[:30]
        if self.city is not None:
            city = sanitize_address_field(self.city)
            self.city = city[:20]
        if self.state is not None:
            state = sanitize_address_field(self.state)
            self.state = state[:2]
        if self.zipCode is not None:
            self.zipCode = self.zipCode[:5]
        if self.email is not None:
            self.email = self.email[:50]
        if self.phone is not None:
            phone = sanitize_phone_field(self.phone)
            self.phone = phone[:14]

    def parse_result(self, result):
        values = super(Profile, self).parse_result(result)
        for key in ['CustomerName', 'CustomerAddress1', 'CustomerAddress2',
                    'CustomerCity']:
            if key in values and values[key]:
                values[key] = values[key].title()
        return values

    def create(self):
        self.sanitize()
        values = {
            'CustomerMerchantID': self.merchant_id,
            'CustomerName': self.name,
            'CustomerAddress1': self.address1,
            'CustomerAddress2': self.address2,
            'CustomerCity': self.city,
            'CustomerState': self.state,
            'CustomerZIP': self.zipCode,
            'CustomerEmail': self.email,
            'CustomerPhone': self.phone,
            'CCAccountNum': self.cc_num,
            'CCExpireDate': self.cc_expiry,
        }
        if self.ident:
            values['CustomerProfileFromOrderInd'] = 'S'
            values['CustomerRefNum'] = self.ident
        self.xml = self.parse_xml(
            "profile_create.xml",
            values,
            default_value="")
        self.result = self.make_request(self.xml)
        return self.parse_result(self.result)

    def read(self):
        values = {
            'CustomerMerchantID': self.merchant_id,
            'CustomerRefNum': self.ident
        }
        self.xml = self.parse_xml("profile_read.xml", values)
        self._result = self.make_request(self.xml)
        return self.parse_result(self._result)

    def update(self):
        self.sanitize()
        values = {
            'CustomerMerchantID': self.merchant_id,
            'CustomerRefNum': self.ident,
            'CustomerName': self.name,
            'CustomerAddress1': self.address1,
            'CustomerAddress2': self.address2,
            'CustomerCity': self.city,
            'CustomerState': self.state,
            'CustomerZIP': self.zipCode,
            'CustomerEmail': self.email,
            'CustomerPhone': self.phone,
            'CCAccountNum': self.cc_num,
            'CCExpireDate': self.cc_expiry,
        }
        self.xml = self.parse_xml("profile_update.xml", values)
        self._result = self.make_request(self.xml)
        return self.parse_result(self._result)

    def destroy(self):
        values = {
            'CustomerMerchantID': self.merchant_id,
            'CustomerRefNum': self.ident,
        }
        self.xml = self.parse_xml("profile_destroy.xml", values)
        self._result = self.make_request(self.xml)
        return self.parse_result(self._result)


class Order(Endpoint):
    """
    MessageType
        A = Authorize
        AC = Authorize Capture
        FC = Force Capture
        R = Refund
    """

    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)
        self.message_type = kwargs.get('message_type')  # <MessageType>
        self.cc_num = kwargs.get('cc_num')  # <AccountNum>
        self.cc_expiry = kwargs.get('cc_expiry')  # <Exp>
        self.cvv_indicator = kwargs.get('cvv_indicator') or \
            kwargs.get('cvd_indicator')  # <CardSecValInd>
        self.cvv = kwargs.get('cvv') or kwargs.get('cvd')  # <CardSecVal>
        self.customer_num = kwargs.get('customer_num')  # <CustomerRefNum>
        self.order_id = kwargs.get('order_id')  # <OrderID>
        self.amount = kwargs.get('amount')  # <Amount>
        self.zipCode = kwargs.get('zip_code')  # <AVSzip>
        self.address1 = kwargs.get('address1')  # <AVSaddress1>
        self.address2 = kwargs.get('address2')  # <AVSaddress2>
        self.city = kwargs.get('city')  # <AVScity>
        self.state = kwargs.get('state')  # <AVSstate>
        self.phone = kwargs.get('phone')  # <AVSphoneNum>
        self.prior_auth_id = kwargs.get('prior_auth_id')  # <PriorAuthID>
        self.tx_ref_num = kwargs.get('tx_ref_num')  # <TxRefNum>
        self.new_customer = kwargs.get('new_customer', False)

    def sanitize(self):
        if self.address1 is not None:
            address1 = sanitize_address_field(self.address1)
            self.address1 = address1[:30]
        if self.address2 is not None:
            address2 = sanitize_address_field(self.address2)
            self.address2 = address2[:30]
        if self.city is not None:
            city = sanitize_address_field(self.city)
            self.city = city[:20]
        if self.state is not None:
            state = sanitize_address_field(self.state)
            self.state = state[:2]
        if self.zipCode is not None:
            self.zipCode = self.zipCode[:5]
        if self.phone is not None:
            phone = sanitize_phone_field(self.phone)
            self.phone = phone[:14]

    def card_sec_val_ind(self):
        """
        Card Security Presence Indicator
        For Discover/Visa
        1     Value is Present
        2     Value on card but illegible
        9     Cardholder states data not available
        Null if not Visa/Discover
        """
        if not self.cvv:
            return None
        if self.cvv_indicator:
            return self.cvv_indicator
        # Quick check for card type
        if self.card_type(self.cc_num) in ('Visa', 'Discover'):
            if self.cc_expiry and len(self.cc_expiry) > 0:
                return "1"
            else:
                return "9"
        return None

    def charge(self):
        self.sanitize()
        values = {
            'MerchantID': self.merchant_id,
            'MessageType': self.message_type or "AC",
            'AccountNum': self.cc_num,
            'Exp': self.cc_expiry,
            'CardSecValInd': self.card_sec_val_ind(),
            'CardSecVal': self.cvv,
            'OrderID': self.order_id,
            'Amount': self.convert_amount(self.amount),
            'CustomerRefNum': self.customer_num,
            'AVSzip': self.zipCode,
            'AVSaddress1': self.address1,
            'AVSaddress2': self.address2,
            'AVScity': self.city,
            'AVSstate': self.state,
            'AVSphoneNum': self.phone,
            'PriorAuthID': self.prior_auth_id,
            'TxRefNum': self.tx_ref_num,
        }
        if self.new_customer:
            values['CustomerProfileFromOrderInd'] = "A"
            values['CustomerProfileOrderOverrideInd'] = "NO"

        # Validation, TBD
        if self.message_type not in ['A', 'AC', 'FC', 'R']:
            pass

        self.xml = self.parse_xml("order_new.xml", values)
        self._result = self.make_request(self.xml)
        return self.parse_result(self._result)

    def authorize(self):
        self.message_type = 'A'
        return self.charge()

    def authorize_capture(self):
        self.message_type = 'AC'
        return self.charge()

    def force_capture(self):
        self.message_type = 'FC'
        return self.charge()

    def refund(self):
        self.message_type = 'R'
        return self.charge()


class MarkForCapture(Endpoint):
    def __init__(self, **kwargs):
        super(MarkForCapture, self).__init__(**kwargs)
        self.order_id = kwargs.get('order_id')  # <OrderID>
        self.amount = kwargs.get('amount')  # <Amount>
        self.tx_ref_num = kwargs.get('tx_ref_num')  # <TxRefNum>

    def request(self):
        values = {
            'MerchantID': self.merchant_id,
            'OrderID': self.order_id,
            'Amount': self.convert_amount(self.amount),
            'TxRefNum': self.tx_ref_num,
        }
        self.xml = self.parse_xml("mark_for_capture.xml", values)
        self._result = self.make_request(self.xml)
        return self.parse_result(self._result)


class Reversal(Endpoint):
    def __init__(self, **kwargs):
        super(Reversal, self).__init__(**kwargs)
        self.tx_ref_num = kwargs.get('tx_ref_num')  # <TxRefNum>
        self.tx_ref_idx = kwargs.get('tx_ref_idx')  # <TxRefIdx>
        self.amount = kwargs.get('amount')  # <AdjustedAmt>
        self.order_id = kwargs.get('order_id')  # <OrderID>
        # <OnlineReversalInd>
        self.online_reversal_ind = kwargs.get('online_reversal_ind')

    def reversal(self):
        self.online_reversal_ind = "Y"
        values = {
            'MerchantID': self.merchant_id,
            'TxRefNum': self.tx_ref_num,
            'TxRefIdx': self.tx_ref_idx,
            'OrderID': self.order_id,
            'OnlineReversalInd': self.online_reversal_ind,
        }
        if self.amount:
            values['AdjustedAmt'] = self.convert_amount(self.amount)
        self.xml = self.parse_xml("reversal.xml", values)
        self._result = self.make_request(self.xml)
        return self.parse_result(self._result)

    def void(self):
        values = {
            'MerchantID': self.merchant_id,
            'TxRefNum': self.tx_ref_num,
            'TxRefIdx': self.tx_ref_idx,
            'OrderID': self.order_id,
        }
        if self.amount:
            values['AdjustedAmt'] = self.convert_amount(self.amount)
        self.xml = self.parse_xml("reversal.xml", values)
        self._result = self.make_request(self.xml)
        return self.parse_result(self._result)
