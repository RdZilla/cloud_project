from decimal import Decimal, InvalidOperation
from typing import Union


def convert_to_decimal(value: Union[str, Decimal, int, float]) -> Union[dict, Decimal]:
    """
    Convert value to decimal
    :param value: input value
    :return: Decimal parameter value
    """
    try:
        value = str(value).replace(',', '.')
        return Decimal(value)
    except (ValueError, TypeError, InvalidOperation):
        return {"detail": "Invalid value"}


def convert_to_boolean(value: Union[str, bool]) -> bool:
    """
    Convert string to boolean
    :param value: input value
    :return: boolean parameter
    """
    if value in [True, 'true']:
        return True
    elif value in [False, 'false']:
        return False
    else:
        raise ValueError
