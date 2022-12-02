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
list=['sellers']

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
        

col4, col5,col6 = container.columns((2, 6, 1))

with col4:
   st.image("images.png", width=80)

with col5:
   st.title("Showheroes -- SellersJson ") 
with col6:
   st.write('')
    
st.sidebar.write('Hello')


@st.experimental_memo(max_entries=1)
def load_data():
    data = urllib.request.urlopen("https://platform.showheroes.com/app/sellers.json").read()
    output = json.loads(data) 
    data = pd.json_normalize(output['sellers'])

    data=data.head(10)
    data['url']="http://"+data['domain'] + "/sellers.json"
    data['Sellers.json status'] = np.vectorize(check)(data['url'])
    return data

@st.experimental_memo(max_entries=1)
def time():
    return date.today()


date=time()
#df=load_data()
#st.dataframe(df,2100,1000)

if st.sidebar.button('Update'):
    if date!=date.today():
        st.sidebar.write('It takes time, please be patient') 
        load_data().clear()
        time.clear()
    else:
        st.sidebar.write('Updated')
else:
    st.sidebar.write('last update', date)
df=load_data().copy()
#st.write(check('sellers',df['url'][0])
st.dataframe(df,2100,1000)
