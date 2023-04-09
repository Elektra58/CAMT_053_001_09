import re
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, ClassVar, Set

import pendulum
from lxml.etree import Element
from pydantic import BaseModel, validator, root_validator, condecimal

from config import settings


class AmountBaseModel(BaseModel):
    amount: condecimal(max_digits=18) | float
    ccy: str
    decimal_places: Optional[int] = None
    strip: Optional[bool] = False

    class Config:
        validate_assignment = True

    @validator('ccy', always=True)
    def validate_ccy(cls, v):
        pattern = re.compile(r'[A-Z]{3}')
        if isinstance(v, str) and pattern.fullmatch(v):
            return v
        raise ValueError('Invalid currency code. Must be a 3-letter uppercase code.')

    @root_validator
    def validate_and_quantize_amount(cls, values):
        amount = values.get('amount')
        ccy = values.get('ccy')
        decimal_places = values.get('decimal_places')
        strip = values.get('strip')

        if amount is not None:
            if isinstance(amount, float):
                amount = Decimal(str(amount))
            if isinstance(amount, str):
                amount = Decimal(amount)

            if decimal_places is None:
                if ccy in {'CLF', 'UYW'}:
                    decimal_places = 4
                elif ccy in {'BHD', 'IQD', 'JOD', 'KWD', 'LYD', 'OMR', 'TND'}:
                    decimal_places = 3
                elif ccy in {'JPY', 'KRW', 'PYG'}:
                    decimal_places = 0
                else:
                    decimal_places = 2  # Default to 2 decimal places

            values['amount'] = amount.quantize(Decimal(f'1E-{decimal_places}'), rounding=ROUND_HALF_UP)

            if strip:
                values['amount'] = values['amount'].normalize()

        return values

    def to_xml(self, tag: str) -> Element:
        element = Element(tag, ccy=self.ccy)
        element.text = str(self.amount)
        return element


class CurrencyCodeBaseModel(str):
    def __new__(cls, ccy):
        pattern = re.compile(r'[A-Z]{3}')
        if not isinstance(ccy, str):
            raise TypeError(f'{cls.__class__.__name__} must be a string')
        if not pattern.fullmatch(ccy):
            raise ValueError(f'{cls.__class__.__name__} must be a 3-letter uppercase alphabetic code')
        return super().__new__(cls, ccy)


class CodeStrBaseModel(BaseModel):
    code: str

    _valid_codes = set()

    @classmethod
    def set_valid_codes(cls, codes):
        cls._valid_codes = codes

    @validator('code', pre=True)
    def validate_code(cls, v):
        if not isinstance(v, str):
            raise TypeError(f'{cls.__class__.__name__} must be a string')

        v = v.strip().upper()

        if v not in cls._valid_codes:
            raise ValueError(
                f'Invalid {cls.__class__.__name__}: `{v}`, allowed values are {", ".join(cls._valid_codes)}')

        return v


class CodeRegexBaseModel(BaseModel):
    value: str
    _regex: ClassVar[str] = ''

    @validator('value')
    def validate_code(cls, value):
        if not re.match(cls._regex, value):
            raise ValueError(f'Invalid code: {value}')
        return value


class ExternalCodeStrBaseModel(BaseModel):
    code: str

    _valid_codes: Set[str] = set()
    _regex: ClassVar[str] = ''

    @classmethod
    def set_valid_codes(cls, codes: Set[str]) -> None:
        cls._valid_codes = codes

    @classmethod
    def set_regex(cls, regex: str) -> None:
        cls._regex = regex

    @validator('code', pre=True)
    def validate_code(cls, v: str) -> str:
        if not isinstance(v, str):
            raise TypeError(f'{cls.__class__.__name__} code must be a string')

        v = v.strip().upper()

        if v not in cls._valid_codes:
            raise ValueError(
                f'Invalid {cls.__class__.__name__} code: `{v}`, allowed values are {", ".join(cls._valid_codes)}')

        return v


class DateTimeBaseModel(BaseModel):
    """
    Base model for datetime fields.
    :param value: str or datetime value. If str, it will be parsed internally into a timezone aware datetime using
    pendulum. A naive datetime object will always be considered local time and converted according to the format
    string

    """
    value: str | datetime | date | pendulum.DateTime
    _original_value: str | datetime | date | pendulum.DateTime

    _datetime_format: ClassVar[str] = ''
    _local_tz: ClassVar[pendulum.timezone] = pendulum.local_timezone()
    _offset_hours = _local_tz.utcoffset(pendulum.now()).total_seconds() // 3600

    @validator('value')
    def validate_datetime(cls, value):
        original_type = type(value).__name__
        # store original value for error messages, convert to str if datetime
        cls._original_value = (
            value
            if isinstance(value, str)
            else value.isoformat()
        )

        # convert date or datetime to pendulum.DateTime
        if isinstance(value, datetime):
            value = pendulum.instance(value)

        elif isinstance(value, str):
            # remove UTC timezone info if present. Pendulum parses to UTC by default
            value = value.replace('Z', '')

            try:
                value = pendulum.parse(value)
            except ValueError as e:
                raise ValueError(f'Invalid datetime: {cls._original_value}') from e

        return value

    @classmethod
    def set_datetime_format(cls, datetime_format: str):
        cls._datetime_format = datetime_format

    @validator('value')
    def format_datetime(cls, value):
        def validate_date(regex: str):
            if not re.search(regex, cls._original_value):
                raise ValueError(f'Missing or incomplete date information in {cls._original_value}')

        def validate_time(regex: str = r'\d{2}:\d{2}:\d{2}'):
            if not re.search(regex, cls._original_value):
                raise ValueError(f'Missing or incomplete time information in {cls._original_value}')

        def has_timezone(regex: str = r'[+-]\d{2}:\d{2}$|[Z]$'):
            return re.search(r'[+-]\d{2}:\d{2}$|[Z]$', cls._original_value)

        match cls._datetime_format:
            case 'YYYY':
                validate_date(r'^\d{4}')
                value = value.format('YYYY')
            case 'YYYY-MM':
                validate_date(r'^\d{4}-\d{2}')
                value = value.format('YYYY-MM')
            case 'YYYY-MM-DD':
                validate_date(r'^\d{4}-\d{2}-\d{2}')
                value = value.format('YYYY-MM-DD')
            case 'YYYY-MM-DDThh:mm:ss.sssZ':
                validate_date(r'^\d{4}-\d{2}-\d{2}')
                validate_time()
                value = (
                    value.in_timezone('utc')
                    if has_timezone()
                    else value.replace(tzinfo=settings.DateTime.naive).in_timezone('utc')
                )
                value = value.format('YYYY-MM-DDTHH:mm:ss.SSSZ').replace('+00:00', 'Z')
            case 'YYYY-MM-DDThh:mm:ss.sss+/-hh:mm':
                validate_date(r'^\d{4}-\d{2}-\d{2}')
                validate_time()
                value = (
                    value
                    if has_timezone()
                    else value.replace(tzinfo=settings.DateTime.naive)
                )
                value = value.format('YYYY-MM-DDTHH:mm:ss.SSSZ')
            case 'YYYY-MM-DDThh:mm:ss.sss':
                validate_date(r'^\d{4}-\d{2}-\d{2}')
                validate_time()
                value = (
                    value.in_timezone(settings.DateTime.naive)
                    if has_timezone()
                    else value.replace(tzinfo=settings.DateTime.naive)
                )
                value = value.format('YYYY-MM-DDTHH:mm:ss.SSS')
            case 'hh:mm:ss.sssZ':
                validate_time()
                value = (
                    value.in_timezone('utc')
                    if has_timezone()
                    else value.replace(tzinfo=settings.DateTime.naive).in_timezone('utc')
                )
                value = value.format('HH:mm:ss.SSSZ').replace('+00:00', 'Z')
            case 'hh:mm:ss.sss+/-hh:mm':
                validate_time()
                value = (
                    value
                    if has_timezone()
                    else value.replace(tzinfo=settings.DateTime.naive).in_timezone('local')
                )
                value = value.format('HH:mm:ss.SSSZ')
            case 'hh:mm:ss.sss':
                validate_time()
                value = (
                    value.in_timezone(settings.DateTime.naive)
                    if has_timezone()
                    else value.replace(tzinfo=settings.DateTime.naive)
                )
                value = value.format('HH:mm:ss.SSS')
            case _:
                raise ValueError(
                    f'Unimplemented datetime format: {cls._datetime_format}'
                )

        return value

    @property
    def original_value(self):
        return self._original_value
