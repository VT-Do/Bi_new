import pandas as pd
import numpy as np
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
from io import StringIO

# col=0 (advertisingsystem), 1 (PubAccId) , 2 (Relationship),  
def check(df,col,keyword):
    list=df[col][~df[col].str.contains(keyword)].tolist()
    if len(list)>0:
        return list
    else:
        return False

# value[0]  (advertisingsystem), value[1] (PubAccId) , value[2] (Relationship),
def check_row(df,row):
    #clean
    if row.count(',')>0:
        value=row.split(',')
        value[0]=value[0].replace(' ','').lower()
        value[1]=str(value[1]).replace(' ','').lower()
        value[2]=value[2].replace(' ','').upper()
    
        return df[(df['AdvertisingSystem']==value[0])&(df['PubAccId']==value[1])&(df['Relationship']==value[2])]
    else:
        return None
	
	
	

st.set_page_config(page_title="BI-team", layout="wide")

# streamlit_app.py


# initial setting
uploaded_file=None
list_lines='Ex: google.com, 12335, DIRECT'


choice = st.sidebar.radio("Select invironment",('WEB','APP','TEST'), horizontal=True)


choice2 = st.sidebar.radio("Insert input",('Upload','Type/Paste'), horizontal=True)

if choice2=='Upload':
    uploaded_file = st.sidebar.file_uploader("Choose a .csv file")

    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        upload_input=pd.read_csv(uploaded_file,header=None)
        n=upload_input.shape[0]
	
	# Clean
        upload_input[0]=upload_input[0].str.replace(' ', '').str.lower()   
        upload_input[1]=upload_input[1].astype('string').str.replace(' ', '').str.lower()
        upload_input[2]=upload_input[2].str.replace(' ', '').str.upper()
	
        
        if check(upload_input,0,'\.'):
    	    st.sidebar.write('Check AdvertisingSystem:')
    	    st.sidebar.write(check(upload_input,0,'\.'))
        if check(upload_input,2,'DIRECT|RESELLER'):
    	    st.sidebar.write('Check Relationship:')
    	    st.sidebar.write(check(upload_input,2,'DIRECT|RESELLER'))
		
        st.sidebar.dataframe(upload_input)
	
	

elif choice2=='Type/Paste':
    list_lines= st.sidebar.text_area('Put lines here', 'Ex: google.com, 12335, DIRECT')

	

   






col4, col5,col6 = st.columns(3)

with col4:
   st.image("images.png", width=80)

with col5:
   st.title("📊 IAB dataset")
with col6:
   st.write('')

if (uploaded_file is None) and (list_lines=='Ex: google.com, 12335, DIRECT'):
    st.markdown(f'<h1 style="color:#de4b4b;font-size:15px;">{"Please insert input!"}</h1>', unsafe_allow_html=True)

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


if (choice=="WEB") and (uploaded_file is not None):
    df1=df1[(df1['AdvertisingSystem'].isin(upload_input[0])) & (df1['PubAccId'].isin(upload_input[1]))]


	
	
    # Download 	
    if df1.shape[0]>0:
        csv = df1.to_csv(index=False).encode('utf-8')
        st.download_button(
    		label="Download ouput as CSV",
    		data=csv,
    		file_name='data.csv',
    		mime='text/csv',
		)
	
        st.dataframe(df1.reset_index(drop=True))
    else:
        st.write('No output found')
elif (choice=="WEB") and (list_lines!='Ex: google.com, 12335, DIRECT'):
    list_of_rows=list_lines.split("\n")

    data=pd.DataFrame(columns=df1.columns.tolist())
	
    for row in list_of_rows:
        data=pd.concat([data, check_row(df1,row)]) 
    if data.shape[0]>0:  
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
    		label="Download ouput as CSV",
    		data=csv,
    		file_name='data.csv',
    		mime='text/csv',
		)
        st.dataframe(data.reset_index(drop=True))   
    else:
        st.write('No output found')
	
	
	
	
	
	
elif (choice=="APP") and (uploaded_file is not None):
    df2=df2[(df2['AdvertisingSystem'].isin(upload_input[0])) & (df2['PubAccId'].isin(upload_input[1]))]
    df2=df2.reset_index(drop=True)


    # Download 	
    if df2.shape[0]>0:
        csv = df2.to_csv(index=False).encode('utf-8')
        st.download_button(
    		label="Download ouput as CSV",
    		data=csv,
    		file_name='data.csv',
    		mime='text/csv',
		)
	
        st.dataframe(df2.reset_index(drop=True))
    else:
        st.write('No output found')

	
elif (choice=="APP") and (list_lines!='Ex: google.com, 12335, DIRECT'):
    list_of_rows=list_lines.split("\n")

    test=pd.read_table(StringIO(list_lines),sep=",", header=None)
    st.sidebar.write('uploaded data',test)

    data=pd.DataFrame(columns=df2.columns.tolist())
	
    for row in list_of_rows:
        data=pd.concat([data, check_row(df2,row)]) 
    if data.shape[0]>0:    
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
    		label="Download ouput as CSV",
    		data=csv,
    		file_name='data.csv',
    		mime='text/csv',
		)
	
        st.dataframe(data.reset_index(drop=True))
    else:
        st.write('No output found')	
	
	

 	
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
	

