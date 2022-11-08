# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 17:30:46 2021

@author: Teo Bee Guan
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="Financial Planning Calculator")

st.title("Financial Planning Calculator")

st.header("**Monthly Income**")
st.subheader("Salary")
colAnnualSal, colTax = st.beta_columns(2)

with colAnnualSal:
    salary = st.number_input("Enter your annual salary($): ", min_value=0.0, format='%f')
with colTax:
    tax_rate = st.number_input("Enter your tax rate(%): ", min_value=0.0, format='%f')

tax_rate = tax_rate / 100.0
salary_after_taxes = salary * (1 - tax_rate)
monthly_takehome_salary = round(salary_after_taxes / 12.0, 2)

st.header("**Monthly Expenses**")
colExpenses1, colExpenses2 = st.beta_columns(2)

with colExpenses1:
    st.subheader("Monthly Rental")
    monthly_rental = st.number_input("Enter your monthly rental($): ", min_value=0.0,format='%f' )
    
    st.subheader("Daily Food Budget")
    daily_food = st.number_input("Enter your daily food budget ($): ", min_value=0.0,format='%f' )
    monthly_food = daily_food * 30
    
    st.subheader("Monthly Unforeseen Expenses")
    monthly_unforeseen = st.number_input("Enter your monthly unforeseen expenses ($): ", min_value=0.0,format='%f' ) 
    
with colExpenses2:
    st.subheader("Monthly Transport")
    monthly_transport = st.number_input("Enter your monthly transport fee ($): ", min_value=0.0,format='%f' )   
    
    st.subheader("Monthly Utilities Fees")
    monthly_utilities = st.number_input("Enter your monthly utilities fees ($): ", min_value=0.0,format='%f' )
    
    st.subheader("Monthly Entertainment Budget")
    monthly_entertainment = st.number_input("Enter your monthly entertainment budget ($): ", min_value=0.0,format='%f' )   

monthly_expenses = monthly_rental + monthly_food + monthly_transport + monthly_entertainment + monthly_utilities + monthly_unforeseen
monthly_savings = monthly_takehome_salary - monthly_expenses 

st.header("**Savings**")
st.subheader("Monthly Take Home Salary: $" + str(round(monthly_takehome_salary,2)))
st.subheader("Monthly Expenses: $" + str(round(monthly_expenses, 2)))
st.subheader("Monthly Savings: $" + str(round(monthly_savings, 2)))

st.markdown("---")

st.header("**Forecast Savings**")
colForecast1, colForecast2 = st.beta_columns(2)
with colForecast1:
    st.subheader("Forecast Year")
    forecast_year = st.number_input("Enter your forecast year (Min 1 year): ", min_value=0,format='%d')
    forecast_months = 12 * forecast_year 
    
    st.subheader("Annual Inflation Rate")
    annual_inflation = st.number_input("Enter annual inflation rate (%): ", min_value=0.0,format='%f')
    monthly_inflation = (1+annual_inflation)**(1/12) - 1
    cumulative_inflation_forecast = np.cumprod(np.repeat(1 + monthly_inflation, forecast_months))
    forecast_expenses = monthly_expenses*cumulative_inflation_forecast
with colForecast2:
    st.subheader("Annual Salary Growth Rate")
    annual_growth = st.number_input("Enter your expected annual salary growth (%): ", min_value=0.0,format='%f')
    monthly_growth = (1 + annual_growth) ** (1/12) - 1
    cumulative_salary_growth = np.cumprod(np.repeat(1 + monthly_growth, forecast_months))
    forecast_salary = monthly_takehome_salary * cumulative_salary_growth 
    
forecast_savings = forecast_salary - forecast_expenses 
cumulative_savings = np.cumsum(forecast_savings)

x_values = np.arange(forecast_year + 1)

fig = go.Figure()
fig.add_trace(
        go.Scatter(
            x=x_values, 
            y=forecast_salary,
            name="Forecast Salary"
        )
    )

fig.add_trace(
        go.Scatter(
            x=x_values,
            y=forecast_expenses,
            name= "Forecast Expenses"
        )
    )

fig.add_trace(
        go.Scatter(
                x=x_values, 
                y=cumulative_savings,
                name= "Forecast Savings"
            )
    )
fig.update_layout(title='Forecast Salary, Expenses & Savings Over the Years',
                   xaxis_title='Year',
                   yaxis_title='Amount($)')

st.plotly_chart(fig, use_container_width=True)









