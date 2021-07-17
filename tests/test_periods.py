from api_v1.namespaces.periods import get_dates_month_period
import datetime as dt

def test_17th_january():
    date = dt.datetime(2020, 1, 17)
    start = dt.datetime(2019, 12, 25, 0, 0, 0)
    end = dt.datetime(2020, 1, 24, 23, 59, 59)
    assert get_dates_month_period(date) == (start, end), "17th january got wrong period"

def test_26th_december():
    date = dt.datetime(2019, 12, 26)
    start = dt.datetime(2019, 12, 25, 0, 0, 0)
    end = dt.datetime(2020, 1, 24, 23, 59, 59)
    assert get_dates_month_period(date) == (start, end), "26th december got wrong period"

def test_4th_april():
    date = dt.datetime(2021, 4, 4)
    start = dt.datetime(2021, 3, 25, 0, 0, 0)
    end = dt.datetime(2021, 4, 24, 23, 59, 59)
    assert get_dates_month_period(date) == (start, end), "4th april got wrong period"

def test_31st_october():
    date = dt.datetime(2021, 10, 31)
    start = dt.datetime(2021, 10, 25, 0, 0, 0)
    end = dt.datetime(2021, 11, 24, 23, 59, 59)
    assert get_dates_month_period(date) == (start, end), "31 october got wrong period"