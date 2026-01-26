# Bond Valuations

Please feel free to use my code to compute the bond value, cash flows till the maturity, current yield and approximated yield to maturity of the bond.

# User guide

Firstly, run the `Bond valuation.py` which will install all necessary packages, import them and will create the class **BondValuation** in memory.


## 1. Bond value and cash flows

#### Example  
_A bond XYZ is issued on "2021-12-25" with the maturity date "2026-12-24" for a face value of £100,000 and coupon rate of 7% per annum to be paid semi-annually. If the current risk free return (discount rate) available in the market is 6.5% per annum, then what would be the value of the bond?_

```python
bc = BondCalculations(
    principal_amount = 100000,
    coupon_rate = 0.07,
    bond_issue_date = '2021-12-25',
    bond_maturity_date = '2026-12-24',
    discount_rate = 0.065,
    coupon_payment_frequency = 'semi-annually')

cash_flow, value_of_bond = bc.bond_value()

print(cash_flow)

   receivable_date  receivable_amount  present_value
1       2022-06-25             3500.0    3390.127555
2       2022-12-25             3500.0    3283.128822
3       2023-06-25             3500.0    3180.064424
4       2023-12-25             3500.0    3079.695674
5       2024-06-24             3500.0    2983.017476
6       2024-12-24             3500.0    2888.867895
7       2025-06-24             3500.0    2798.180186
8       2025-12-24             3500.0    2709.864413
9       2026-06-24             3500.0    2624.796005
10      2026-12-24           103500.0   75169.168548

print(value_of_bond)
102107.0

```
Since the tenure of the bond is 5 years and the interest amount paid is semi-annually, the cash flow table shows that the buyer will receive an amount of £3500 semi-annually. On the maturity or expiry date, in addition to the coupon amount of £3500, the face value value of the bond £100,000 will also be received.

The value of the bond is the sum of present values of all futures payments which came to £102,107. Since, the face value is £100,000 it will be therefore a bargain if you buy the bond.

#### Points to note  
* if bond value > market price of the bond, the bond is at a premium price  
* if bond value < market price of the bond, the bond is at a discount price  
* if bond value = market price of the bond, the bond is at a par value  



## 2. Current yield and Yield to maturity  

#### Example  
_Considering the same example above, if the market price for the bond is £110,000, then what is the current yield and yield to maturity of the bond?_

Current yield is the return earned if the bond is held for one year.
Yield to maturity is the return earned if the bond is held till maturity.

```python
current_yield, ytm = bc.yield_calculations(current_bond_price = 110000)

print(current_yield)
0.06364

print(ytm)
0.04762

```
The current yield is 0.06364 or 6.36% and the yield to maturity is 0.04762 or 4.76%.  
Even though the coupon rate is 7%, the current yield and yield to maturity are lower because the bond is available at a premium (£110,000 instead of £100,000).

#### Example  
_Considering the same example above, if the market price for the bond is £90,000, then what is the current yield and yield to maturity of the bond?_

```python
current_yield, ytm = bc.yield_calculations(current_bond_price = 90000)

print(current_yield)
0.07778

print(ytm)
0.09474

```
The current yield is 0.07778 or 7.78% and the yield to maturity is 0.09474 or 9.47%.  
Even though the coupon rate is 7%, the current yield and yield to maturity are higher because the bond is available at a discounted rate (£90,000 instead of £100,000).

#### Points to note  
* if bond coupon rate > YTM, the bond is at a premium price  
* if bond coupon rate < YTM, the bond is at a discount price  
* if bond coupon rate = YTM, the bond is at a par value  

## Notes  
* When comparing two bonds, choose the one with higher yield to maturity which indicates the higher profitability of the bond.
* Note that all my calculations assume that the coupon payments are reinvested as they are received.
* Also, the present value calculation relies on the start date:
    - if the bond was already issued, then the current date will be taken into account. 
    - if the bond will be issued in the near future, then the issue date will be taken into account.
    - Therefore, if you repeat my examples above, the output will be different since your current date is different from mine.



## Code execution via the terminal
Below is a demonstration of executing the code from a command line interface.
![Terminal execution](Images/terminal%20execution.png)




