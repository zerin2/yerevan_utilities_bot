from decimal import Decimal


def to_decimal(num_str: str):
    return Decimal(num_str.replace(',', '.'))
