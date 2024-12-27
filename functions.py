import os
from calendar import monthrange
from datetime import datetime, timedelta

from config import dict_months

def get_count_day_month(month):
    """Возвращает количество дней переданного месяца"""

    year_today = datetime.now().year
    count_days = (monthrange(year_today, month))[1]

    return count_days


def get_plan_volume(data_file, count_days):
    """Возвращает значение плана"""

    last_sheet = data_file[str(count_days)]
    plan = last_sheet['I47']

    return int(plan.value)

def get_date_update_file(path_report):

    update_time = os.path.getmtime(path_report)
    mtime_readable = (datetime.fromtimestamp(update_time) - timedelta(days=1))
    format_date = mtime_readable.strftime('%d.%m.%y')
    return format_date

def get_actual_volume(daily_report, path_report):
    """Возвращает объем на прошлый вечер"""

    update_time = os.path.getmtime(path_report)
    mtime_readable = datetime.fromtimestamp(update_time)
    number_page = mtime_readable.day
    work_page = daily_report[f'{number_page-1}']
    volume_actual = work_page['J47'].value
    volume_plan = work_page['I47'].value
    res = {'actual': int(volume_actual), 'plan': int(volume_plan)}
    return res

def get_data_today(data_file, count_days, data_today):
    last_sheet = data_file[str(count_days)]
    date = datetime.now().day
    day_sheet = data_file[str(date-1)]




def get_name_month_now(month):
    """Возвращает название месяца"""

    name_month = dict_months[month]
    return name_month


def get_paths_to_file(name_month, day_report, report):
    """Возвращает маршруты до файлов"""

    path_dayily_report = day_report[0] + name_month + day_report[1] + name_month.lower() + day_report[2]
    path_report = report[0] + name_month + report[1]
    paths = {'daily_report': path_dayily_report, 'report': path_report}
    return paths
