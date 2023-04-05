import unittest
from decimal import Decimal
from xml.etree.ElementTree import tostring

from CAMT_053_001_09.base_models import AmountBaseModel
from CAMT_053_001_09.message_datatypes import ActiveOrHistoricCurrencyAnd13DecimalAmount, ActiveCurrencyCode


class TestAmountBaseModel(unittest.TestCase):

    def test_valid_currency(self):
        amount = AmountBaseModel(amount=100, ccy='USD')
        self.assertEqual(amount.ccy, 'USD')

    def test_invalid_currency(self):
        with self.assertRaises(ValueError):
            AmountBaseModel(amount=100, ccy='US')

    def test_default_decimal_places(self):
        amount = AmountBaseModel(amount=123.456, ccy='USD')
        self.assertEqual(amount.amount, Decimal('123.46'))

    def test_custom_decimal_places(self):
        amount = AmountBaseModel(amount=123.456, ccy='USD', decimal_places=4)
        self.assertEqual(amount.amount, Decimal('123.4560'))

    def test_zero_decimal_places(self):
        amount = AmountBaseModel(amount=123.456, ccy='JPY')
        self.assertEqual(amount.amount, Decimal('123'))

    def test_four_decimal_places(self):
        amount = AmountBaseModel(amount=123.456789, ccy='CLF')
        self.assertEqual(amount.amount, Decimal('123.4568'))

    def test_strip_leading_trailing_zeros(self):
        amount1 = AmountBaseModel(amount="00123.4500", ccy="USD", strip=True)
        assert amount1.amount == Decimal("123.45")

        amount2 = AmountBaseModel(amount="00010.0000", ccy="USD", strip=True)
        assert amount2.amount == Decimal("10")

        amount3 = AmountBaseModel(amount="00123.4500", ccy="USD")
        assert amount3.amount == Decimal("00123.4500")

        amount4 = AmountBaseModel(amount="00010.0000", ccy="USD")
        assert amount4.amount == Decimal("00010.0000")

    def test_to_xml(self):
        amount = AmountBaseModel(amount=123.45, ccy='USD')
        xml_element = amount.to_xml('Amount')
        xml_string = tostring(xml_element, encoding='unicode')

        expected_xml_string = '<Amount ccy="USD">123.45</Amount>'
        self.assertEqual(xml_string, expected_xml_string)


class TestActiveOrHistoricCurrencyAnd13DecimalAmount(unittest.TestCase):

    def test_valid_currency(self):
        amount = ActiveOrHistoricCurrencyAnd13DecimalAmount(amount=100, ccy='USD')
        self.assertEqual(amount.ccy, 'USD')

    def test_invalid_currency(self):
        with self.assertRaises(ValueError):
            ActiveOrHistoricCurrencyAnd13DecimalAmount(amount=100, ccy='US')

    def test_default_decimal_places(self):
        amount = ActiveOrHistoricCurrencyAnd13DecimalAmount(amount=123.456, ccy='USD')
        self.assertEqual(amount.amount, Decimal('123.4560000000000'))

    def test_custom_decimal_places(self):
        amount = ActiveOrHistoricCurrencyAnd13DecimalAmount(amount=123.456, ccy='USD', decimal_places=4)
        self.assertEqual(amount.amount, Decimal('123.4560'))

    def test_zero_decimal_places(self):
        amount = ActiveOrHistoricCurrencyAnd13DecimalAmount(amount=123.456, ccy='JPY')
        self.assertEqual(amount.amount, Decimal('123.4560000000000'))

    def test_four_decimal_places(self):
        amount = ActiveOrHistoricCurrencyAnd13DecimalAmount(amount=123.456789, ccy='CLF')
        self.assertEqual(amount.amount, Decimal('123.4567890000000'))

    def test_strip_leading_trailing_zeros(self):
        amount1 = ActiveOrHistoricCurrencyAnd13DecimalAmount(amount="00123.4500", ccy="USD", strip=True)
        assert amount1.amount == Decimal("123.45")

        amount2 = ActiveOrHistoricCurrencyAnd13DecimalAmount(amount="00010.0000", ccy="USD", strip=True)
        assert amount2.amount == Decimal("10")

        amount3 = ActiveOrHistoricCurrencyAnd13DecimalAmount(amount="00123.4500", ccy="USD")
        assert amount3.amount == Decimal("00123.4500")

        amount4 = ActiveOrHistoricCurrencyAnd13DecimalAmount(amount="00010.0000", ccy="USD")
        assert amount4.amount == Decimal("00010.0000")

    def test_to_xml(self):
        amount = ActiveOrHistoricCurrencyAnd13DecimalAmount(amount=123.45, ccy='USD')
        xml_element = amount.to_xml('Amount')
        xml_string = tostring(xml_element, encoding='unicode')

        expected_xml_string = '<Amount ccy="USD">123.4500000000000</Amount>'
        self.assertEqual(xml_string, expected_xml_string)


class TestCurrencyCodeBase(unittest.TestCase):

    def test_currency_code_base_validation(self):
        valid_code = ActiveCurrencyCode('USD')
        self.assertEqual(valid_code, 'USD')

        with self.assertRaises(ValueError):
            ActiveCurrencyCode('US')

        with self.assertRaises(ValueError):
            ActiveCurrencyCode('USDD')

        with self.assertRaises(ValueError):
            ActiveCurrencyCode('123')



if __name__ == '__main__':
    unittest.main()
