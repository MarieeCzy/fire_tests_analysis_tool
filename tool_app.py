import datetime
from dis import dis
from tkinter import N
from tokenize import Single
from typing import Any
from xmlrpc.client import DateTime
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
md = """---"""

st.set_page_config(
    page_title='FläktGroup analysis tool', page_icon='📊', initial_sidebar_state='expanded'
)

def create_df(selected_sheet):
    df = raw_data.parse(selected_sheet)
    #convert time in s to time in format hh:mm:ss
    try:
        for _ in df['Time (s)']:
            df['Time (s)'][_] = str(datetime.timedelta(seconds=_))
    except:
        st.error('Select the worksheet containing the Time (s) column') 
    return df

def h_slider(data):
    max_value = int(graph_data.max().max())
    min_value = int(graph_data.min().min())
    avr_value = int((max_value + min_value)/2)
    
    horizontal_value = st.slider(
        'Select value for horizontal line',
        min_value, max_value, avr_value
    )
    return horizontal_value

def plot(
    data, y_value, title: str, hover_data, h_line_value: int, h_line_text: str):
    new_plot = px.line(
        data, x='Time (s)', y=y_value, title= title, hover_data=hover_data
    )
    new_plot.add_hline(
        y=h_line_value, line_dash="dot", annotation_text=h_line_text, 
        annotation_position= "bottom right", line_color= "red",
    )
    return new_plot

st.write(
    '''
# 📊 Fire tests analysis tool
This application is a Streamlit dashboard that can be used
to analyze raw data results of conducted fire tests.
\nUpload raw fire test report.
    '''
)


uploaded_file = st.file_uploader('Upload .xlsx file', type='.xlsx')

use_example_file = st.checkbox(
    'Use example file', False, help='Use built-in example file to demo app'
)

# If CSV is not uploaded and checkbox is filled, use values from the example file
# and pass them down to the next if block
if use_example_file:
    uploaded_file = 'data/example_FT000.xlsx'

if uploaded_file:
    raw_data = pd.ExcelFile(uploaded_file)
    sheet_list = raw_data.sheet_names
    st.markdown(md)

    st.subheader('Available sheets to analyze')
    selected_sheet = st.radio('Choose: ', sheet_list)
    df = create_df(selected_sheet)
    st.markdown(md)

#Analysis of a single record or multiple records
if uploaded_file != None:
    left, right = st.columns(2)
    with left:
        single = st.checkbox(
            'Single-line plot', False, help='Choose if you want analyze one parameter',
            disabled=False
    )
    with right:
        multi = st.checkbox(
            'Multi-line plot', False, help='Choose if you want analyze more than one parmeter',
            disabled=False
    )

    if single:
        #Select single column
        st.subheader('Select column')
        selected_col = st.selectbox(
            'Select one column', df.columns[1:]
        )

        new_columns = ['Time (s)']
        new_columns.append(selected_col)
        graph_data = pd.DataFrame(df[new_columns])

        if st.checkbox(f'Show graph data', value= False):
            st.write(graph_data.head())
            st.markdown(md)

        #Plot graph
        st.title("Plot single line graph")
        graph_title = st.text_input("Graph title")

        if graph_title is not '':
            h_line_slider_value = h_slider(graph_data)
            graph = plot(
                graph_data, selected_col, graph_title, ['Time (s)', selected_col], h_line_slider_value, f'{h_line_slider_value} deg'
            )
            st.write(graph)
            st.markdown(md)

    elif multi:
        #Select multiple columns
        st.markdown(md)
        st.title(
            "Plot multi line graph"
        )
        
        all_columns = st.checkbox('Select all columns')
        if all_columns:
            columns = df.columns
        else:
            st.subheader("Select columns, remember to add: 'Time (s)'")
            columns = st.multiselect('Select columns:', df.columns, default=None)
            confirm_btn_2 = st.button('Apply')
            if confirm_btn_2 == True:
                st.table(columns)
                st.markdown(md)
                
        graph_data = pd.DataFrame(df[columns])
        graph_title = st.text_input("Mutiline graph title")
        
        if graph_title is not '':
            h_line_slider_value = h_slider(graph_data)
            graph = plot(
                graph_data, graph_data.columns, graph_title, ['Time (s)'], h_line_slider_value, f'{h_line_slider_value} deg'
            )
            st.write(graph)


#Show/hide raw data frame
    st.subheader("Diaplay raw data")
    if st.checkbox(f'Show selected data from: {selected_sheet} sheet', value= False):
        st.write(df)

