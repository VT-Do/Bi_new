import pandas as pd
import numpy as np
import streamlit as st
import requests
import json,urllib.request
from datetime import date

from google.oauth2 import service_account
from google.cloud import bigquery
from io import StringIO
import streamlit_authenticator as stauth
import yaml
import time
import extra_streamlit_components as stx
import smtplib
from difflib import SequenceMatcher

st.set_page_config(layout="wide")
container=st.container()
list=['sellers','seller_id']

def check(link):
    text=[]
    try:
        response = requests.get(link, timeout=10)
        data = response.text
    
        # Create a list of first 20 lines
        Lines=[]
        for i, line in enumerate(data.split('\n')):
            if i < 20:
                Lines.append(line)
            else:
                break
        # Check if keywords in the above list
        condition = True
        for keyword in list:
            if condition:
                # check if keyword in Lines
                for item in Lines:                 
                    if keyword in item:
                        condition= True
                        break
                    else:
                        condition=  False
            else:
                break        
        return condition
    except Exception as ex: 
        return ex

def test(row):
    try:
        if check(list,row.url):
            return 'OK'
        else:
            return 'Error'
    except Exception as ex:
        return ex
    
def check_sellers(domain):
    try:
        url = "https://us-central1-viralize-gateway.cloudfunctions.net/mergeSellers?providers=" + domain
        df = pd.read_json(url, lines=True)
        if not df.empty:
            return True
        else:
            return False
    except:
        return False
    

col4, col5,col6 = container.columns((2, 6, 1))

with col4:
   st.image("images.png", width=80)

with col5:
   st.title("Showheroes SellersJson ") 
with col6:
   st.write('')
    
st.sidebar.write('Hello')


@st.experimental_memo(max_entries=1)
def load_data():
    data = urllib.request.urlopen("https://platform.showheroes.com/app/sellers.json").read()
    output = json.loads(data) 
    data = pd.json_normalize(output['sellers'])

#    data=data.head(100)
    data['url']="http://"+data['domain'] + "/sellers.json"
    data['Sellers.json status'] = np.vectorize(check)(data['url'])
    data['Json format'] = np.vectorize(check_sellers)(data['domain'])

    return data

@st.experimental_memo(max_entries=1)
def time():
    return date.today()


date=time()
#df=load_data()
#st.dataframe(df,2100,1000)


if st.sidebar.button('Update'):
    if date!=date.today():
        with st.spinner("Please be patient, update's ongoing"):
            load_data.clear()
            time.clear()
            df=load_data().copy()
            st.balloons()
            st.sidebar.write('Successfully updated')
    else:
        st.sidebar.write('Data were updated today')
        df=load_data().copy()
else:
    st.sidebar.write('last update', date)
    df=load_data().copy()
    

#st.write(check('sellers',df['url'][0])
st.dataframe(df,2100,1500)
