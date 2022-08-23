import datetime
from tkinter import N
from typing import Any
from xmlrpc.client import DateTime
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
md = """---"""


st.title('Fire tests analysis tool')
st.markdown('This application is a Streamlit dashboard that can be used'
            ' to analyze raw data results of conducted fire tests.')
st.markdown(md)
st.subheader("Upload raw fire test report in xlsx file")


#Upload fire report
uploaded_file = st.file_uploader("Choose a report file")

if uploaded_file is not None:
    raw_data = pd.ExcelFile(uploaded_file)
    sheet_list = raw_data.sheet_names
    st.markdown(md)
    
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
st.markdown(md)


#Select single column
st.subheader('Select column')
selected_col = st.selectbox('Select one column', df.columns[1:])
new_columns = ['Time (s)']
new_columns.append(selected_col)

graph_data = pd.DataFrame(df[new_columns])
if st.checkbox(f'Show graph data', value= False):
    st.write(graph_data)
st.markdown(md)


#Plot graph
st.title("Plot single line graph")
title = st.text_input("Graph title")

if title is not '':
    new_plot = px.line(graph_data, x='Time (s)', y=selected_col, 
                        title= title, hover_data=['Time (s)', selected_col])
    new_plot.add_hline(y=180, line_dash="dot",
                        annotation_text="180 deg", annotation_position= "bottom right",
                        line_color= "red")
    st.write(new_plot)
st.markdown(md)


#Select multiple columns
st.title("Plot multi line graph")
if st.checkbox(f'Create plot for multiple columns', value= True):
        all_columns = st.checkbox('Select all columns')
        if all_columns:
            columns = df.columns
            st.table(columns)
        else:
            st.subheader("Select columns, remember to add: 'Time (s)'")
            columns = st.multiselect('Select columns:', df.columns, default=None)
            confirm_btn_2 = st.button('Apply')
            if confirm_btn_2 == True:
                st.table(columns)

        st.markdown(md)
        #Section: Plot graph for selected columnd
        graph_data = pd.DataFrame(df[columns])
        
        
        title_multi = st.text_input("Mutiline graph title")
        
        if title_multi is not '':
            plot = px.line(graph_data, x='Time (s)', y=graph_data.columns, 
                            title= title_multi, hover_data=['Time (s)'])
            plot.add_hline(y=180, line_dash="dot",
                            annotation_text="180 deg", annotation_position= "bottom right", line_color="red")
            st.write(plot)



#Show/hide raw data frame
st.markdown(md)
st.subheader("Diaplay raw data")
if st.checkbox(f'Show selected data from: {selected_sheet} sheet', value= False):
    st.write(df)

