import pandas as pd
import numpy as np
import streamlit as st
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

col4, col5,col6 = container.columns((1, 7, 1))

with col4:
   st.image("images.png", width=80)

with col5:
   st.title("📊 Showheroes SellersJson ") 
with col6:
   st.write('')
    
st.sidebar.write('Hello')	
data = urllib.request.urlopen("https://platform.showheroes.com/app/sellers.json").read()
output = json.loads(data) 
df = pd.json_normalize(output['sellers'])

st.write('DATA')
st.dataframe(df,2100,1000)


