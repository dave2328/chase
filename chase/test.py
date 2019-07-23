import os
import unittest
from chase import Profile, Order, Reversal

merchant_id = os.environ.get('TEST_ORBITAL_MERCHANT_ID')
username = os.environ.get('TEST_ORBITAL_USERNAME')
password = os.environ.get('TEST_ORBITAL_PASSWORD')

def new_profile():
    profile = Profile(
        merchant_id=merchant_id,
        username=username,
        password=password
    )
    profile.name = "Test User"
    profile.address1 = "101 Main St."
    profile.address2 = "Apt. 4"
    profile.city = "New York"
    profile.state = "NY"
    profile.zipCode = "10012"
    profile.email = "test@example.com"
    profile.phone = "9089089080"
    profile.cc_num = "4788250000028291"
    profile.cc_expiry = "1122"
    return profile


def new_order():
    return Order(
        merchant_id=merchant_id,
        username=username,
        password=password
    )


def new_reversal():
    return Reversal(
        merchant_id=merchant_id,
        username=username,
        password=password
    )


class TestProfileFunctions(unittest.TestCase):

    def assert_default_fields(self, result):
        self.assertEqual(result['ProfileProcStatus'], '0')
        self.assertEqual(result['CustomerName'], 'Test User')
        self.assertEqual(result['CustomerAddress1'], '101 Main St.')
        self.assertEqual(result['CustomerAddress2'], 'Apt. 4')
        self.assertEqual(result['CustomerCity'], 'New York')
        self.assertEqual(result['CustomerState'], 'NY')
        self.assertEqual(result['CustomerZIP'], '10012')
        self.assertEqual(result['CustomerEmail'], 'test@example.com')
        self.assertEqual(result['CustomerPhone'], '9089089080')
        self.assertEqual(result['CCAccountNum'], '4788250000028291')
        self.assertEqual(result['CCExpireDate'], '1122')

    def test_lifecycle(self):
        # test profile creation
        profile = new_profile()
        result = profile.create()
        self.assert_default_fields(result)
        ident = result['CustomerRefNum']

        # test profile reading
        profile = new_profile()
        profile.ident = ident
        result = profile.read()
        self.assert_default_fields(result)

        # test profile updating
        profile = new_profile()
        profile.ident = ident
        profile.name = 'Example Customer'
        profile.city = 'Philadelphia'
        profile.state = 'PA'
        profile.zipCode = '19130'
        result = profile.update()
        self.assertEqual(result['ProfileProcStatus'], '0')
        self.assertEqual(result['CustomerRefNum'], ident)
        self.assertEqual(result['CustomerName'], 'Example Customer')
        self.assertEqual(result['CustomerCity'], 'Philadelphia')
        self.assertEqual(result['CustomerState'], 'PA')
        self.assertEqual(result['CustomerZIP'], '19130')
        result = profile.read()
        self.assertEqual(result['ProfileProcStatus'], '0')
        self.assertEqual(result['CustomerName'], 'Example Customer')
        self.assertEqual(result['CustomerAddress1'], '101 Main St.')
        self.assertEqual(result['CustomerAddress2'], 'Apt. 4')
        self.assertEqual(result['CustomerCity'], 'Philadelphia')
        self.assertEqual(result['CustomerState'], 'PA')
        self.assertEqual(result['CustomerZIP'], '19130')
        self.assertEqual(result['CustomerEmail'], 'test@example.com')
        self.assertEqual(result['CustomerPhone'], '9089089080')
        self.assertEqual(result['CCAccountNum'], '4788250000028291')
        self.assertEqual(result['CCExpireDate'], '1122')

        # test profile deletion
        profile = new_profile()
        profile.ident = ident
        result = profile.destroy()
        self.assertEqual(result['ProfileProcStatus'], '0')
        self.assertEqual(result['CustomerRefNum'], ident)

class TestOrderFunctions(unittest.TestCase):

    def test_profile_order(self):
        self.profile = new_profile()
        result = self.profile.create()
        customer_num = result['CustomerRefNum']
        order = new_order()
        order.customer_num = customer_num
        order.order_id = '100001'
        order.amount = '10.00'
        result = order.charge()
        self.assertEqual(result['ProfileProcStatus'], '0')
        txRefNum = result['TxRefNum']
        txRefIdx = result['TxRefIdx']
        self.assertTrue(txRefNum)
        self.assertTrue(txRefIdx)
        refund = new_reversal()
        refund.tx_ref_num = txRefNum
        refund.tx_ref_idx = txRefIdx
        refund.order_id = '100001'
        result = refund.void()
        self.assertEqual(result['ProcStatus'], '0')

    def test_cc_order(self):
        order = new_order()
        order.order_id = '100001'
        order.amount = '10.00'
        order.address1 = "101 Main St."
        order.address2 = "Apt. 4"
        order.city = "New York"
        order.state = "NY"
        order.zipCode = "10012"
        order.email = "test@example.com"
        order.phone = "9089089080"
        order.cc_num = "4788250000028291"
        order.cc_expiry = "1122"
        result = order.charge()
        txRefNum = result['TxRefNum']
        txRefIdx = result['TxRefIdx']
        self.assertTrue(txRefNum)
        self.assertTrue(txRefIdx)
        refund = new_reversal()
        refund.tx_ref_num = txRefNum
        refund.tx_ref_idx = txRefIdx
        refund.order_id = '100001'
        result = refund.void()
        self.assertEqual(result['ProcStatus'], '0')

if __name__ == '__main__':
    unittest.main()
