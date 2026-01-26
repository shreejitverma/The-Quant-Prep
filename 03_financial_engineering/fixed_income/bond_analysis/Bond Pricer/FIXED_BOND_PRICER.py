import pandas as pd
import numpy as np
import math as m
import datetime as dt
from dateutil.relativedelta import relativedelta
import calendar

##################################################################################
#Adding daycount convention functions
##################################################################################
def day_count_actual_360(start_date, end_date):
    #Returns number of days between start_date and end_date, using Actual/360 convention
    return (end_date - start_date).days

def day_count_actual_365(start_date, end_date):
    #Returns number of days between start_date and end_date, using Actual/365 convention
    return (end_date - start_date).days

def day_count_actual_actual(start_date, end_date):
    #Returns number of days between start_date and end_date, using Actual/Actual convention
    return (end_date - start_date).days

def day_count_30_360(start_date, end_date):
    #Returns number of days between start_date and end_date, using Thirty/360 convention
    d1 = min(30, start_date.day)
    d2 = min(d1, end_date.day) if d1 == 30 else end_date.day
    return 360*(end_date.year - start_date.year) + 30*(end_date.month - start_date.month) + d2 - d1

def day_count_30E_360(start_date, end_date):
    #Returns number of days between start_date and end_date, using ThirtyE/360 convention
    d1 = min(30, start_date.day)
    d2 = min(30, end_date.day)
    return 360 * (end_date.year - start_date.year) + 30 * (end_date.month - start_date.month) + d2 - d1

class fixed_bond:
    def __init__(self, issue_date, settlement_date, first_coupon_date, maturity_date, face_value, reoffer_yield, coupon_rate, first_coupon_type, coupon_frequency, day_count_convention, redemption_rate):
        ##################################################################################
        #Setting up inital attributes
        ##################################################################################
        self.issue_date = issue_date
        self.settlement_date = settlement_date
        self.first_coupon_date = first_coupon_date
        self.maturity_date = maturity_date
        self.face_value = face_value
        self.reoffer_yield = reoffer_yield
        self.coupon_rate = coupon_rate
        self.first_coupon_type = first_coupon_type
        self.coupon_frequency = coupon_frequency
        self.day_count_convention = day_count_convention
        self.redemption_rate = redemption_rate

        ##################################################################################
        #Parsing input values
        ##################################################################################
        #Converting reoffer yield to percentage
        self.reoffer_yield = self.reoffer_yield/100

        #Converting coupon rate to percentage
        self.coupon_rate = self.coupon_rate/100

        #parsing coupon frequency
        if self.coupon_frequency == "ANNUAL":
            self.coupon_frequency_modifier = 1
        elif self.coupon_frequency == "SEMI-ANNUAL":
            self.coupon_frequency_modifier = 2
        elif self.coupon_frequency == "QUARTERLY":
            self.coupon_frequency_modifier = 4
        elif self.coupon_frequency_modifier == "MONTHLY":
            self.coupon_frequency_modifier = 12
        else:
            self.coupon_frequency_modifier = 1
            #need to add error handling

        #Converting redemption rate to percentage
        self.redemption_rate = self.redemption_rate/100

        #Generating accrual start date
        time_modifier = int(12/self.coupon_frequency_modifier)
        if self.first_coupon_type == "REGULAR":
            self.accrual_start_date = self.settlement_date
        else:
            self.accrual_start_date = self.first_coupon_date - relativedelta(months=time_modifier)

        ##################################################################################
        #Generating the columns for the cash flow table
        ##################################################################################
        #generating cash flow schedule
        cash_flow_date = self.first_coupon_date
        cash_flow_dates = [cash_flow_date]
        self.number_of_periods = 1

        while cash_flow_date < maturity_date:
            cash_flow_date += relativedelta(months=time_modifier)
            cash_flow_dates.append(cash_flow_date)
            self.number_of_periods += 1

        self.cash_flow_dates = cash_flow_dates

        #computing cash flow periods
        cash_flow_periods = []
        for i in range(self.number_of_periods):
            cash_flow_periods.append(i + 1)
        self.cash_flow_periods = cash_flow_periods

        # computing future cash flows per date
        self.coupon_payment = (self.face_value*self.coupon_rate)/self.coupon_frequency_modifier
        self.principal_payment = self.face_value * self.redemption_rate

        cash_flow_amounts = []
        for i in range(self.number_of_periods):
            if i == self.number_of_periods - 1:
                cash_flow = self.principal_payment + self.coupon_payment
            else:
                cash_flow = self.coupon_payment

            cash_flow_amounts.append(cash_flow)
        self.cash_flow_amounts = cash_flow_amounts

        #Computing discount rate
        self.discount_rate = 1 + (self.reoffer_yield/self.coupon_frequency_modifier)
        self.discount_rates = []
        for i in range(self.number_of_periods):
            self.discount_rates.append(self.discount_rate)

        #Computing discount period
        if self.first_coupon_type == "REGULAR":
            self.discount_period = 1
        else:
            if self.day_count_convention == "ACTUAL/ACTUAL":
                numerator = day_count_actual_actual(self.settlement_date,self.first_coupon_date)
                denominator = day_count_actual_actual(self.accrual_start_date,self.first_coupon_date)
                self.discount_period = numerator/denominator
                if self.first_coupon_type == "FULL SHORT FIRST":
                    accrued_numerator = day_count_actual_actual(self.accrual_start_date,self.settlement_date)
                    accrued_denominator = denominator
                    self.accrued_period = accrued_numerator/accrued_denominator
                    self.accrued_days = accrued_numerator
                    self.accrued_interest = self.cash_flow_amounts[0]*self.accrued_period
                else:
                    self.accrued_period = 0
                    self.accrued_days = 0
                    self.accrued_interest = 0

            elif self.day_count_actual_365 == "ACTUAL/365":
                numerator = day_count_actual_365(self.settlement_date,self.first_coupon_date)
                denominator = 365/self.coupon_frequency_modifier
                self.discount_period = numerator/denominator
                if self.first_coupon_type == "FULL SHORT FIRST":
                    accrued_numerator = day_count_actual_actual(self.accrual_start_date,self.settlement_date)
                    accrued_denominator = denominator
                    self.accrued_period = accrued_numerator/accrued_denominator
                    self.accrued_days = accrued_numerator
                    self.accrued_interest = self.cash_flow_amounts[0]*self.accrued_period
                else:
                    self.accrued_period = 0
                    self.accrued_days = 0
                    self.accrued_interest = 0

            elif self.day_count_actual_360 == "ACTUAL/360":
                numerator = day_count_actual_360(self.settlement_date,self.first_coupon_date)
                denominator = 360/self.coupon_frequency_modifier
                self.discount_period = numerator/denominator
                if self.first_coupon_type == "FULL SHORT FIRST":
                    accrued_numerator = day_count_actual_actual(self.accrual_start_date,self.settlement_date)
                    accrued_denominator = denominator
                    self.accrued_period = accrued_numerator/accrued_denominator
                    self.accrued_days = accrued_numerator
                    self.accrued_interest = self.cash_flow_amounts[0]*self.accrued_period
                else:
                    self.accrued_period = 0
                    self.accrued_days = 0
                    self.accrued_interest = 0

            elif self.day_count_30_360 == "30/360":
                numerator = day_count_30_360(self.settlement_date,self.first_coupon_date)
                denominator = 360/coupon_frequency_modifier
                self.discount_period = numerator/denominator
                if self.first_coupon_type == "FULL SHORT FIRST":
                    accrued_numerator = day_count_actual_actual(self.accrual_start_date,self.settlement_date)
                    accrued_denominator = denominator
                    self.accrued_period = accrued_numerator/accrued_denominator
                    self.accrued_days = accrued_numerator
                    self.accrued_interest = self.cash_flow_amounts[0]*self.accrued_period
                else:
                    self.accrued_period = 0
                    self.accrued_days = 0
                    self.accrued_interest = 0

            elif self.day_count_30E_360 == "30E/360":
                numerator = day_count_30E_360(self.settlement_date,self.first_coupon_date)
                denominator = 360/coupon_frequency_modifier
                self.discount_period = numerator/denominator
                if self.first_coupon_type == "FULL SHORT FIRST":
                    accrued_numerator = day_count_actual_actual(self.accrual_start_date,self.settlement_date)
                    accrued_denominator = denominator
                    self.accrued_period = accrued_numerator/accrued_denominator
                    self.accrued_days = accrued_numerator
                    self.accrued_interest = self.cash_flow_amounts[0]*self.accrued_period
                else:
                    self.accrued_period = 0
                    self.accrued_days = 0
                    self.accrued_interest = 0
        
        self.discount_periods = []
        for i in range(self.number_of_periods):
            self.discount_periods.append(self.discount_period+i)

        #Adjusting first coupon if it's a full short first
        if self.first_coupon_type == "FULL SHORT FIRST":
            self.cash_flow_amounts[0] = self.coupon_payment
        elif self.first_coupon_type != "REGULAR":
            self.cash_flow_amounts[0] = self.coupon_payment * self.discount_period

        #generating a cash flow table and calculating reoffer cash price
        #table - coupon number / coupon date / cash flow / discount rate / discount period / npv
        df = pd.DataFrame(np.column_stack([self.cash_flow_periods, self.cash_flow_dates, self.cash_flow_amounts, self.discount_rates, self.discount_periods]), 
                               columns=['coupon number', 'coupon_date', 'cash_flow', 'discount_rate', 'discount_period'])
        df['npv'] = (df.cash_flow / (df.discount_rate**df.discount_period))

        self.cash_flow_table = df
        self.reoffer_price = (self.cash_flow_table.npv.sum()/self.face_value)*100
        self.dirty_price = self.reoffer_price + (self.accrued_interest/self.face_value)


##################################################################################
#Using the class
##################################################################################
issue_date = dt.date(2019,1,8)
settlement_date = dt.date(2019,1,15)
first_coupon_date = dt.date(2019,6,22)
maturity_date = dt.date(2029,6,22)
face_value = 1000
reoffer_yield = 0.944
coupon_rate = 0.9
first_coupon_type = "ODD"
coupon_frequency = "ANNUAL"
day_count_convention = "ACTUAL/ACTUAL"
redemption_rate = 100

test_bond = fixed_bond(issue_date,settlement_date,first_coupon_date, maturity_date,face_value,reoffer_yield,coupon_rate,first_coupon_type,coupon_frequency,day_count_convention,redemption_rate)

print(test_bond.cash_flow_table)
print(f"Reoffer clean price is: {round(test_bond.reoffer_price,3)}%")
print(f"Days of accrued interest: {test_bond.accrued_days}")
print(f"Reoffer dirty price is: {round(test_bond.dirty_price,3)}%")

##################################################################################
#List of inputs
##################################################################################
#issue_date, settlement_date, first_coupon_date,maturity_date = datetime objects (yyyy,m,d)
#face_value = float
#reoffer_yield = for example, a reoffer yield of 2.3% is entered as 2.3
#coupon_rate = for example, a coupon of 2.25% is entered as 2.25
#first_coupon_type = string: REGULAR, ODD, FULL SHORT FIRST
#coupon_frequency = string: ANNUAL, SEMI-ANNUAL, QUARTERLY, MONTHLY
#day_count_convention = string: ACTUAL/ACTUAL, ACTUAL/365, ACTUAL/360, 30/360, 30E/360
#redemption_rate = for example, a redemption rate of 100% is entered as 100
