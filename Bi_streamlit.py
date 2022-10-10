import pandas as pd
import numpy as np
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery


st.set_page_config(page_title="BI-team", layout="wide")

# streamlit_app.py


# initial setting
uploaded_file=None
List_lines="Ex: google.com, 12335, DIRECT"


choice = st.sidebar.radio("Select invironment",('WEB','APP','TEST'), horizontal=True)


choice2 = st.sidebar.radio("Insert input",('Upload','Type/Paste'), horizontal=True)

if choice2=='Upload':
    uploaded_file = st.sidebar.file_uploader("Choose a .csv file")

    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        upload_input=pd.read_csv(uploaded_file,header=None)
        n=upload_input.shape[0]
        advertisingsystem=upload_input[0].str.replace(' ', '')        	
        pubaccid=upload_input[1].astype('string').str.replace(' ', '')
        relationship=upload_input[2].str.replace(' ', '')
        st.sidebar.write('Uploaded data',upload_input)

elif choice2=='Type/Paste':
    List_lines= st.sidebar.text_area('Put lines here', '''Ex: google.com, 12335, DIRECT
    ''')



   






col4, col5,col6 = st.columns(3)

with col4:
   st.image("images.png", width=80)

with col5:
   st.title("📊 IAB dataset")
with col6:
   st.write('')


# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

@st.cache
def load_data1(): 
    query1="SELECT * FROM `showheroes-bi.bi.bi_adstxt_join_sellerjson_with_count_domains`"
    query_job1 = client.query(query1)
    return client.query(query1).to_dataframe().fillna('-')



@st.cache
def load_data2():
    query2="SELECT * FROM `showheroes-bi.bi.bi_appadstxt_join_sellersjson_with_count_domains`"
    query_job2 = client.query(query2)
    return client.query(query2).to_dataframe().fillna('-')

	
df1=load_data1().copy()
df2=load_data2().copy()


st.write((uploaded_file)
st.write(List_lines)

if (choice=="WEB") and (uploaded_file is not None):
    df1=df1[(df1['AdvertisingSystem'].isin(advertisingsystem)) & (df1['PubAccId'].isin(pubaccid))]


	
	
    # Download 
    csv =df1.to_csv(index=False).encode('utf-8')	
    st.download_button(
    		label="Download ouput as CSV",
    		data=csv,
    		file_name='data.csv',
    		mime='text/csv',
		)
    st.dataframe(df1.reset_index(drop=True))
	
elif (choice=="APP") and (uploaded_file is not None):
    df2=df2[(df2['AdvertisingSystem'].isin(advertisingsystem)) & (df2['PubAccId'].isin(pubaccid))]
    df2=df2.reset_index(drop=True)


    # Download 	
    csv = df2.to_csv(index=False).encode('utf-8')
    st.download_button(
    		label="Download ouput as CSV",
    		data=csv,
    		file_name='data.csv',
    		mime='text/csv',
		)
	
    st.dataframe(df2.reset_index(drop=True))

	
elif choice=='Test':
    # Store the initial value of widgets in session state
    if "visibility" not in st.session_state:
    	st.session_state.visibility = "visible"
    	st.session_state.disabled = False

    col1, col2 = st.columns(2)

    with col1:
    	st.checkbox("Disable selectbox widget", key="disabled")
    	st.radio("Set selectbox label visibility 👉",key="visibility",options=["visible", "hidden", "collapsed"],)

    with col2:
    	option = st.selectbox("How would you like to be contacted?",("Email", "Home phone", "Mobile phone"),label_visibility=st.session_state.visibility,disabled=st.session_state.disabled,)
	

