import pandas as pd
import numpy as np
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery


st.set_page_config(page_title="BI-team", layout="wide")

# streamlit_app.py





choice = st.sidebar.radio(
    "Select dataset",
    ('WEB','APP','TEST'))


uploaded_file = st.sidebar.file_uploader("Choose a .csv file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # Can be used wherever a "file-like" object is accepted:
    input = pd.read_csv(uploaded_file, header=None)
    
    st.write('Uploaded data',input)
	
List_lines= st.sidebar.text_area('Put lines here', '''Ex: google.com, 12335, DIRECT
    ''')

AdvertisingSystem=input[0].str.replace(' ', '')
PubAccId=input[1].str.replace(' ', '')
Relationship=input[1].str.replace(' ', '')

#i1 = st.button("button 1")
#st.write("value:", i1)
#i2 = st.checkbox("reset button")







# st. set_page_config(layout="wide")

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
	query1="SELECT * FROM `showheroes-bi.bi.bi_adstxt_join_sellerjson_with_count_domains` limit 100000"
	query_job1 = client.query(query1)
	return client.query(query1).to_dataframe().fillna('-')



@st.cache
def load_data2():
	query2="SELECT * FROM `showheroes-bi.bi.bi_appadstxt_join_sellersjson_with_count_domains` limit 100000"
	query_job2 = client.query(query2)
	return client.query(query2).to_dataframe().fillna('-')

	
df1=load_data1().copy()
df2=load_data2().copy()


	


if choice=="WEB":
		
	

	
	
	@st.cache
	def convert_df(df):
    	# IMPORTANT: Cache the conversion to prevent computation on every rerun
    		return df.to_csv().encode('utf-8')

	
	
	
	csv = convert_df(df1)

	st.download_button(
    		label="Download data as CSV",
    		data=csv,
    		file_name='data.csv',
    		mime='text/csv',
		)
	
	st.dataframe(df1)
	
elif choice=="APP":

	@st.cache
	def convert_df(df):
    	# IMPORTANT: Cache the conversion to prevent computation on every rerun
    		return df.to_csv().encode('utf-8')

	
	
	
	csv = convert_df(df2)

	st.download_button(
    		label="Download data as CSV",
    		data=csv,
    		file_name='data.csv',
    		mime='text/csv',
		)
	
	st.dataframe(df2)

	
else:
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
	

