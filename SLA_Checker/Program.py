__author__ = "Steven Lam"
__version__ = "1.0.0"
__status__ = "PRE_PRODUCTION"

from datetime import datetime, date
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
    def calculate_ticket_hrs(self):

        total_ticket_hrs = 0

        with open('data.json') as f:
            data = json.load(f)

            ticket_start_date = date(self.st_year, self.st_month, self.st_day)
            ticket_end_date = date(self.end_year, self.end_month, self.end_day)

            # Check if day lands on Sat, Sun, or holiday; if so - deduct 8 hrs
            weekends = ValidDate().weekendcheck(ticket_start_date, ticket_end_date)
            holiday_list = ValidDate().holidaycheck(start_date=ticket_start_date, end_date=ticket_end_date, province=data[self.client]["prov"])
            total_ticket_hrs -= (weekends + len(holiday_list)) * 8

            ticket_end_time = datetime.datetime(self.end_year, self.end_month, self.end_day, self.end_hr, self.end_min)
            ticket_start_time = datetime.datetime(self.st_year, self.st_month, self.st_day, self.st_hr, self.st_min)

            if ticket_start_date == ticket_end_date:
                total_ticket_hrs = ticket_end_time - ticket_start_time

            else:
                client_start_hr = data[self.client]['start']
                client_end_hr = data[self.client]['end']

                start_hr, start_min = self.st_hr, self.st_min
                if self.st_hr <= 9:
                    start_hr, start_min = 9, 0

                first_day_hours = datetime.datetime(self.st_year, self.st_month, self.st_day, client_end_hr) - \
                                  datetime.datetime(self.st_year, self.st_month, self.st_day, start_hr, start_min)

                full_day_hours = ((ticket_end_date - ticket_start_date).days - 1) * 8.0

                end_hr, end_min = self.end_hr, self.end_min
                if self.end_hr <= 9:
                    end_hr, end_min = 9, 0
                if self.end_hr >= 17:
                    end_hr, end_min = 17, 0

                last_day_hours = datetime.datetime(self.end_year, self.end_month, self.end_day, end_hr, end_min) - \
                                 datetime.datetime(self.end_year, self.end_month, self.end_day, client_start_hr)

                total_ticket_hrs = (first_day_hours.total_seconds() / 3600.0) + full_day_hours + (last_day_hours.total_seconds() / 3600.0)

        return total_ticket_hrs


    def calculate_sla_breach(self, severity, ticket_hours):

        with open('data.json') as f:
            data = json.load(f)

        if severity == 'severity 1' or severity == 'severity 2':
            start = datetime.datetime(self.st_year, self.st_month, self.st_day, self.st_hr, self.st_min)
            end = datetime.datetime(self.end_year, self.end_month, self.end_day, self.end_hr, self.end_min)
            delta = end - start
            # TODO: FIX THIS. Current returns Hrs + % mins...
            return data[self.client]['SEV'][severity] - (delta.total_seconds() / 3600)
        elif severity == 'severity 3' or severity == 'severity 4':
            ticket_max_time = data[self.client]['SEV'][severity]
            print(ticket_max_time, (ticket_hours.total_seconds() / 3600))
            remaining_sla_hrs = (ticket_max_time - (ticket_hours.total_seconds() / 3600.0))
            return remaining_sla_hrs


# test = SLA(client="AC", st_year=2018, st_month=7, st_day=4, st_hr=9, st_min=0,
#                         end_year=2018, end_month=7, end_day=4, end_hr=12, end_min=0)
#
# hrs = test.calculate_ticket_hrs()
# print(test.calculate_sla_breach("severity 3", hrs))
