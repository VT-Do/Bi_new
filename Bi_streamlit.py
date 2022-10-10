#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
# import dask.dataframe as dd
# from dask import delayed, compute
import warnings
import requests
import gzip
import shutil
#from google.cloud import bigquery
import os
from google.cloud.bigquery.client import Client
import smtplib
#from pandas.core.common import SettingWithCopyWarning
#warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
#import json,urllib.request
#import concurrent.futures
import time


st.write("""# My first app 
Hello *world!*""")

# Load table from BQ
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "showheroes-bi-4be202b7b571-cloud.json"

# Construct a BigQuery client object.
client = bigquery.Client()
query = """
        SELECT *
        FROM `showheroes-bi.bi.bi_list_of_domains`
    """
query_job = client.query(query)  # Make an API request.
    
# import querry_job as a dataframe
df=client.query(query).to_dataframe()

st.table(df)

