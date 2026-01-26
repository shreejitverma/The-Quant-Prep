#!/usr/bin/env python3
"""Bond Calculator with associated functions.

This script allows the user to calculate the Yield-to-Maturity, Price, Duration, or Convexity of a bond.
It is operated purely through a Command Line Interface (CLI).
"""

from pyfiglet import Figlet
import numpy as np
from scipy.optimize import newton

__author__ = "Shreyas V. Srinivasan"
__credits__ = ["Shreyas V. Srinivasan", "Deborah J. Lucas"]

__version__ = "1.2.4"
__maintainer__ = "Shreyas V. Srinivasan"
__email__ = "shreyass@alum.mit.edu"
__status__ = "Production"


def _weighted_cash_flows(coefficients : np.array, coupon : float = 0.0, face : float = 100.00, freq : int = 1, maturity : int = 1) -> float:
    """Calculates the weighted average of a series of bond cash flows.

    Parameters
    ----------
    coefficients : np.array
        Coefficients by which to weight the bond's cash flows when taking the average.
    coupon : float = 0.0
        The annual coupon rate of the bond.
    face : float = 100.00
        The bond's face value.
    freq : int = 1
        The number of compounding periods in a year.
    maturity : int = 1
        The bond's maturity, in years.

    Returns
    -------
    float
        The weighted average of a series of bond cash flows.
    """

    cf = np.array([(coupon/freq)*face] * (freq*maturity)) # Compute nominal future cash flows
    cf[-1] += face # Account for principal repayment in last period

    return np.dot(cf, coefficients)


def _npv_cash_flows(discount: float = 0.0, coupon: float = 0.0, face: float = 100.00, nper: int = 1) -> float:
    """Calculates the net present value of a bond's cash flows.

    Parameters
    ----------
    discount : float = 0.0
        The discount rate for the cash flows (equivalently, the bond's yield)
    coupon : float = 0.0
        The per-period coupon rate of the bond.
    face : float = 100.00
        The bond's face value, or principal amount repaid at maturity.
    nper : int = 1
        The number of payment periods.

    Returns
    -------
    float
        The present value (PV) of the bond's cash flows.
    """

    coefficients = np.fromfunction(lambda i: 1/(1 + discount)**(i + 1), (nper,), dtype=int)

    return _weighted_cash_flows(coefficients=coefficients, coupon=coupon, face=face, maturity=nper)


def _ytm() -> float:
    """Calculates a bond's Yield-to-Maturity (YTM).

    Acquires all necessary parameters through command line input.

    Returns
    -------
    float
        The YTM of the desired bond, as a decimal.
    """

    price = float(input("> Bond price: $"))
    nper = int(input("> Number of payment periods: "))
    face = float(input("> Face value: $"))
    coupon = float(input("> Coupon %age per period (enter as number, e.g., '5' for 5%): "))/100

    return newton(lambda y: _npv_cash_flows(y, coupon, face, nper) - price, 0.05) # Use Newton's method to equate cash flows (as function of YTM) to price


def _price() -> float:
    """Calculates a bond's price.

    Acquires all necessary parameters through command line input.

    Returns
    -------
    float
        The price of the desired bond.
    """
    
    face = float(input("> Face value: $"))
    apr = float(input("> APR (enter as number, e.g., '5' for 5%): "))/100
    coupon = float(input("> Annual coupon rate (enter as number, e.g., '5' for 5%): "))/100
    freq = int(input("> Coupon payments per year: "))
    years = int(input("> Years to maturity: "))

    return _npv_cash_flows(apr/freq, coupon/freq, face, freq*years)


def _macaulay_duration(apr : float = 0.0, coupon : float = 0.0, face : float = 100.00, freq : int = 1, maturity : int = 1, price : float = 100.00) -> float:
    """Calculates the Macaulay Duration of a bond.

    Parameters
    ----------
    apr : float = 0.0
        The bond's APR, or the value y in the Macaulay Duration formula.
    coupon : float = 0.0
        The annual coupon rate of the bond.
    face : float = 100.00
        The bond's face value.
    freq : int = 1
        The number of compounding periods in a year, or the value k in the Macaulay Duration formula.
    maturity : int = 1
        The bond's maturity, in years.
    price : float = 100.00
        The bond price, the value P_B in the Macaulay Duration formula.

    Returns
    -------
    float
        The Macaulay Duration of the bond.
    """

    coefficients = np.fromfunction(lambda t: ((t+1)/freq)*((1 + (apr/freq))**(-(t+1)))/price, (freq*maturity,), dtype=int) # Compute weighting for CFs from Macaulay Duration formula

    return _weighted_cash_flows(coefficients, coupon, face, freq, maturity)


def _convexity(apr : float = 0.0, coupon : float = 0.0, face : float = 100.00, freq : int = 1, maturity : int = 1, price : float = 100.00) -> float:
    """Calculates the convexity of an option-free bond.

    Parameters
    ----------
    apr : float = 0.0
        The bond's APR, or the value y in the Macaulay Duration formula.
    coupon : float = 0.0
        The annual coupon rate of the bond.
    face : float = 100.00
        The bond's face value.
    freq : int = 1
        The number of compounding periods in a year, or the value k in the Macaulay Duration formula.
    maturity : int = 1
        The bond's maturity, in years.
    price : float = 100.00
        The bond price, the value P_B in the Macaulay Duration formula.

    Returns
    -------
    float
        The convexity of the bond.
    """

    coefficients = np.fromfunction(lambda t: (((t+1)*(t+2))/((1 + (apr/freq))**(t+3)*(freq**2)))/price, (freq*maturity,), dtype=int) # Compute weighting for CFs from Convexity formula

    return _weighted_cash_flows(coefficients, coupon, face, freq, maturity)


def _duration_convexity() -> tuple:
    """Calculates the Macaulay Duration, modified duration, and convexity of a bond.

    Acquires all necessary parameters through command line input.

    Returns
    -------
    tuple
        The Macaulay Duration, modified duration, and convexity of a bond, in this order.
    """
    
    n = int(input("> Years to maturity: "))
    freq = int(input("> Coupon payments per year: "))
    coupon = float(input("> Annual coupon rate (enter as number, e.g., '5' for 5%): "))/100
    face = float(input("> Face value: $"))
    yld = float(input("> Bond Equivalent Yield (enter as number, e.g., '5' for 5%): "))/100

    price = _npv_cash_flows(yld/freq, coupon/freq, face, freq*n)

    d = _macaulay_duration(yld, coupon, face, freq, n, price)
    d_m = d/(1 + (yld/freq))
    c_0 = _convexity(yld, coupon, face, freq, n, price)
    return d, d_m, c_0


if __name__ == '__main__':
    f = Figlet(font='slant')
    print(f.renderText('Bond Calculator'))

    exit = False
    while(not exit):
        print("---------------------------------------------")
        print("Please select one of the following functions:")
        print("    1. Yield to Maturity")
        print("    2. Price")
        print("    3. Duration & Convexity")
        try:
            choice = int(input("Enter your choice as a number: "))
        except:
            choice = 0

        if choice == 1:
            print("    | Yield to Maturity: {:.2f}%".format(100*_ytm()))
        elif choice == 2:
            print("    | Price: ${:.2f}".format(_price()))
        elif choice == 3:
            d, d_m, c_0 = _duration_convexity()
            print("    | Macaulay Duration: {:.4f}".format(d))
            print("    | Modified Duration: {:.4f}".format(d_m))
            print("    | Convexity: {:.4f}".format(c_0))
        else:
            print("Choice must be within the range 1 - 3.")

        exit = (input("Press 'x' to exit or any key to continue: ").strip() == "x")
