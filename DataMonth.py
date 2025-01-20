import os
from calendar import monthrange
from datetime import datetime, timedelta

import openpyxl

from config import dict_months


class DataMonthNow:

    def __init__(self, daily_report, report):
        self.month = datetime.now().month
        self.daily_report = daily_report
        self.report = report

    def get_count_day_month(self):
        """Возвращает количество дней текущего месяца"""

        year_today = datetime.now().year
        count_days = (monthrange(year_today, self.month))[1]

        return count_days

    def get_name_month_now(self):
        """Возвращает название месяца"""

        name_month = dict_months[self.month]
        return name_month

    def get_paths_to_file(self):
        """Возвращает маршруты до файлов"""

        name_month_now = self.get_name_month_now()
        path_daily_report = self.daily_report[0] + name_month_now + self.daily_report[1] + name_month_now.lower() + self.daily_report[2]
        path_report = self.report[0] + name_month_now + self.report[1]
        paths = {'daily_report': path_daily_report, 'report': path_report}
        return paths

    def get_data_daily_file(self):
        """Возвращает книгу суточный рапорт"""

        paths = self.get_paths_to_file()
        data_file = openpyxl.load_workbook(paths['daily_report'], data_only=True)

        return data_file

    # def get_date_update_file(self, paths):
    #     """Возвращает дату обновления данных в рапорте - 1 день"""
    #
    #     update_time = os.path.getmtime(paths['report'])
    #     mtime_readable = (datetime.fromtimestamp(update_time) - timedelta(days=1))
    #     format_date = mtime_readable.strftime('%d.%m.%y')
    #     return format_date

    def get_plan_volume(self):
        """Возвращает план на месяц"""

        data_file = self.get_data_daily_file()
        count_days_month = self.get_count_day_month()
        last_sheet = data_file[str(count_days_month)]
        plan = last_sheet['I47']

        return int(plan.value)

    def get_actual_volume(self):
        """Возвращает данные по заготовке с начала месяца"""

        data_file = self.get_data_daily_file()
        paths = self.get_paths_to_file()
        plan_month = self.get_plan_volume()
        update_time = os.path.getmtime(paths['report'])
        mtime_readable = (datetime.fromtimestamp(update_time))

        # получаем дату обновления данных в рапорте (не дату обновления файла)
        back_date_update = mtime_readable - timedelta(days=1)
        format_date_update = back_date_update.strftime('%d.%m.%y')

        number_page = mtime_readable.day

        actual_list = []
        for i in range(number_page):
            d = {}
            if i == 0:
                continue
            work_page = data_file[f'{i}']
            d[f'{i}'] = {'actual': int(work_page['F47'].value), 'plan': int(work_page['E47'].value)}
            actual_list.append(d)


        work_page = data_file[f'{number_page - 1}']
        volume_actual = work_page['J47'].value
        volume_plan = work_page['I47'].value
        res = {
            'actual': int(volume_actual),
            'plan': int(volume_plan),
            'update_time': format_date_update,
            'plan_month': plan_month,
            'actual_list': actual_list,
        }
        return res

