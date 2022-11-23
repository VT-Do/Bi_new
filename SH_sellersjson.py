import pandas as pd
import numpy as np
import streamlit as st
import requests
import json,urllib.request


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

def check(keyword,link):
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
   st.title("Showheroes SellersJson ") 
with col6:
   st.write('')
    
st.sidebar.write('Hello')	
data = urllib.request.urlopen("https://platform.showheroes.com/app/sellers.json").read()
output = json.loads(data) 
df = pd.json_normalize(output['sellers'])

df=df.head(100)
df['url']="http://"+df['domain'] + "/sellers.json"
df['Sellers.json status'] = np.vectorize(check)(list, df['url'])

st.write('DATA')
st.dataframe(df,2100,1000)


