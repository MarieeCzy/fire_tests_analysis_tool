import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('Fire tests analysis tool')
st.markdown('This application is a Streamlit dashboard that can be used'
            ' to analyze raw data results of conducted fire tests.')

st.subheader("Upload raw fire test report in xlsx file")

uploaded_file = st.file_uploader("Choose a report file")

if uploaded_file is not None:
    raw_data = pd.ExcelFile(uploaded_file)
    sheet_list = raw_data.sheet_names

    #Choose sheet
    selected_sheet = st.radio('Available sheets to analyze:', sheet_list)
    st.write(f'Selected: {selected_sheet}')
    df = raw_data.parse(selected_sheet)

    if st.checkbox(f'Show selected data from: {selected_sheet} sheet', True):
        st.write(df)