import pytest
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta
from app.services.utils import get_date_difference, days_declension


@pytest.mark.parametrize(
    'date_before, interval, expected_result',
    (
        (date.today() + timedelta(days=-100), 'd', 100),
        (date.today() + timedelta(weeks=-10), 'm', 2),  # 10 недель - полных 2 месяца
        (date.today() + timedelta(days=-408), 'd', 408),
    )
)
def test_get_date_difference(date_before, interval, expected_result):
    result = get_date_difference(f'{date_before.strftime("%Y-%m-%d")} 00:00:00', interval)
    assert result == expected_result


@pytest.mark.parametrize(
    'days, word',
    (
        (1, 'день'),
        (3, 'дня'),
        (5, 'дней'),
        (101, 'день'),
        (202, 'дня'),
        (808, 'дней'),
    )
)
def test_days_declension(days, word):
    result = days_declension(days)
    assert result == word
