import pandas as pd
import numpy as np
import plotly.express as px
import datetime
import time
import matplotlib.pyplot as plt
import copy
import streamlit as st
import os
from sqlalchemy import create_engine #to access a sql database

engine = create_engine('postgresql://lectura:ncorrea#2022@138.100.82.178:5432/2207')
df = pd.read_sql_query("SELECT id_var, date, value FROM variable_log_float WHERE id_var = 575 LIMIT 800", con=engine)
# Convert the values in the "date" column to datetime objects
df["date"] = pd.to_datetime(df["date"], unit="ms")


# Shift the "value" column by one row and store it in a new column called "prev_value"
# Use the fill_value parameter to specify a default value to use for the shifted rows
df["prev_value"] = df["value"].shift(fill_value=df["value"].iloc[0])

# Create an empty list to store the data for the Gantt chart
data = []

# Select the rows where the "value" changes from 255 to 0 or vice versa
rows = df.where((df["value"] == 0) & (df["prev_value"] == 255) | (df["value"] == 255) & (df["prev_value"] == 0))

#Iterate through the selected rows and create the data for the Gantt chart
for index, row in rows.iterrows():
    status = "on" if row["value"] == 255 else "off"
    start = row["date"]
    finish = df["date"].shift(-1).iloc[index]
    data.append({"status": status, "start": start, "finish": finish})


# Create the Gantt chart using the data
fig = px.timeline(data, x_start="start", x_end="finish", y="status")


#Show the Gantt chart

#fig.show()                    #FORVISUALSTUDIOCODE

st.plotly_chart(fig)

