__author__ = "Steven Lam"
__version__ = "1.0.0"
__status__ = "PRE_PRODUCTION"

import datetime
from datetime import date
import json
from ValidDate import *
'''
TODO: 
-implement GUI Interface
-Calcualte SLA infringement
'''

class SLA():

    def __init__(self, client, st_year, st_month, st_day, st_hr, st_min, end_year, end_month, end_day, end_hr, end_min):
        self.st_year = st_year
        self.st_month = st_month
        self.st_day = st_day
        self.st_hr = st_hr
        self.st_min = st_min
        self.end_year = end_year
        self.end_month = end_month
        self.end_day = end_day
        self.end_hr = end_hr
        self.end_min = end_min
        self.client = client


    # Return the total time the ticket was counting down in the SLA timer for SEV2 and SEV3
    # TODO: Refactor to use UTC offset
    def calculate_ticket_hrs(self):
        total_ticket_hrs = 0
        ca_holidays = holidays.Canada()

        with open('data.json') as f:
            data = json.load(f)

            ticket_start = datetime.date(self.st_year, self.st_month, self.st_day)
            ticket_end = datetime.date(self.end_year, self.end_month, self.end_day)

            # Calculate the # of hours the ticket has been in progress countdown
            first_day = datetime.datetime(year=self.st_year, month=self.st_month, day=self.st_day, hour=data[self.client]["end"]) \
                        - datetime.datetime(year=self.st_year, month=self.st_month, day=self.st_day, hour=self.st_hr, minute=self.st_min)
            full_days = ((ticket_end - ticket_start).days - 1) * 8
            last_day = datetime.datetime(year=self.end_year, month=self.end_month, day=self.end_day, hour=self.end_hr, minute=self.end_min) \
                        - datetime.datetime(year=self.end_year, month=self.end_month, day=self.end_day, hour=data[self.client]["start"])
            total_ticket_hrs = (first_day.total_seconds()/3600) + full_days + (last_day.total_seconds()/3600)

            # Check if day lands on Sat, Sun, or holiday; if so - deduct 8 hrs
            _ = ValidDate()
            for day in _.daterange(start_date=ticket_start, end_date=ticket_end):
                if day.isoweekday() == 6 or day.isoweekday() == 7:
                    total_ticket_hrs -= 8
            holiday_list = _.holidaycheck(start_date=ticket_start, end_date=ticket_end, province=data[self.client]["prov"])
            total_ticket_hrs -= len(holiday_list) * 8

        return holiday_list, total_ticket_hrs

    def calculate_sla_breach(self, severity):
        sev = ''
        with open('data.json') as f:
            data = json.load(f)
            if (self.client == 'OPT' or self.client == 'ALM' or self.client == 'SDM' or self.client == 'TMX') and severity == 1:
                sev = 'severity_1_min'
            elif self.client == 'TMX' and severity == 2:
                sev = 'severity_2_min'
            else:
                sev = 'severity_' + str(severity)
            ticket_max_time =  data[self.client][sev]
        return ticket_max_time


test = SLA(client="TMX", st_year=2017, st_month=12, st_day=30, st_hr=9, st_min=0,
                                    end_year=2018, end_month=1, end_day=2, end_hr=17, end_min=0)
print(test.calculate_ticket_hrs())
print(test.calculate_sla_breach(2))


