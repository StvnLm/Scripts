import datetime
from datetime import date
import holidays

class ValidDate():

    def __init__(self):
        self.self = self

    def daterange(self, start_date, end_date):
        for n in range((end_date - start_date).days + 1):
            yield start_date + datetime.timedelta(n)

    def weekendcheck(self, start_date, end_date,):
        counter = 0
        for day in ValidDate().daterange(start_date=start_date, end_date=end_date):
            if day.isoweekday() == 6 or day.isoweekday() == 7:
                counter += 1
        return counter

    def holidaycheck(self, start_date, end_date, province):
        holidaylist = []
        for date in ValidDate().daterange(start_date, end_date):
            for holiday_date, holiday_name in sorted(holidays.CA(prov=province, years=date.year).items()):
                # Ensure holiday isnt already on Weekend
                if date == holiday_date and (date.isoweekday() != 6 and date.isoweekday() != 7):
                    holidaylist.append(holiday_name + ' - ' + str(holiday_date))
            if province == 'QC' and 'Boxing Day' in holidaylist:
                holidaylist.remove('Boxing Day')
        return holidaylist

