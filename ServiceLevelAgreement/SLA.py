__author__ = "Steven Lam"
__version__ = "1.0.0"
__status__ = "PRE_PRODUCTION"

import datetime
from datetime import date
import json
import holidays


class DateRange:

    def __init__(self):
        self.self = self


    def daterange(self, start_date, end_date):
        for n in range((end_date - start_date).days + 1):
            yield start_date + datetime.timedelta(n)


class SLA:

    def __init__(self, client, severity):
        self.client = client
        self.severity = severity


    # Return the total time the ticket was counting down in the SLA timer for SEV2 and SEV3
    # TODO: Refactor to use UTC offset
    def calculate_sla_sev23(self, st_year, st_month, st_day, st_hr, st_min, end_year, end_month, end_day, end_hr, end_min):
        total_sla_time = 0
        ca_holidays = holidays.Canada()
        with open('data.json') as f:
            data = json.load(f)

            # Calculate the # of hours the ticket has been in SLA countdown
            first_day = datetime.datetime(year=st_year, month=st_month, day=st_day, hour=data[self.client]["end"]) \
                        - datetime.datetime(year=end_year, month=st_month, day=st_day, hour=st_hr, minute=st_min)
            full_days = (datetime.datetime(year=end_year, month=end_month, day=end_day)
                        - datetime.datetime(year=st_year, month=st_month, day=st_day) - datetime.timedelta(days=1)) * 8
            last_day = datetime.datetime(year=end_year, month=end_month, day=end_day, hour=end_hr, minute=end_min) \
                       - datetime.datetime(year=end_year, month=end_month, day=end_day, hour=data[self.client]["start"])
            total_sla_time = float(first_day.total_seconds()/3600) + float(full_days.days) + float(last_day.total_seconds()/3600)

            # Calculate the number of weekdays
            ticket_start = datetime.date(st_year, st_month, st_day)
            ticket_end = datetime.date(end_year, end_month, end_day)
            weekend = DateRange()
            for day in weekend.daterange(ticket_start, ticket_end):
                if day.isoweekday() == 6 or day.isoweekday() == 7:
                    total_sla_time -= 8
        return total_sla_time

    def calculate_sla_breach(self):
        pass

test = SLA("AC", 1)
print(test.calculate_sla_sev23(st_year=2018, st_month=6, st_day=29, st_hr=9, st_min=0,
                              end_year=2018, end_month=7, end_day=3, end_hr=17, end_min=0))


for date, name in sorted(holidays.Canada(prov='ON').items()):
    print(date, name)
