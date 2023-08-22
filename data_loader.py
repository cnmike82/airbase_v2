import numpy as np
import pandas as pd
import streamlit as st
import os

def upload_airports():

    # Option to upload the csv file:
    uploaded_file = st.file_uploader("Upload the airport data", type = ['csv', 'xlsx'], label_visibility="collapsed")

    if uploaded_file is not None and uploaded_file.type == 'text/csv':
        airports = pd.read_csv(uploaded_file)
        
        return airports
    
    elif uploaded_file is not None and uploaded_file.type == 'text/xlsx':
        airports = pd.read_excel(uploaded_file)
        
        return airports

def upload_red_airports():

    # Option to upload the csv file:
    uploaded_file = st.file_uploader("Upload the red airport data", type = ['csv', 'xlsx'], label_visibility="collapsed")

    if uploaded_file is not None and uploaded_file.type == 'text/csv':
        airports = pd.read_csv(uploaded_file)
        
        return airports
    
    elif uploaded_file is not None and uploaded_file.type == 'text/xlsx':
        airports = pd.read_excel(uploaded_file)
        
        return airports

def upload_aircraft_ranges():

    #Option to upload the csv file:
    uploaded_file = st.file_uploader("Upload the aircraft range data", type = ['csv', '.xlsx'], label_visibility="collapsed")

    if uploaded_file is not None and uploaded_file.type == 'text/csv':
        aircrafts = pd.read_csv(uploaded_file)
        

        return aircrafts
    
    elif uploaded_file is not None and uploaded_file.type == 'text/xlsx':
        aircrafts = pd.read_excel(uploaded_file)
        

        return aircrafts

def upload_red_aircraft_ranges():

    #Option to upload the csv file:
    uploaded_file = st.file_uploader("Upload the red aircraft range data", type = ['csv', '.xlsx'], label_visibility="collapsed")

    if uploaded_file is not None and uploaded_file.type == 'text/csv':
        aircrafts = pd.read_csv(uploaded_file)
        

        return aircrafts
    
    elif uploaded_file is not None and uploaded_file.type == 'text/xlsx':
        aircrafts = pd.read_excel(uploaded_file)
        

        return aircrafts

