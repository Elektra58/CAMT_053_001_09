from CAMT_053_001_09.base_models import AmountBaseModel, CurrencyCodeBaseModel, CodeStrBaseModel, CodeRegexBaseModel, \
    DateTimeBaseModel, ExternalCodeStrBaseModel
from CAMT_053_001_09.utils import set_valid_codes_decorator, set_regex_decorator, set_external_code_set_decorator, \
    set_datetime_format_decorator
from pydantic import StrictBool, condecimal
from decimal import Decimal


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


@set_valid_codes_decorator({'ADDR', 'PBOX', 'HOME', 'BIZZ', 'MLTO', 'DLVY'})
class AddressType2Code(CodeStrBaseModel):
    """
    Specifies the type of address.
    """
    pass


@set_valid_codes_decorator({'ATTD', 'SATT', 'UATT'})
class AttendanceContext1Code(CodeStrBaseModel):
    """
    Human attendance at the POI location during the transaction.
    """
    pass


@set_valid_codes_decorator({'ICCD', 'AGNT', 'MERC'})
class AuthenticationEntity1Code(CodeStrBaseModel):
    """
    Entity or object in charge of verifying the cardholder authenticity.
    """
    pass


@set_valid_codes_decorator({'UKNW', 'BYPS', 'NPIN', 'FPIN', 'CPSG', 'PPSG', 'MANU', 'MERC', 'SCRT', 'SNCT', 'SCNL'})
class AuthenticationMethod1Code(CodeStrBaseModel):
    """
    Method used to verify the cardholder.
    """
    pass


@set_valid_codes_decorator({'TAGC', 'PHYS', 'BRCD', 'MGST', 'CICC', 'DFLE', 'CTLS', 'ECTL'})
class CardDataReading1Code(CodeStrBaseModel):
    """
    Type of reading of the card data.
    """
    pass


@set_valid_codes_decorator(
    {'MNSG', 'NPIN', 'FCPN', 'FEPN', 'FDSG', 'FBIO', 'MNVR', 'FBIG', 'APKI', 'PKIS', 'CHDT', 'SCEC'})
class CardholderVerificationCapability1Code(CodeStrBaseModel):
    """
    Cardholder verification capabilities of the POI (Personal Identification Number) performing the transaction.
    """
    pass


@set_valid_codes_decorator({'AGGR', 'DCCV', 'GRTT', 'INSP', 'LOYT', 'NRES', 'PUCO', 'RECP', 'SOAF', 'UNAF', 'VCAU'})
class CardPaymentServiceType2Code(CodeStrBaseModel):
    """
    Service provided by the card payment transaction, in addition to the main service.
    """
    pass


@set_valid_codes_decorator({'DEBT', 'CRED', 'SHAR', 'SLEV'})
class ChargeBearerType1Code(CodeStrBaseModel):
    """
    Specifies which party(ies) will pay charges due for processing of the instruction.
    """
    pass


@set_valid_codes_decorator({'CODU', 'COPY', 'DUPL'})
class CopyDuplicate1Code(CodeStrBaseModel):
    """
    Specifies if this document is a copy, a duplicate, or a duplicate of a copy.
    """
    pass


@set_regex_decorator(r'^[A-Z]{2}$')
class CountryCode(CodeRegexBaseModel):
    """
    Code to identify a country, a dependency, or another area of particular geopolitical interest, on the basis of
    country names obtained from the United Nations (ISO 3166, Alpha-2 code).
    """
    # TODO: check against ISO 3166-1 alpha-2
    pass


@set_valid_codes_decorator({'CRDT', 'DBIT'})
class CreditDebitCode(CodeStrBaseModel):
    """
    Specifies if an operation is an increase or a decrease.
    """
    pass


@set_valid_codes_decorator({'PRST', 'BYPS', 'UNRD', 'NCSC'})
class CSCManagement1Code(CodeStrBaseModel):
    """
    CSC (Card Security Code) management associated with the transaction.
    """
    pass


@set_valid_codes_decorator({'RADM', 'RPIN', 'FXDR', 'DISP', 'PUOR', 'SCOR'})
class DocumentType3Code(CodeStrBaseModel):
    """
    Specifies the type of document.
    """
    pass


@set_valid_codes_decorator(
    {'MSIN', 'CNFA', 'DNFA', 'CINV', 'CREN', 'DEBN', 'HIRI', 'SBIN', 'CMCN', 'SOAC', 'DISP', 'BOLD', 'VCHR', 'AROI',
     'TSUT', 'PUOR'})
class DocumentType6Code(CodeStrBaseModel):
    """
    Specifies a type of financial or commercial document.
    """
    pass


@set_external_code_set_decorator()
class ExternalAccountIdentification1Code(ExternalCodeStrBaseModel):
    """
    Specifies the external account identification scheme name code in the format of character string with a maximum
    length of 4 characters.
    """
    pass


@set_external_code_set_decorator()
class ExternalBalanceSubType1Code(ExternalCodeStrBaseModel):
    """
    Specifies the balance sub-type, as published in an external balance sub-type code list.
    """
    pass


@set_external_code_set_decorator()
class ExternalBalanceType1Code(ExternalCodeStrBaseModel):
    """
    Specifies the balance type, as published in an external balance type code set.
    """
    pass


@set_external_code_set_decorator()
class ExternalBankTransactionDomain1Code(ExternalCodeStrBaseModel):
    """
    Specifies the bank transaction code domain, as published in an external bank transaction code domain code list.
    """
    pass


@set_external_code_set_decorator()
class ExternalBankTransactionFamily1Code(ExternalCodeStrBaseModel):
    """
    Specifies the bank transaction code family, as published in an external bank transaction code family code list.
    """
    pass


@set_external_code_set_decorator()
class ExternalBankTransactionSubFamily1Code(ExternalCodeStrBaseModel):
    """
    Specifies the bank transaction code sub-family, as published in an external bank transaction code sub-family
    code list.
    """
    pass


@set_external_code_set_decorator()
class ExternalCardTransactionCategory1Code(ExternalCodeStrBaseModel):
    """
    Specifies the category of card transaction in the format of character string with a maximum length of 4 characters.
    """
    pass


@set_external_code_set_decorator()
class ExternalCashAccountType1Code(ExternalCodeStrBaseModel):
    """
    Specifies the nature, or use, of the cash account in the format of character string with a maximum length of
    4 characters.
    """
    pass


@set_external_code_set_decorator()
class ExternalChargeType1Code(ExternalCodeStrBaseModel):
    """
    Specifies the nature, or use, of the charges in the format of character string with a maximum length of 4
    characters.
    """
    pass


@set_external_code_set_decorator()
class ExternalClearingSystemIdentification1Code(ExternalCodeStrBaseModel):
    """
    Specifies the clearing system identification code, as published in an external clearing system identification
    code list.
    """
    pass


@set_external_code_set_decorator()
class ExternalCreditLineType1Code(ExternalCodeStrBaseModel):
    """
    Specifies the external credit line type code in the format of character string with a maximum length of 4
    characters.
    """
    pass


@set_external_code_set_decorator()
class ExternalDiscountAmountType1Code(ExternalCodeStrBaseModel):
    """
    Specifies the nature, or use, of the amount in the format of character string with a maximum length of 4
    characters.
    """
    pass


@set_external_code_set_decorator()
class ExternalDocumentLineType1Code(ExternalCodeStrBaseModel):
    """
    Specifies the document line type as published in an external document type code list.
    """
    pass


@set_external_code_set_decorator()
class ExternalEntryStatus1Code(ExternalCodeStrBaseModel):
    """
    Specifies the status of an entry on the books of the account servicer, as published in an external code set.
    """
    pass


@set_external_code_set_decorator()
class ExternalFinancialInstitutionIdentification1Code(ExternalCodeStrBaseModel):
    """
    Specifies the external financial institution identification scheme name code in the format of character string
    with a maximum length of 4 characters.
    """
    pass


@set_external_code_set_decorator()
class ExternalFinancialInstrumentIdentificationType1Code(ExternalCodeStrBaseModel):
    """
    Specifies the external financial instrument identification type scheme name code in the format of character
    string with a maximum length of 4 characters.
    """
    pass


@set_external_code_set_decorator()
class ExternalGarnishmentType1Code(ExternalCodeStrBaseModel):
    """
    Specifies the garnishment type as published in an external document type code list.
    """
    pass


@set_external_code_set_decorator()
class ExternalLocalInstrument1Code(ExternalCodeStrBaseModel):
    """
    Specifies the external local instrument code in the format of character string with a maximum length of 35
    characters.
    """
    pass


@set_external_code_set_decorator()
class ExternalOrganisationIdentification1Code(ExternalCodeStrBaseModel):
    """
    Specifies the external organisation identification scheme name code in the format of character string with a
    maximum length of 4 characters.
    """
    pass


@set_external_code_set_decorator()
class ExternalPersonIdentification1Code(ExternalCodeStrBaseModel):
    """
    Specifies the external person identification scheme name code in the format of character string with a maximum
    length of 4 characters.
    """
    pass


@set_external_code_set_decorator()
class ExternalProxyAccountType1Code(ExternalCodeStrBaseModel):
    """
    Specifies the external proxy account type code, as published in the proxy account type external code set.
    """
    pass


@set_external_code_set_decorator()
class ExternalPurpose1Code(ExternalCodeStrBaseModel):
    """
    Specifies the external purpose code in the format of character string with a maximum length of 4 characters.
    """
    pass


@set_external_code_set_decorator()
class ExternalReportingSource1Code(ExternalCodeStrBaseModel):
    """
    Specifies the reporting source, as published in an external reporting source code list.
    """
    pass


@set_external_code_set_decorator()
class ExternalRePresentmentReason1Code(ExternalCodeStrBaseModel):
    """
    Specifies the external representment reason code in the format of character string with a maximum length of 4
    characters. The list of valid codes is an external code list published separately.
    """
    pass


@set_external_code_set_decorator()
class ExternalReturnReason1Code(ExternalCodeStrBaseModel):
    """
    Specifies the nature, or use, of the amount in the format of character string with a maximum length of 4
    characters.
    """
    pass


@set_external_code_set_decorator()
class ExternalTechnicalInputChannel1Code(ExternalCodeStrBaseModel):
    """
    Specifies the technical input channel, as published in an external technical input channel code list.
    """
    pass


@set_valid_codes_decorator({'CRED', 'DEBT', 'BOTH'})
class FloorLimitType1Code(CodeStrBaseModel):
    """
    Indicates whether the floor limit applies to credit, to debit or to both credit and debit entries.
    """
    pass


@set_valid_codes_decorator({'INDY', 'OVRN'})
class InterestType1Code(CodeStrBaseModel):
    """
    Indicates which type of interest is applied to a balance left on an account.
    """
    pass


@set_regex_decorator(r'^[a-z]{2}$')
class ISO2ALanguageCode(str):
    """
    Identification of the language name according to the ISO 639-1 codes. The type is validated by the list of
    values coded with two alphabetic characters, defined in the standard.
    # TODO: validate against ISO 639-1 codes
    """
    pass


@set_valid_codes_decorator({'DOCT', 'MADM', 'MISS', 'MIST', 'MIKS'})
class NamePrefix2Code(CodeStrBaseModel):
    """
    Specifies the terms used to formally address a person.
    """
    pass


@set_valid_codes_decorator({'OFLN', 'ONLN', 'SMON'})
class OnLineCapability1Code(CodeStrBaseModel):
    """
    On-line and off-line capabilities of the POI (Point Of Interaction).
    """
    pass


@set_valid_codes_decorator({'OPOI', 'MERC', 'ACCP', 'ITAG', 'ACQR', 'CISS', 'DLIS'})
class PartyType3Code(CodeStrBaseModel):
    """
    Identification of the type of entity involved in a transaction.
    """
    pass


@set_valid_codes_decorator({'MERC', 'ACCP', 'ITAG', 'ACQR', 'CISS', 'TAXH'})
class PartyType4Code(CodeStrBaseModel):
    """
    Entity assigning an identification (for example merchant, acceptor, acquirer, tax authority, etc.).
    """
    pass


@set_valid_codes_decorator({'SOFT', 'EMVK', 'EMVO', 'MRIT', 'CHIT', 'SECM', 'PEDV'})
class POIComponentType1Code(CodeStrBaseModel):
    """
    Generic component type belonging to a POI (Point of Interaction) Terminal.
    """
    pass


@set_valid_codes_decorator({'LETT', 'MAIL', 'PHON', 'FAXX', 'CELL'})
class PreferredContactMethod1Code(CodeStrBaseModel):
    """
    Preferred method used to reach the individual contact within an organisation.
    """
    pass


@set_valid_codes_decorator({'DISC', 'PREM', 'PARV'})
class PriceValueType1Code(CodeStrBaseModel):
    """
    Specifies a type of value of the price.
    """
    pass


@set_valid_codes_decorator({'ALLL', 'CHNG', 'MODF'})
class QueryType3Code(CodeStrBaseModel):
    """
    Specifies the nature of the request, that is whether all information be returned or only information that has
    changed since the last similar request was returned.
    """
    pass


@set_valid_codes_decorator({'FAXI', 'EDIC', 'URID', 'EMAL', 'POST', 'SMSM'})
class RemittanceLocationMethod2Code(CodeStrBaseModel):
    """
    Specifies the method used to deliver the remittance advice information.
    """
    pass


@set_valid_codes_decorator(
    {'MM01', 'MM02', 'MM03', 'MM04', 'MM05', 'MM06', 'MM07', 'MM08', 'MM09', 'MM10', 'MM11', 'MM12', 'QTR1', 'QTR2',
     'QTR3', 'QTR4', 'HLF1', 'HLF2'})
class TaxRecordPeriod1Code(CodeStrBaseModel):
    """
    Specifies the period related to the tax payment.
    """
    pass


@set_valid_codes_decorator({'MAIL', 'TLPH', 'ECOM', 'TVPY', 'INTC', 'INTD', 'LOAN', 'PENS', 'TAXS', 'SACC', 'SVGS'})
class TransactionChannel1Code(CodeStrBaseModel):
    """
    Identifies the type of the communication channels used by the cardholder to the acceptor system.
    """
    pass


@set_valid_codes_decorator({'MERC', 'PRIV', 'PUBL'})
class TransactionEnvironment1Code(CodeStrBaseModel):
    """
    Indicates the environment of the transaction.
    """
    pass


@set_valid_codes_decorator(
    {'PIEC', 'TONS', 'FOOT', 'GBGA', 'USGA', 'GRAM', 'INCH', 'KILO', 'PUND', 'METR', 'CMET', 'MMET', 'LITR', 'CELI',
     'MILI', 'GBOU', 'USOU', 'GBQA', 'USQA', 'GBPI', 'USPI', 'MILE', 'KMET', 'YARD', 'SQKI', 'HECT', 'ARES', 'SMET',
     'SCMT', 'SMIL', 'SQMI', 'SQYA', 'SQFO', 'SQIN', 'ACRE'})
class UnitOfMeasure1Code(CodeStrBaseModel):
    """
    Unit of measure of the item purchased.
    """
    pass


@set_valid_codes_decorator({'MDSP', 'CDSP'})
class UserInterface2Code(CodeStrBaseModel):
    """
    Type of interface to display a message.
    """
    pass


# 6.2.3 Date

@set_datetime_format_decorator('YYYY-MM-DD')
class ISODate(DateTimeBaseModel):
    """
    A particular point in the progression of time in a calendar year expressed in the YYYY-MM-DD format. This
    representation is defined in "XML Schema Part 2: Datatypes Second Edition - W3C Recommendation 28 October 2004"
    which is aligned with ISO 8601.
    """
    pass


@set_datetime_format_decorator('YYYY-MM-DDThh:mm:ss.sssZ')
class ISODateTime(DateTimeBaseModel):
    """
    A particular point in the progression of time defined by a mandatory date and a mandatory time component,
    expressed in either UTC time format (YYYY-MM-DDThh:mm:ss.sssZ), local time with UTC offset format
    (YYYY-MM-DDThh:mm:ss.sss+/-hh:mm), or local time format (YYYY-MMDDThh:mm:ss.sss). These representations are
    defined in "XML Schema Part 2: Datatypes Second Edition - W3C Recommendation 28 October 2004" which is aligned
    with ISO 8601.

    Remark: Naive datetime objects are considered in the local timezone.
    """
    pass


# 6.2.5 IdentifierSet

@set_regex_decorator(r'^[A-Z0-9]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3}){0,1}$')
class AnyBICDec2014Identifier(str):
    """
    Code allocated to a financial or non-financial institution by the ISO 9362 Registration Authority, as described
    in ISO 9362: 2014 - "Banking - Banking telecommunication messages - Business identifier code (BIC)".
    """
    pass


@set_regex_decorator(r'^[A-Z0-9]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3}){0,1}$')
class BICFIDec2014Identifier(str):
    """
    Code allocated to a financial institution by the ISO 9362 Registration Authority as described in ISO 9362:
    2014 - "Banking - Banking telecommunication messages - Business identifier code (BIC)".
    """
    pass


@set_regex_decorator(r'^[A-Z]{2}[0-9]{2}[a-zA-Z0-9]{1,30}$')
class IBAN2007Identifier(str):
    """
    An identifier used internationally by financial institutions to uniquely identify the account of a customer at
    a financial institution, as described in the latest edition of the international standard ISO 13616:
    2007 - "Banking and related financial services - International Bank Account Number (IBAN)".
    """
    pass


@set_regex_decorator(r'^[A-Z]{2}[A-Z0-9]{9}[0-9]{1}$')
class ISINOct2015Identifier(str):
    """
    International Securities Identification Number (ISIN). A numbering system designed by the United Nation's
    International Organisation for Standardisation (ISO). The ISIN is composed of a 2-character prefix representing
    the country of issue, followed by the national security number (if one exists), and a check digit. Each country
    has a national numbering agency that assigns ISIN numbers for securities in that country.
    """
    pass


@set_regex_decorator(r'^[A-Z0-9]{18}[0-9]{2}$')
class LEIIdentifier(str):
    """
    Legal Entity Identifier is a code allocated to a party as described in ISO 17442 "Financial Services - Legal
    Entity Identifier (LEI)".
    """
    pass


@set_regex_decorator(r'^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$')
class UUIDv4Identifier(str):
    """
    Universally Unique IDentifier (UUID) version 4, as described in IETC RFC 4122 "Universally Unique IDentifier
    (UUID) URN Namespace".
    """
    pass


# 6.2.6 Indicator

class ChargeIncludedIndicator(StrictBool):
    """
    Indicates whether a charge is included in the amount.
    """
    pass


class TrueFalseIndicator(StrictBool):
    """
    A flag indicating a True or False value.
    """
    pass


class YesNoIndicator(StrictBool):
    """
    Indicates a "Yes" or "No" type of answer for an element.
    """
    pass


# 6.2.7 Quantity

class DecimalNumber(condecimal(max_digits=18)):
    """
    Number of objects represented as a decimal number, for example 0.75 or 45.6
    """
    pass


class NonNegativeDecimalNumber(condecimal(max_digits=18, ge=Decimal('0'))):
    """
    Number of objects represented as a non negative decimal number, for example, 0.75 or 45.6
    """
    pass


class Number(int):
    """
    Number of objects represented as an integer
    """
    pass


# 6.2.8 Rate
class BaseOneRate(condecimal(max_digits=11, ge=Decimal('0'), le=Decimal('1'))):
    """
    Rate expressed as a decimal, for example, 0.7 is 7/10 and 70%
    """
    pass


class PercentageRate(condecimal(max_digits=11, ge=Decimal('0'), le=Decimal('100'))):
    """
    Rate expressed as a percentage, that is, in hundredths, for example, 0.7 is 7/10 of a percent, and 7.0 is 7%
    """
    pass


# 6.2.9 Text

@set_regex_decorator(r'^[0-9]$')
class Exact1NumericText(CodeRegexBaseModel):
    """
    Specifies a numeric string with an exact length of1digit.
    """
    pass


@set_regex_decorator(r'^[0-9]{3}$')
class Exact3NumericText(CodeRegexBaseModel):
    """
    Specifies a numeric string with an exact length of 3 digits.
    """
    pass


@set_regex_decorator(r'^[a-zA-Z0-9]{4}$')
class Exact4AlphaNumericText(CodeRegexBaseModel):
    """
    Specifies an alphanumeric string with a length of 4 characters.
    """
    pass


@set_regex_decorator(r'^[a-zA-Z0-9\s\S]{1,1025}$')
class Max1025Text(CodeRegexBaseModel):
    """
    Specifies a character string with a maximum length of 1025 characters.
    """
    pass


@set_regex_decorator(r'^[a-zA-Z0-9\s\S]{1,105}$')
class Max105Text(CodeRegexBaseModel):
    """
    Specifies a character string with a maximum length of 105 characters.
    """
    pass


@set_regex_decorator(r'^[a-zA-Z0-9\s\S]{1,128}$')
class Max128Text(CodeRegexBaseModel):
    """
    Specifies a character string with a maximum length of 128 characters.
    """
    pass


@set_regex_decorator(r'^[a-zA-Z0-9\s\S]{1,140}$')
class Max140Text(CodeRegexBaseModel):
    """
    Specifies a character string with a maximum length of 140 characters.
    """
    pass


@set_regex_decorator(r'^[0-9]{1,15}$')
class Max15NumericText(CodeRegexBaseModel):
    """
    Specifies a numeric string with a maximum length of 15 digits.
    """
    pass


@set_regex_decorator(r'^[\+]{0,1}[0-9]{1,15}$')
class Max15PlusSignedNumericText(CodeRegexBaseModel):
    """
    Specifies a numeric string with a maximum length of 15 digits and may be prefixed with a plus sign.
    """
    pass


@set_regex_decorator(r'^[a-zA-Z0-9\s\S]{1,16}$')
class Max16Text(CodeRegexBaseModel):
    """
    Specifies a character string with a maximum length of 16 characters.
    """
    pass


@set_regex_decorator(r'^[a-zA-Z0-9\s\S]{1,2048}$')
class Max2048Text(CodeRegexBaseModel):
    """
    Specifies a character string with a maximum length of 2048 characters.
    """
    pass


@set_regex_decorator(r'^[a-zA-Z0-9\s\S]{1,34}$')
class Max34Text(CodeRegexBaseModel):
    """
    Specifies a character string with a maximum length of 34 characters.
    """
    pass


@set_regex_decorator(r'^[a-zA-Z0-9\s\S]{1,350}$')
class Max350Text(CodeRegexBaseModel):
    """
    Specifies a character string with a maximum length of 350 characters.
    """
    pass


@set_regex_decorator(r'^[a-zA-Z0-9\s\S]{1,35}$')
class Max35Text(CodeRegexBaseModel):
    """
    Specifies a character string with a maximum length of 35 characters.
    """
    pass


@set_regex_decorator(r'^[0-9]{1,3}$')
class Max3NumericText(CodeRegexBaseModel):
    """
    Specifies a numeric string with a maximum length of 3 digits.
    """
    pass


@set_regex_decorator(r'^[a-zA-Z0-9\s\S]{1,4}$')
class Max4Text(CodeRegexBaseModel):
    """
    Specifies a character string with a maximum length of 4 characters.
    """
    pass


@set_regex_decorator(r'^[a-zA-Z0-9\s\S]{1,500}$')
class Max500Text(CodeRegexBaseModel):
    """
    Specifies a character string with a maximum length of 500 characters.
    """
    pass


@set_regex_decorator(r'^[0-9]{1,5}$')
class Max5NumericText(CodeRegexBaseModel):
    """
    Specifies a numeric string with a maximum length of 5 digits.
    """
    pass


@set_regex_decorator(r'^[a-zA-Z0-9\s\S]{1,70}$')
class Max70Text(CodeRegexBaseModel):
    """
    Specifies a character string with a maximum length of 70 characters.
    """
    pass


@set_regex_decorator(r'^[0-9]{2,3}$')
class Min2Max3NumericText(CodeRegexBaseModel):
    """
    Specifies a numeric string with a minimum length of 2 digits, and a maximum length of 3 digits.
    """
    pass


@set_regex_decorator(r'^[0-9]{3,4}$')
class Min3Max4NumericText(CodeRegexBaseModel):
    """
    Specifies a numeric string with a minimum length of 3 digits, and a maximum length of 4 digits.
    """
    pass


@set_regex_decorator(r'^[0-9]{8,28}$')
class Min8Max28NumericText(CodeRegexBaseModel):
    """
    Specifies a numeric string with a minimum length of 8 digits, and a maximum length of 28 digits.
    """
    pass


@set_regex_decorator(r'^\+[0-9]{1,3}-[0-9()+\-]{1,30}$')
class PhoneNumber(CodeRegexBaseModel):
    """
    The collection of information which identifies a specific phone or FAX number as defined by telecom services.
    It consists of a "+" followed by the country code (from 1 to 3 characters) then a "-" and finally, any
    combination of numbers, "(", ")", "+" and "-" (up to 30 characters).
    """
    pass


# 6.2.10 Time

@set_datetime_format_decorator('hh:mm:ss.sssZ')
class ISOTime(DateTimeBaseModel):
    """
    A particular point in the progression of time in a calendar day expressed in either UTC time format
    (hh:mm:ss.sssZ), local time with UTC offset format (hh:mm:ss.sss+/-hh:mm), or local time format (hh:mm:ss.sss).
    These representations are defined in "XML Schema Part 2: Datatypes Second Edition - W3C Recommendation 28
    October 2004" which is aligned with ISO 8601.
    """
    pass


# 6.2.11 Year

@set_datetime_format_decorator('YYYY')
class ISOYear(DateTimeBaseModel):
    """
    Year represented by YYYY (ISO 8601).
    """
    pass


# 6.2.12 YearMonth

@set_datetime_format_decorator('YYYY-MM')
class ISOYearMonth(DateTimeBaseModel):
    """
    Month within a particular calendar year represented by YYYY-MM (ISO 8601).
    """
    pass
