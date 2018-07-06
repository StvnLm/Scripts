import datetime
from datetime import date
import json

class ValidDate():

    def __init__(self):
        self.self = self


    def daterange(self, start_date, end_date):
        for n in range((end_date - start_date).days + 1):
            yield start_date + datetime.timedelta(n)


    def weekendcheck(self, start_date, end_date):
        saturday_counter, sunday_counter = 0, 0
        for day in ValidDate().daterange(start_date=start_date, end_date=end_date):
            if day.isoweekday() == 6:
                saturday_counter += 1
            if day.isoweekday() == 7:
                sunday_counter += 1
        return saturday_counter, sunday_counter

    def weekdaylist(self, start_date, end_date):
        weekdaylist = []
        for day in ValidDate().daterange(start_date=start_date, end_date=end_date):
            if day.isoweekday() != (6 and 7):
                weekdaylist.append((str(day.month) + '/' + str(day.day) + '/' + str(day.year)))
        return  weekdaylist

    # Uses holidays module

    # def holidaycheck(self, start_date, end_date, province):
    #     holidaylist = []
    #     for date in ValidDate().daterange(start_date, end_date):
    #         date = datetime.date(date.year, date.month, date.day)
    #         for holiday_date, holiday_name in sorted(holidays.CA(prov=province, years=date.year).items()):
    #             # Ensure holiday isnt already on Weekend
    #             if date == holiday_date and (date.isoweekday() != 6 and date.isoweekday() != 7):
    #                 holidaylist.append(holiday_name + ' - ' + str(holiday_date))
    #         if province == 'QC' and 'Boxing Day' in holidaylist:
    #             holidaylist.remove('Boxing Day')
    #     return holidaylist


    # def weekend_holiday_hours(self, start_datetime, end_datetime, province):
    #     total_hours = [0, 0, 0]
    #     holidates = holidays.CA(prov='ON', years=2018)
    #     if province == 'QC' or province == 'AL' or province == 'BC':
    #         for k, v in dict(holidates).items():
    #             if v == 'Boxing Day':
    #                 del holidates[k]
    #     if start_datetime.isoweekday() == 6 or start_datetime.isoweekday() == 7:
    #         total_hours =  [(23 - start_datetime.hour), (60 - start_datetime.minute), 0]
    #         if total_hours[1] == 60:
    #             total_hours[1] = 0
    #             total_hours[0] += 1
    #     for day in ValidDate().daterange(start_date=start_datetime + datetime.timedelta(days=1), end_date=end_datetime):
    #         if day.isoweekday() == 6 or day.isoweekday() == 7 or day in holidates:
    #             total_hours[2] += 1
    #     return total_hours


date1 = datetime.datetime(2018, 7, 1, 8, 0)
date2 = datetime.datetime(2018, 7, 5, 17, 0)
x = ValidDate().weekdaylist(date1, date2)
print(x)

# x=ValidDate().holidaycheck(date1, date2, 'ON')
# print(x)
# for day in ValidDate().daterange(start_date=date1, end_date=date2):
#     ValidDate().weekend_holiday_hours(date1, date2)
# print(ValidDate().weekend_holiday_hours(date1, date2, 'BC'))


