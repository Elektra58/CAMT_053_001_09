from CAMT_053_001_09.base_models import AmountBaseModel, CurrencyCodeBaseModel


# 6.2.1 Amount

class ActiveCurrencyAndAmount(AmountBaseModel):
    """
    A number of monetary units specified in an active currency where the unit of currency is explicit and compliant
    with ISO 4217.
    """
    pass


class ActiveOrHistoricCurrencyAnd13DecimalAmount(AmountBaseModel):
    """
    A number of monetary units specified in an active or a historic currency where the unit of currency is explicit
    and compliant with ISO 4217. The number of fractional digits (or minor unit of currency) is not checked as per
    ISO 4217: It must be lesser than or equal to 13.
    """

    def __init__(self, *args, **kwargs):
        # Set the default decimal_places for ActiveOrHistoricCurrencyAnd13DecimalAmount instances
        default_decimal_places = 13
        kwargs['decimal_places'] = kwargs.get('decimal_places', default_decimal_places)
        super().__init__(**kwargs)


class ActiveOrHistoricCurrencyAndAmount(AmountBaseModel):
    """
    A number of monetary units specified in an active or a historic currency where the unit of currency is explicit
    and compliant with ISO 4217.
    """
    pass


class ImpliedCurrencyAndAmount(AmountBaseModel):
    """
    Number of monetary units specified in a currency where the unit of currency is implied by the context and
    compliant with ISO 4217. The decimal separator is a dot.
    """
    pass


# 6.2.2 CodeSet
class ActiveCurrencyCode(CurrencyCodeBaseModel):
    """
    A code allocated to a currency by a Maintenance Agency under an international identification scheme as
    described in the latest edition of the international standard ISO 4217 "Codes for the representation of
    currencies and funds".
    """
    pass


class ActiveOrHistoricCurrencyCode(CurrencyCodeBaseModel):
    """
    A code allocated to a currency by a Maintenance Agency under an international identification scheme, as
    described in the latest edition of the international standard ISO 4217 "Codes for the representation of
    currencies and funds".
    """
    pass
