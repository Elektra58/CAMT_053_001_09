# CAMT.053.001.09 - ISO 20022 Library

A Python library for generating and parsing ISO 20022 CAMT.053.001.09 compliant XML files. The library is designed to be easy to use, modular, and extensible. It uses popular Python libraries such as `lxml`, `pydantic`, `loguru`, and `dynaconf`.

## Features

- Generate importable ISO 20022 XML files for accounting software like Banana Accounting
- Supports input from various sources such as InteractiveBrokers FlexQuery XML files, TD Ameritrade activity statements, and others
- Leverages Pydantic for data validation and serialization
- Implements ISO 20022 CAMT.053.001.09 standard as closely as possible
- Includes unit tests for each class and function

## Installation

To install the library, simply run:

```bash
pip install git+https://github.com/Elektra58/CAMT_053_001_09.git
```


## Usage

Here's a basic example of how to use the library to create an `ActiveCurrencyAndAmount` instance and generate an XML element:

```python
from message_datatypes import ActiveCurrencyAndAmount
from lxml.etree import tostring

amount = ActiveCurrencyAndAmount(amount="12345.67", ccy="CHF")
xml_element = amount.to_xml(tag="Amt")
print(tostring(xml_element, pretty_print=True).decode("utf-8"))
```

More usage examples and detailed documentation will be added soon.

## Dependencies
- lxml
- pydantic
- loguru
- dynaconf

## Contributing
Contributions are welcome! Please feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
