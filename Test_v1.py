import pandas as pd
import numpy as np
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery



with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)	
	
	

st.set_page_config(page_title="BI-team", layout="wide")





choice = st.sidebar.radio("Select invironment",('WEB','APP','TESTTT'), horizontal=True)


choice2 = st.sidebar.radio("Insert input",('Upload','Type/Paste'), horizontal=True)

if choice2=='Upload':
    uploaded_file = st.sidebar.file_uploader("Choose a .csv file")

    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        upload_input=pd.read_csv(uploaded_file,header=None)
        n=upload_input.shape[0]
	
	# Clean
        upload_input[0]=upload_input[0].str.replace(' ', '')
        upload_input[1]=upload_input[1].astype('string').str.replace(' ', '')
        upload_input[2]=upload_input[2].str.replace(' ', '')
	
        upload_input[0]=upload_input[0].str.lower()   	
        upload_input[1]=upload_input[1].astype('string').str.lower()
        upload_input[2]=upload_input[2].str.lower()
	
	
	
        if check(upload_input,2,'DIRECT|RESELLER'):
            st.sidebar.write('Check Relationship:')
            st.sidebar.write(check(upload_input,2,'DIRECT|RESELLER'))
        if check(upload_input,0,'.'):
            st.sidebar.write('Check AdvertisingSystem:')
            st.sidebar.write(check(upload_input,0,'.'))
            st.write('Nothing')
            st.sidebar.table('Uploaded data',upload_input)
            st.sidebar.table('Uploaded data',upload_input)
	
	

   

