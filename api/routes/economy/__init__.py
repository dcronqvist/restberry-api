import datetime as dt

def get_dates_month_period(date):
    today = date

    current_month = today.month

    if today.day >= 25:
        start_date = dt.datetime(today.year, today.month, 25)
        end_year = today.year
        if today.month >= 12:
            end_year += 1
        end_month = today.month + 1
        if end_month > 12:
            end_month = end_month % 12
        
        end_date = dt.datetime(end_year, end_month, 24)

        return start_date, end_date
    else:
        if today.month == 1:
            start_date = dt.datetime(today.year - 1, 12, 25)
            end_date = dt.datetime(today.year, today.month, 24)
            return start_date, end_date
        else:
            start_date = dt.datetime(today.year, today.month - 1, 25)
            end_date = dt.datetime(today.year, today.month, 24)
            return start_date, end_date

        