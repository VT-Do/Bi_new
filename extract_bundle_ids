import pandas as pd
import numpy as np
import streamlit as st
import requests
import re
from bs4 import BeautifulSoup
import json
import pandas as pd

st.set_page_config(layout="wide")


col4, col5,col6 = container.columns((2, 6, 1))

with col4:
   st.image("images.png", width=80)

with col5:
   st.title("Extract Bundle IDs") 
with col6:
   st.write('')
    
st.sidebar.write('Hello')




list_bundleid = ['air.com.jogatina.ginrummy.android','air.com.jogatina.mahjong']
app_data = []

for bundle_id in list_bundleid:
    try:
        url = "https://play.google.com/store/apps/details?id=" + bundle_id
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        title_element = soup.find("h1",class_=re.compile("Fd93Bb"))
        app_title = title_element.text.strip()
        app_data.append({'Bundle ID': bundle_id, 'App Title': app_title})
    except:
        try:
            url = "https://apptopia.com/google-play/app/" + bundle_id + "/about"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            json_element = soup.find("script", type="application/ld+json")
            json_data = json.loads(json_element.string)
            app_title = json_data['name']
            app_data.append({'Bundle ID': bundle_id, 'App Title': app_title})
        except:
            app_data.append({'Bundle ID': bundle_id, 'App Title': '-'})
   
df = pd.DataFrame(app_data)
    
st.dataframe(df,2100,1500)
