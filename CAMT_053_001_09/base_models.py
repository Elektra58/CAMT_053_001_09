import re
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

from lxml.etree import Element
from pydantic import BaseModel, validator, root_validator, condecimal


class AmountBaseModel(BaseModel):
    amount: condecimal(max_digits=18) | float
    ccy: str
    decimal_places: Optional[int] = None
    strip: Optional[bool] = False

    class Config:
        validate_assignment = True

    @validator("ccy", always=True)
    def validate_ccy(cls, v):
        pattern = re.compile(r'[A-Z]{3}')
        if isinstance(v, str) and pattern.fullmatch(v):
            return v
        raise ValueError("Invalid currency code. Must be a 3-letter uppercase code.")

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
            raise TypeError(f'{cls.__name__} must be a string')
        if not pattern.fullmatch(ccy):
            raise ValueError(f'{cls.__name__} must be a 3-letter uppercase alphabetic code')
        return super().__new__(cls, ccy)
