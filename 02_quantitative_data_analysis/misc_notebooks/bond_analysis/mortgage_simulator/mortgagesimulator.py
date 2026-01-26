# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 17:12:17 2021

@author: Teo Bee Guan
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(
    page_title="Mortgage Loan Simulator")

st.title("Mortgage Loan Simulator")

st.header("**Mortgage Details**")
col1, col2 = st.beta_columns(2)

with col1:
    st.subheader("Home Value")
    home_value = st.number_input("Enter your home value($): ", min_value=0.0, format='%f')
    
    st.subheader("Loan Interest Rate")
    interest_rate = st.number_input("Enter your home loan interest rate(%): ", min_value=0.0, format='%f')

with col2:
    st.subheader("Down Payment Percent")
    down_payment_percent = st.number_input("Enter your down payment percent(%): ", min_value=0.0, format='%f')
    
    st.subheader("Target Payment Period (Years)")
    payment_years = st.number_input("Enter your target payment period (years): ", min_value=3, format='%d')
    

down_payment = home_value* (down_payment_percent / 100)
loan_amount = home_value - down_payment
payment_months = payment_years*12
interest_rate = interest_rate / 100
periodic_interest_rate = (1+interest_rate)**(1/12) - 1
monthly_installment = -1*np.pmt(periodic_interest_rate , payment_months, loan_amount)

st.subheader("**Down Payment:** $" + str(round(down_payment,2)))
st.subheader("**Loan Amount:** $" + str(round(loan_amount, 2)))
st.subheader("**Monthly Installment:** $" + str(round(monthly_installment, 2)))

st.markdown("---")

st.header("**Mortgage loan Amortization**")
principal_remaining = np.zeros(payment_months)
interest_pay_arr = np.zeros(payment_months)
principal_pay_arr = np.zeros(payment_months)

for i in range(0, payment_months):
    
    if i == 0:
        previous_principal_remaining = loan_amount
    else:
        previous_principal_remaining = principal_remaining[i-1]
        
    interest_payment = round(previous_principal_remaining*periodic_interest_rate, 2)
    principal_payment = round(monthly_installment - interest_payment, 2)
    
    if previous_principal_remaining - principal_payment < 0:
        principal_payment = previous_principal_remaining
    
    interest_pay_arr[i] = interest_payment 
    principal_pay_arr[i] = principal_payment
    principal_remaining[i] = previous_principal_remaining - principal_payment
    

month_num = np.arange(payment_months)
month_num = month_num + 1

principal_remaining = np.around(principal_remaining, decimals=2)

fig = make_subplots(
    rows=2, cols=1,
    vertical_spacing=0.03,
    specs=[[{"type": "table"}],
           [{"type": "scatter"}]
          ]
)

fig.add_trace(
        go.Table(
            header=dict(
                    values=['Month', 'Principal Payment($)', 'Interest Payment($)', 'Remaining Principal($)']
                ),
            cells = dict(
                    values =[month_num, principal_pay_arr, interest_pay_arr, principal_remaining]
                )
            ),
        row=1, col=1
    )

fig.add_trace(
        go.Scatter(
                x=month_num,
                y=principal_pay_arr,
                name= "Principal Payment"
            ),
        row=2, col=1
    )

fig.append_trace(
        go.Scatter(
            x=month_num, 
            y=interest_pay_arr,
            name="Interest Payment"
        ),
        row=2, col=1
    )

fig.update_layout(title='Mortgage Installment Payment Over Months',
                   xaxis_title='Month',
                   yaxis_title='Amount($)',
                   height= 800,
                   width = 1200,
                   legend= dict(
                           orientation="h",
                           yanchor='top',
                           y=0.47,
                           xanchor= 'left',
                           x= 0.01
                       )
                  )

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.header("**Home Equity (With Constant Market Value)**")

cumulative_home_equity = np.cumsum(principal_pay_arr)
cumulative_interest_paid = np.cumsum(interest_pay_arr)


fig = go.Figure()
fig.add_trace(
        go.Scatter(
            x=month_num, 
            y=cumulative_home_equity,
            name="Cumulative Home Equity"
        )
    )

fig.add_trace(
        go.Scatter(
            x=month_num, 
            y=cumulative_interest_paid,
            name="Cumulative Interest Paid"
        )
    )

fig.update_layout(title='Cumulative Home Equity Over Time',
                   xaxis_title='Month',
                   yaxis_title='Amount($)',
                   height= 500,
                   width = 1200,
                   legend= dict(
                           orientation="h",
                           yanchor='top',
                           y=0.98,
                           xanchor= 'left',
                           x= 0.01
                       )
                  )


st.plotly_chart(fig, use_container_width=True)


st.markdown("---")
st.header("**Forecast Growth**")

st.subheader("Forecast Growth (Per Year)")
forecast_growth = st.number_input("Enter your forecast growth rate(%): ",  format='%f')

growth_per_month = (forecast_growth / 12.0) / 100 
growth_array = np.full(payment_months, growth_per_month)
forecast_cumulative_growth = np.cumprod(1+growth_array)
forecast_home_value= home_value*forecast_cumulative_growth
cumulative_percent_owned = (down_payment_percent/100) + (cumulative_home_equity/home_value)
forecast_home_equity = cumulative_percent_owned*forecast_home_value

fig = go.Figure()
fig.add_trace(
        go.Scatter(
            x=month_num, 
            y=forecast_home_value,
            name="Forecast Home Value"
        )
    )

fig.add_trace(
        go.Scatter(
            x=month_num, 
            y=forecast_home_equity,
            name="Forecast Home Equity Owned"
        )
    )

fig.add_trace(
        go.Scatter(
            x=month_num, 
            y=principal_remaining,
            name="Remaining Principal"
        )
    )

fig.update_layout(title='Forecast Home Value Vs Forecast Home Equity Over Time',
                   xaxis_title='Month',
                   yaxis_title='Amount($)',
                   height= 500,
                   width = 1200,
                   legend= dict(
                           orientation="h",
                           yanchor='top',
                           y=1.14,
                           xanchor= 'left',
                           x= 0.01
                       )
                  )

st.plotly_chart(fig, use_container_width=True)

    

