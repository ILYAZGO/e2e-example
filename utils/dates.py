from datetime import datetime, timedelta
import calendar

#.strftime("%d/%m/%Y")
#.strftime("%Y-%m-%d")

today = datetime.now()
today_with_dots = today.strftime("%d.%m.%y")

yesterday = (today - timedelta(days=1))

first_day_this_week = today - timedelta(days=today.weekday())
last_day_this_week = first_day_this_week + timedelta(days=6)

first_day_last_week = first_day_this_week - timedelta(days=7)
last_day_last_week = first_day_last_week + timedelta(days=6)

first_day_this_month = today.replace(day=1)
days_in_current_month = calendar.monthrange(today.year, today.month)[1]
last_day_this_month = today.replace(day=days_in_current_month)


if today.month == 1:  # Handle January
    first_day_last_month = datetime(today.year - 1, 12, 1)
else:
    first_day_last_month = datetime(today.year, today.month - 1, 1)
#first_day_last_month = today - timedelta(days=today.month)
last_day_last_month = first_day_this_month - timedelta(days=1)

#first_day_last_quarter =
#last_day_last_quarter =

first_month_of_quarter = (today.month - 1) // 3 * 3 + 1
first_day_this_quarter = datetime(today.year, first_month_of_quarter, 1)
last_month_of_quarter = ((today.month - 1) // 3 + 1) * 3
# Create a date for the first day of the next month
first_day_of_next_month = datetime(today.year, last_month_of_quarter + 1, 1) if (
        last_month_of_quarter < 12) else datetime(today.year + 1, 1, 1)
# Subtract one day to get the last day of the quarter
last_day_this_quarter = first_day_of_next_month - timedelta(days=1)

first_day_last_year = today.replace(year=today.year - 1, month=1, day=1)
last_day_last_year = today.replace(year=today.year - 1, month=12, day=31)

first_day_this_year = today.replace(month=1, day=1)
last_day_this_year = today.replace(month=12, day=31)



tomorrow = (today + timedelta(days=1)).strftime("%d/%m/%Y")
tomorrow_with_dash = (today + timedelta(days=1)).strftime("%Y-%m-%d") # for quotas test

first_day_week_ago = (today - timedelta(days=6)).strftime("%d/%m/%Y")


first_day_year_ago = (today - timedelta(days=365)).strftime("%d/%m/%Y")


