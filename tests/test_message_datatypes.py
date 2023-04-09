import unittest
from datetime import datetime, timezone
from decimal import Decimal
from xml.etree.ElementTree import tostring

import pendulum

from CAMT_053_001_09.base_models import AmountBaseModel, DateTimeBaseModel
from CAMT_053_001_09.message_datatypes import ActiveOrHistoricCurrencyAnd13DecimalAmount, ActiveCurrencyCode, \
    AddressType2Code, CountryCode, ExternalAccountIdentification1Code
from CAMT_053_001_09.utils import set_datetime_format_decorator


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


class TestAddressType2Code(unittest.TestCase):
    def test_valid_codes(self):
        valid_codes = ['ADDR', 'PBOX', 'HOME', 'BIZZ', 'MLTO', 'DLVY']
        for code in valid_codes:
            with self.subTest(code=code):
                try:
                    AddressType2Code(code=code)
                except Exception as e:
                    self.fail(f"Valid code '{code}' raised an exception: {e}")

    def test_invalid_codes(self):
        invalid_codes = ['INVALID', '12', '']
        for code in invalid_codes:
            with self.subTest(code=code):
                with self.assertRaises(ValueError):
                    AddressType2Code(code=code)


class TestCountryCode(unittest.TestCase):
    def test_valid_country_codes(self):
        valid_codes = ['US', 'GB', 'DE', 'FR', 'JP', 'CN', 'BR', 'IN']

        for code in valid_codes:
            with self.subTest(code=code):
                try:
                    country_code = CountryCode(value=code)
                    self.assertEqual(country_code.value, code)
                except ValueError:
                    self.fail(f'ValueError raised for valid code: {code}')

    def test_invalid_country_codes(self):
        invalid_codes = ['USA', '1A', 'A1']

        for code in invalid_codes:
            with self.subTest(code=code):
                with self.assertRaises(ValueError):
                    country_code = CountryCode(value=code)
                    self.fail(f'ValueError not raised for {code}. CountryCode instance: {country_code}')


class TestExternalAccountIdentification1Code(unittest.TestCase):
    def test_valid_codes(self):
        valid_codes = {'AIIN', 'BBAN', 'CUID', 'UPIC'}

        for code in valid_codes:
            with self.subTest(code=code):
                ext_code = ExternalAccountIdentification1Code(code=code)
                self.assertEqual(ext_code.code, code)

    def test_invalid_codes(self):
        invalid_codes = ['ABCD', '1234', 'AI', 'UP']

        for code in invalid_codes:
            with self.subTest(code=code):
                with self.assertRaises(ValueError):
                    ExternalAccountIdentification1Code(code=code)


class TestDateTimeBaseModel(unittest.TestCase):
    local_tz = pendulum.local_timezone()
    offset_hours = local_tz.utcoffset(pendulum.now()).total_seconds() // 3600

    valid_inputs = {
        'YYYY': [
            (datetime(2018, 3, 6, 12, 00), '2018'),
            ('1920', '1920'),
            ('2018-01-01T00:00:00+01:00', '2018'),
            ('2019-01-01T00:00:00Z', '2019'),
            ('2020-01-01', '2020'),
            ('2021-01', '2021'),
            ('2022', '2022'),
        ],
        'YYYY-MM': [
            (datetime(2018, 3, 6, 12, 00), '2018-03'),
            ('2019-01-01T00:00:00+01:00', '2019-01'),
            ('2020-01-01T00:00:00Z', '2020-01'),
            ('2021-01-03', '2021-01'),
            ('2022-03', '2022-03'),
        ],
        'YYYY-MM-DD': [
            (datetime(2018, 3, 6, 12, 00), '2018-03-06'),
            ('2018-01-01T00:00:00', '2018-01-01'),
            ('2018-01-01T00:00:00Z', '2018-01-01'),
            ('2019-01-01T00:00:00+01:00', '2019-01-01'),
            ('2022-04-01', '2022-04-01'),
        ],
        'YYYY-MM-DDThh:mm:ss.sssZ': [
            (datetime(2023, 4, 6, 12, 34, 56, 789000), '2023-04-06T10:34:56.789Z'),
            (datetime(2023, 4, 6, 12, 34, 56, 789000, tzinfo=timezone.utc), '2023-04-06T12:34:56.789Z'),
            ('2023-04-06T12:34:56.789Z', '2023-04-06T12:34:56.789Z'),
            ('2019-11-25T23:59:59.999-05:00', '2019-11-26T04:59:59.999Z'),
            ('2019-11-25T23:59:59.999', '2019-11-25T22:59:59.999Z'),
            ('2023-04-06 23:59:59Z', '2023-04-06T23:59:59.000Z'),
        ],
        'YYYY-MM-DDThh:mm:ss.sss+/-hh:mm': [
            (datetime(2023, 4, 6, 12, 34, 56, 789000), '2023-04-06T12:34:56.789+02:00'),
            (datetime(2023, 4, 6, 12, 34, 56, 789000, tzinfo=timezone.utc), '2023-04-06T12:34:56.789+00:00'),
            ('2023-04-06T12:34:56.789Z', '2023-04-06T12:34:56.789+00:00'),
            ('2019-11-25T23:59:59.999-05:00', '2019-11-25T23:59:59.999-05:00'),
            ('2019-11-25T23:59:59.999', '2019-11-25T23:59:59.999+01:00'),
            ('2023-04-06 23:59:59Z', '2023-04-06T23:59:59.000+00:00'),
        ],
        'YYYY-MM-DDThh:mm:ss.sss': [
            (datetime(2023, 4, 6, 12, 34, 56, 789000), '2023-04-06T12:34:56.789'),
            (datetime(2023, 4, 6, 12, 34, 56, 789000, tzinfo=timezone.utc), '2023-04-06T14:34:56.789'),
            ('2023-04-06T12:34:56.789Z', '2023-04-06T14:34:56.789'),
            ('2019-11-25T23:59:59.999-05:00', '2019-11-26T05:59:59.999'),
            ('2019-11-25T23:59:59.999', '2019-11-25T23:59:59.999'),
            ('2023-04-06 23:59:59Z', '2023-04-07T01:59:59.000')
        ],
        'hh:mm:ss.sssZ': [
            (datetime(2023, 4, 6, 12, 34, 56, 789000), '10:34:56.789Z'),
            (datetime(2023, 4, 6, 12, 34, 56, 789000, tzinfo=timezone.utc), '12:34:56.789Z'),
            ('12:34:56.789Z', '12:34:56.789Z'),
            ('2019-11-25T23:59:59.999-05:00', '04:59:59.999Z'),
            ('2019-11-25T23:59:59.999', '22:59:59.999Z'),
            ('23:59:59Z', '23:59:59.000Z')
        ],
        'hh:mm:ss.sss+/-hh:mm': [
            (datetime(2023, 4, 6, 12, 34, 56, 789000), '12:34:56.789+02:00'),
            (datetime(2023, 4, 6, 12, 34, 56, 789000, tzinfo=timezone.utc), '12:34:56.789+00:00'),
            ('12:34:56.789Z', '12:34:56.789+00:00'),
            ('2019-11-25T23:59:59.999-05:00', '23:59:59.999-05:00'),
            ('2019-11-25T23:59:59.999', '23:59:59.999+01:00'),
            ('23:59:59Z', '23:59:59.000+00:00')
        ],
        'hh:mm:ss.sss': [
            (datetime(2023, 4, 6, 12, 34, 56, 789000), '12:34:56.789'),
            (datetime(2023, 4, 6, 12, 34, 56, 789000, tzinfo=timezone.utc), '14:34:56.789'),
            ('12:34:56.789Z', '14:34:56.789'),
            ('2019-11-25T23:59:59.999-05:00', '05:59:59.999'),
            ('2019-11-25T23:59:59.999', '23:59:59.999'),
            ('23:59:59Z', '01:59:59.000')
        ],
    }

    invalid_inputs = {
        'YYYY': ['20', '00', 'invalid'],
        'YYYY-MM': ['22', '22-3', '2018', '2022-00', '2022-13', 'invalid'],
        'YYYY-MM-DD': ['22-1-1', '2022-13-01', '2022-01-32', 'invalid'],
        'YYYY-MM-DDThh:mm:ss.sssZ': ['2022-04-07', 'invalid'],
        'YYYY-MM-DDThh:mm:ss.sss+/-hh:mm': ['2022-04-07', 'invalid'],
        'YYYY-MM-DDThh:mm:ss.sss': ['2022-04-07', 'invalid'],
        'hh:mm:ss.sssZ': ['2022-04-07', 'invalid'],
        'hh:mm:ss.sss+/-hh:mm': ['2022-04-07', 'invalid'],
        'hh:mm:ss.sss': ['2022-04-07', 'invalid']
    }

    def test_year_model(self):
        format_str = 'YYYY'

        @set_datetime_format_decorator(format_str)
        class YearModel(DateTimeBaseModel):
            pass

        for valid_input, valid_output in self.valid_inputs[format_str]:
            with self.subTest(valid_input=valid_input):
                year_model = YearModel(value=valid_input)
                self.assertEqual(year_model.value, valid_output)

        for invalid_input in self.invalid_inputs[format_str]:
            with self.subTest(invalid_input=invalid_input):
                with self.assertRaises(ValueError):
                    YearModel(value=invalid_input)

    def test_year_month_model(self):
        format_str = 'YYYY-MM'

        @set_datetime_format_decorator(format_str)
        class YearMonthModel(DateTimeBaseModel):
            pass

        for valid_input, valid_output in self.valid_inputs[format_str]:
            with self.subTest(valid_input=valid_input):
                year_month_model = YearMonthModel(value=valid_input)
                self.assertEqual(year_month_model.value, valid_output)

        for invalid_input in self.invalid_inputs[format_str]:
            with self.subTest(invalid_input=invalid_input):
                with self.assertRaises(ValueError):
                    YearMonthModel(value=invalid_input)

    def test_date_model(self):
        format_str = 'YYYY-MM-DD'

        @set_datetime_format_decorator(format_str)
        class DateModel(DateTimeBaseModel):
            pass

        for valid_input, valid_output in self.valid_inputs[format_str]:
            with self.subTest(valid_input=valid_input):
                date_model = DateModel(value=valid_input)
                self.assertEqual(date_model.value, valid_output)

        for invalid_input in sorted(self.invalid_inputs[format_str]):
            with self.subTest(invalid_input=invalid_input):
                with self.assertRaises(ValueError):
                    DateModel(value=invalid_input)

    def test_time_model(self):
        format_strings = {
            'hh:mm:ss.sssZ',
            'hh:mm:ss.sss+/-hh:mm',
            'hh:mm:ss.sss'
        }

        for format_str in format_strings:
            with self.subTest(format_str=format_str):
                @set_datetime_format_decorator(format_str)
                class TimeModel(DateTimeBaseModel):
                    pass

                for valid_input, valid_output in self.valid_inputs[format_str]:
                    with self.subTest(valid_input=valid_input):
                        time_model = TimeModel(value=valid_input)
                        self.assertEqual(time_model.value, valid_output)

                for invalid_input in self.invalid_inputs[format_str]:
                    with self.subTest(invalid_input=invalid_input):
                        with self.assertRaises(ValueError):
                            TimeModel(value=invalid_input)

    def test_datetime_model(self):
        format_strings = {
            'YYYY-MM-DDThh:mm:ss.sssZ',
            'YYYY-MM-DDThh:mm:ss.sss+/-hh:mm',
            'YYYY-MM-DDThh:mm:ss.sss'
        }

        for format_str in format_strings:
            with self.subTest(format_str=format_str):
                @set_datetime_format_decorator(format_str)
                class DateTimeModel(DateTimeBaseModel):
                    pass

                for valid_input, valid_output in self.valid_inputs[format_str]:
                    with self.subTest(valid_input=valid_input):
                        date_time_model = DateTimeModel(value=valid_input)
                        self.assertEqual(date_time_model.value, valid_output)

                for invalid_input in self.invalid_inputs[format_str]:
                    with self.subTest(invalid_input=invalid_input):
                        with self.assertRaises(ValueError):
                            DateTimeModel(value=invalid_input)


if __name__ == '__main__':
    unittest.main()
