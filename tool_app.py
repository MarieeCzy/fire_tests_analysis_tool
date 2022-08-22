import datetime
from tkinter import N
from typing import Any
from xmlrpc.client import DateTime
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('Fire tests analysis tool')
st.markdown('This application is a Streamlit dashboard that can be used'
            ' to analyze raw data results of conducted fire tests.')
st.markdown("""---""")
st.subheader("Upload raw fire test report in xlsx file")

#Section: Upload fire report
uploaded_file = st.file_uploader("Choose a report file")

if uploaded_file is not None:
    raw_data = pd.ExcelFile(uploaded_file)
    sheet_list = raw_data.sheet_names
    st.markdown("""---""")

    #Choose sheet
    st.subheader('Available sheets to analyze')
    selected_sheet = st.radio('Choose: ', sheet_list)
    
    def create_df():
        df = raw_data.parse(selected_sheet)
        #convert time in s to time in format hh:mm:ss
        for _ in df['Time (s)']:
            df['Time (s)'][_] = str(datetime.timedelta(seconds=_))
        return df
    
    df = create_df()

st.markdown("""---""")

#Section: Select columns
st.subheader('Select columns')

all_columns = st.checkbox('Select all columns')
if all_columns:
    columns = df.columns[1:]
    st.table(columns)
else:
    columns = st.multiselect('Select columns:', df.columns, default=None)
    confirm_btn = st.button('Apply')
    if confirm_btn == True:
        st.table(columns)
st.markdown("""---""")

#Section: Plot graph for selected columns
graph_data = pd.DataFrame(df[columns])

st.subheader("Plot graph")
title = st.text_input("Graph title")
plot_btn = st.button('Plot!')

if (title is not '') & (plot_btn == True):
    plot = px.line(graph_data, title= title, hover_data=[])
    st.write(plot)


#Show/hide raw data frame
st.markdown("""---""")
st.subheader("Diaplay raw data")
if st.checkbox(f'Show selected data from: {selected_sheet} sheet', value= False):
    st.write(df)

