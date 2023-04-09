import json
from pathlib import Path


def set_valid_codes_decorator(valid_codes):
    def decorator(cls):
        cls.set_valid_codes(valid_codes)
        return cls

    return decorator


def set_regex_decorator(regex_pattern: str):
    def decorator(cls):
        cls._regex = regex_pattern
        return cls

    return decorator


def set_external_code_set_decorator():
    json_path = Path(__file__).parent / 'json' / '4Q2022_ExternalCodeSets_v1.json'
    with json_path.open(mode='r', encoding='utf-8') as f:
        data = json.load(f)

    def decorator(cls):
        class_name = cls.__name__
        item = data['definitions'][class_name]

        if t := item.get('type') != 'string':
            raise ValueError(f'Unhandled type for {class_name}: {t}')
        if e := item.get('enum'):
            valid_codes = set(e)
            cls.set_valid_codes(valid_codes)
        elif (minl := item.get('minLength')) and (maxl := item.get('maxLength')):
            regex = f'^[A-Z]{{{minl},{maxl}}}$'
            cls.set_regex(regex)
        return cls

    return decorator


def set_datetime_format_decorator(format_string: str):
    def decorator(cls):
        cls._datetime_format = format_string
        return cls

    return decorator
