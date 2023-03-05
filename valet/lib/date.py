import typing as tp
from datetime import datetime as dt
from datetime import timedelta


def to_date(date_string: str) -> dt.date:
    return dt.strptime(date_string, '%Y-%m-%d').date()


def is_date(date_string: str) -> bool:
    try:
        to_date(date_string)
    except ValueError:
        return False

    return True


def range(
    start: dt.date = dt.today().date(), days: int = 5
) -> tp.Generator[dt.date, None, None]:
    """
    Generates 'days' days starting with the next Monday after the `start` day.
    """
    until_monday = 7 - start.isoweekday() + 1
    monday = start + timedelta(days=until_monday)
    return (monday + timedelta(days=d) for d in range(days))
