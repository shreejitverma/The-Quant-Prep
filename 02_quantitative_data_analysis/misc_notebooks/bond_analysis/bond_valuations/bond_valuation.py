# Import built-in libraries
from datetime import datetime, date, timedelta
import os

# Install and import external libraries
os.system("pip install -r requirements.txt")
import numpy as np
import pandas as pd


class BondCalculations:
    """
    Summary
    ===========
    Computes future cash flows, value of the bond, current yield and approximated yield to maturity of a bond.

    Parameters
    ===========
    principal_amount: a float
        par value (or principal amount or the face value) of the bond
        Example: if the face value is $100, then principal_amount = 100
    coupon_rate: a float
        percentage of coupon rate. The amount of interest paid by the issuer.
        Example: if coupon rate is 5%, then coupon_rate = 0.05
    bond_issue_date: a string
        Bond issue date
        Example: If the bond was issued on 25th February 2000, then bond_issue_date = "2000-02-25"
    bond_maturity_date: a string
        Bond maturity (expiry) date
        Example: If the bond gets expired on 24th February 2020, then bond_maturity_date = "2020-02-24"
    discount_rate: a float
        The coupon rate is fixed for the bond when it gets issued. Discount rate is the current interest rate available in the market which could be inflation rate OR minimum expected rate of return from bonds of similar quality or credit rating.
        Example: If the yield is 4%, then discount_rate = 0.04
    coupon_payment_frequency: a string
        It is interest payment frequency and it takes any value: 'annually', 'semi-annually', 'quarterly', 'monthly' , 'weekly', 'daily'
        Example: coupon_payment_frequency = 'annually' (default)
        
    """
    
    def __init__(self,
                 principal_amount: np.float,
                 coupon_rate: np.float,
                 bond_issue_date: np.str,
                 bond_maturity_date: np.str,
                 discount_rate: np.float,
                 coupon_payment_frequency: np.str = 'annual'):
        
        self.principal_amount = principal_amount
        self.coupon_rate = coupon_rate
        self.bond_issue_date = datetime.strptime(bond_issue_date, '%Y-%m-%d').date()
        self.bond_maturity_date = datetime.strptime(bond_maturity_date, '%Y-%m-%d').date()
        self.discount_rate = discount_rate
        self.coupon_payment_frequency = coupon_payment_frequency
        # setting the current date (cd)
        self.cd = date.today() if date.today() >= self.bond_issue_date else self.bond_issue_date
        self.payments_per_year = {
            'annually'     : 1,
            'semi-annually': 2,
            'quarterly'    : 4,
            'monthly'      : 12,
            'weekly'       : 52,
            'daily'        : 365
        }

    def present_value(self, 
                      row: pd.Series) -> np.float:
        """
        This is used in the method "bond_value()" to calculate the present value from future date and amount.
        fd = future date
        fv = future value
        n = no. of years
        t = no. of times compounded in a year
        pv = present value
        """
        fd = row['receivable_date']
        fv = row['receivable_amount']
        n = (fd - self.cd).days / 365
        t = self.payments_per_year[self.coupon_payment_frequency]
        pv = fv / ((1 + (self.discount_rate / t)) ** (n * t))
        return pv

    def bond_value(self) -> (pd.DataFrame, np.float):
        """
        Summary
        ===========
        Computes future cash flows and the value of the bond (expected selling price).
        
        Returns
        ========
        A tuple with two elements:
            a dataframe: contains all the cash flows
            a float: value of the bond
        
        Calculation
        ===========
        The present value of a bond is: sum of present value (PV) of all future interest payments receivable and present value (PV) of future principal amount receivable.
        The calculation assumes that the coupon payment received is reinvested as they are received.
        """
        no_of_days_btw_payments = (365 / self.payments_per_year[self.coupon_payment_frequency])
        no_of_periods = np.floor((self.bond_maturity_date - self.bond_issue_date).days / no_of_days_btw_payments) + 1
        periods = [self.bond_issue_date + timedelta(days = (i * no_of_days_btw_payments)) for i in np.arange(no_of_periods)]
        
        # The maturity date will be last period in the periods list
        self.bond_maturity_date = periods[-1]
        
        df = pd.DataFrame({
            'receivable_date'  : periods,
            'receivable_amount': (self.principal_amount * self.coupon_rate) / self.payments_per_year[self.coupon_payment_frequency]
        })
    
        # Keeping only those dates where the coupon payment will be received
        df = df[df['receivable_date'] > self.cd]
    
        # On the maturity date, along with final coupon payment, the principal amount will also be received.
        df.loc[df.index.max(), 'receivable_amount'] += self.principal_amount
    
        df['present_value'] = df.apply(func = self.present_value, axis = 1)
    
        return df, round(df['present_value'].sum(), 0)
    
    def yield_calculations(self, 
                           current_bond_price: np.float) -> (np.float, np.float):
        """
        Summary
        =======
        Computes current yield and approximated yield to maturity of the bond.
        Current yield
            return earned if held the bond for a year.
        Yield to maturity
            return earned if held the bond till maturity.
        
        Parameters
        ==========
        current_bond_price: a float
            The current market price of the bond.
            Example: If the current market price of the bond is 127.25, then current_bond_price = 127.25
        
        Returns
        =======
        A tuple with two elements:
            a float: current_yield
            a float: approximated yield to maturity
        
        Calculation
        ===========
                          r * F
        Current yield = ---------
                            P
        
                             F - P
                        C + -------
                               n
        Approx. YTM = ------------------
                             F + P
                            -------
                               2
        where:
            r = coupon rate
            F = principal amount
            P = current bond price
            C = interest received per year
            n = no of years left
        """
        current_yield = (self.coupon_rate * self.principal_amount) / current_bond_price

        receivable_per_year = self.principal_amount * self.coupon_rate
        no_of_year_left = (self.bond_maturity_date - self.cd).days / 365
        yield_to_maturity = (receivable_per_year + ((self.principal_amount - current_bond_price) / no_of_year_left)) / ((self.principal_amount + current_bond_price) / 2)
        return round(current_yield, 5), round(yield_to_maturity, 5)


def user_input_and_checks():
    """
    This function will ask the user to enter the necessary details about the bond.
     It then checks if the entered values are valid.
     If not, it will repeatedly asks until a valid value is given.
    
    Returns
    ========
    a dictionary
    """
    valid_inputs = {'face_value': None,
                    'issue_date': None,
                    'maturity_date': None,
                    'coupon_rate': None,
                    'discount_rate': None,
                    'coupon_frequency': None,
                    'current_market_price': None}
    face_value_valid = -1
    while face_value_valid == -1:
        face_value = input('Enter the face value of the bond (e.g. if £100,000, then type 100000): ')
        try:
            valid_inputs['face_value'] = np.float(face_value)
            face_value_valid = 1
        except Exception as _:
            print('Invalid entry !! Try again !!')
            pass
    issue_date_valid = -1
    while issue_date_valid == -1:
        issue_date = input('Enter the bond issue date (e.g. 2020-12-22): ')
        try:
            datetime.strptime(issue_date, '%Y-%m-%d').date()
            valid_inputs['issue_date'] = issue_date
            issue_date_valid = 1
        except Exception as _:
            print('Invalid entry !! Try again !!')
            pass
    maturity_date_valid = -1
    while maturity_date_valid == -1:
        maturity_date = input('Enter the bond maturity date (e.g. 2020-12-22): ')
        try:
            datetime.strptime(maturity_date, '%Y-%m-%d').date()
            valid_inputs['maturity_date'] = maturity_date
            if datetime.strptime(valid_inputs['maturity_date'], '%Y-%m-%d') < datetime.strptime(valid_inputs['issue_date'], '%Y-%m-%d'):
                print('Bond maturity date should not be less than bond issue date !!')
                print('Invalid entry !! Try again !!')
            else:
                maturity_date_valid = 1
        except Exception as _:
            print('Invalid entry !! Try again !!')
            pass
    coupon_rate_valid = -1
    while coupon_rate_valid == -1:
        coupon_rate = input('Enter the coupon rate (e.g. if 7%, then type 0.07): ')
        try:
            valid_inputs['coupon_rate'] = np.float(coupon_rate)
            coupon_rate_valid = 1
        except Exception as _:
            print('Invalid entry !! Try again !!')
            pass
    discount_rate_valid = -1
    while discount_rate_valid == -1:
        discount_rate = input('Enter the discount rate (e.g. if 6%, then type 0.06): ')
        try:
            valid_inputs['discount_rate'] = np.float(discount_rate)
            discount_rate_valid = 1
        except Exception as _:
            print('Invalid entry !! Try again !!')
            pass
    coupon_frequency_valid = -1
    while coupon_frequency_valid == -1:
        coupon_frequency = input("Enter the coupon payment frequency (options: annually, semi-annually, quarterly, monthly, weekly, daily): ")
        if coupon_frequency in ['annually', 'semi-annually', 'quarterly', 'monthly', 'weekly', 'daily']:
            valid_inputs['coupon_frequency'] = coupon_frequency
            coupon_frequency_valid = 1
        else:
            print('Invalid entry !! Try again !!')
    current_market_price_valid = -1
    while current_market_price_valid == -1:
        current_market_price = input("Enter the current market price of the bond (e.g. if £120,000, type 120000): ")
        try:
            valid_inputs['current_market_price'] = np.float(current_market_price)
            current_market_price_valid = 1
        except Exception as _:
            print('Invalid entry !! Try again !!')
            pass

    return valid_inputs


def main():
    user_inputs = user_input_and_checks()
    bc = BondCalculations(
        principal_amount = user_inputs['face_value'],
        coupon_rate = user_inputs['coupon_rate'],
        bond_issue_date = user_inputs['issue_date'],
        bond_maturity_date = user_inputs['maturity_date'],
        discount_rate = user_inputs['discount_rate'],
        coupon_payment_frequency = user_inputs['coupon_frequency'])
    cf, bv = bc.bond_value()
    cy, ytm = bc.yield_calculations(current_bond_price = user_inputs['current_market_price'])
    print(cf)
    print(f'Value of the bond is: {bv}')
    print(f'Current Yield is: {cy} or {round(cy * 100, 3)}%')
    print(f'Yield to maturity is: {ytm} or {round(ytm * 100, 3)}%')


if __name__ == '__main__':
    main()

