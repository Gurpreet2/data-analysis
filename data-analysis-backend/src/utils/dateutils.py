from datetime import datetime
from typing import Optional


def have_same_month(first_date: datetime, second_date: datetime) -> bool:
    """
    Returns true if `first_date` and `second_date` have the same year and month
    """
    return first_date.year == second_date.year and first_date.month == second_date.month


def have_same_day(first_date: datetime, second_date: datetime) -> bool:
    """
    Returns true if `first_date` and `second_date` have the same year, month, and day
    """
    return first_date.date() == second_date.date()


def get_date_format(date_string: str) -> Optional[str]:
    """
    Returns the date format of the passed in string if it is a date, `None` if it isn't a date
    """
    if date_string is None:
        return None
    formats = [
        '%m/%d/%Y',
        '%m/%d/%y',
        '%m-%d-%Y',
        '%Y-%m-%d',
        '%m-%d-%y',
        '%y-%m-%d',
    ]
    for fmt in formats:
        try:
            datetime.strptime(date_string, fmt)
            return fmt
        except ValueError:
            continue
    return None
