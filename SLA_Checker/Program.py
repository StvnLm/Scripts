__author__ = "Steven Lam"
__version__ = "1.0.0"
__status__ = "PRE_PRODUCTION"

from datetime import date, datetime
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


    # TODO: Refactor to use UTC offset?

    def calculate_ticket_hrs(self):
        total_ticket_hrs = 0
        ca_holidays = holidays.Canada()

        with open('data.json') as f:
            data = json.load(f)

            ticket_start = datetime.date(self.st_year, self.st_month, self.st_day)
            ticket_end = datetime.date(self.end_year, self.end_month, self.end_day)

            # Calculate the # of hours the ticket has been in progress countdown
            total_ticket_hrs = 0
            first_day = datetime.datetime(self.st_year, self.st_month, self.st_day, data[self.client]["end"]) \
                        - datetime.datetime(self.st_year, self.st_month, self.st_day, self.st_hr, self.st_min)
            full_days = ((ticket_end - ticket_start).days - 1) * 8
            if ticket_start == ticket_end:
                last_day = 0
                full_days = 0
                total_ticket_hrs = (first_day.total_seconds()/3600) + full_days
            else:
                full_days = ((ticket_end - ticket_start).days - 1) * 8
                last_day = datetime.datetime(self.end_year, self.end_month, self.end_day, self.end_hr, self.end_min) \
                                            - datetime.datetime(self.end_year, self.end_month, self.end_day, data[self.client]["start"])
                total_ticket_hrs = (first_day.total_seconds()/3600) + full_days + (last_day.total_seconds()/3600)
                
            # Check if day lands on Sat, Sun, or holiday; if so - deduct 8 hrs
            weekends = ValidDate().weekendcheck(ticket_start, ticket_end)
            holiday_list = ValidDate().holidaycheck(start_date=ticket_start, end_date=ticket_end, province=data[self.client]["prov"])
            total_ticket_hrs -= (weekends + len(holiday_list)) * 8
        return total_ticket_hrs


    def calculate_sla_breach(self, severity, ticket_hours):
        ticket_max_time = 0.0

        with open('data.json') as f:

            data = json.load(f)
            # If the client has minutes instead of hours, add 15 minutes
            if (self.client == 'OPT' or self.client == 'ALM' or self.client == 'SDM' or self.client == 'TMX') and severity == 'severity_1':
                ticket_max_time = data[self.client]['SEV'][severity]
            elif self.client == 'TMX' and severity == 'severity_2':
                ticket_max_time = data[self.client]['SEV'][severity]
            else:
                ticket_max_time = data[self.client]['SEV'][severity] * 60.0

        ticket_time_minutes = (SLA(self.client, self.st_year, self.st_month, self.st_day, data[self.client]["start"], self.st_min, self.end_year,
                          self.end_month, self.end_day, self.end_hr, self.end_min).calculate_ticket_hrs()) * 60

        remaining_sla_hrs = (ticket_max_time - ticket_time_minutes) / 60
        return remaining_sla_hrs


