import pandas as pd
import numpy as np
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
from io import StringIO
#from streamlit import caching
import time

# col=0 (advertisingsystem), 1 (PubAccId) , 2 (Relationship),  
def check(df,col,keyword):
    list=df[col][~df[col].str.contains(keyword)].tolist()
    if len(list)>0:
        return list
    else:
        return False

# Check if AvertisingSystem contains '.' or Relationship is not DIRECT or RESELLER
def return_input_error(input):
    if check(input,0,'\.'):
        st.sidebar.write('Check AdvertisingSystem:')
        st.sidebar.write(check(input,0,'\.'))
    if check(input,2,'DIRECT|RESELLER'):
        st.sidebar.write('Check Relationship:')
        st.sidebar.write(check(input,2,'DIRECT|RESELLER'))


# df[0] (advertisingsystem), df[1] (PubAccId) , df[2] (Relationship),  
def check_row(df,input_data,row):
    df_filtered=df[(df['AdvertisingSystem']==input_data[0][row])&(df['PubAccId']==input_data[1][row])&(df['Relationship']==input_data[2][row])]
    if df_filtered.shape[0]>0:
        return df_filtered
    else:
        return None
	
#download
def download(output_data):
    if output_data.shape[0]>0:    
        csv = output_data.to_csv(index=False).encode('utf-8')
        st.download_button(
    		label="Download ouput as CSV",
    		data=csv,
    		file_name='data.csv',
    		mime='text/csv',
		)
	
        st.dataframe(output_data.reset_index(drop=True),2000,1000)

    else:
        st.write('')
        st.write('No output found')
	

	
	
	
st.set_page_config(layout="wide")


# streamlit_app.py


# initial setting
uploaded_file=None
list_lines='Ex: google.com, 12335, DIRECT'

if 'BI_team' not in st.session_state:
    Password = st.text_input('Password', 'Type here')
    st.session_state.Password=Password
    st.write('The password is', Password)

if Password=='BI_team':
    choice = st.sidebar.radio("Select invironment",('WEB','APP', 'Test', 'Test2'), horizontal=True)


    choice2 = st.sidebar.radio("Insert input",('Upload','Type/Paste'), horizontal=True)

    if choice2=='Upload':
        uploaded_file = st.sidebar.file_uploader("Choose a .csv file")

        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
	
            try:
                upload_input=pd.read_csv(uploaded_file,header=None)
                n=upload_input.shape[0]
	
	        # Clean
                upload_input[0]=upload_input[0].str.replace(' ', '').str.replace('\t','').str.lower()   
                upload_input[1]=upload_input[1].astype('string').str.replace(' ', '').str.replace('\t','').str.lower()
                upload_input[2]=upload_input[2].str.replace(' ', '').str.replace('\t','').str.upper()
	    
                return_input_error(upload_input)
                st.sidebar.dataframe(upload_input)
		
            except Exception as ex:
                st.sidebar.write('Please check the input format')
                uploaded_file=None
        

    elif choice2=='Type/Paste':
        list_lines= st.sidebar.text_area('Put lines here', 'Ex: google.com, 12335, DIRECT')
    
        try:
            input=pd.read_table(StringIO(list_lines),sep=",", header=None)
	
            # Clean
            input[0]=input[0].str.replace(' ','').str.replace('\t','').str.lower()
            input[1]=input[1].astype('string').str.replace(' ','').str.replace('\t','').str.lower()
            input[2]=input[2].str.replace(' ','').str.replace('\t','').str.upper()
            input=input.drop_duplicates()
            if list_lines !='Ex: google.com, 12335, DIRECT' and list_lines.strip()!='':
                return_input_error(input)
                st.sidebar.write('Input data',input)
        except:
            st.sidebar.write('Please check the input format')
            list_lines=''





    col4, col5,col6 = st.columns(3)

    with col4:
       st.image("images.png", width=80)

    with col5:
       st.title("📊 IAB dataset")
    with col6:
       st.write('')

    if (uploaded_file is None) and ((list_lines=='Ex: google.com, 12335, DIRECT') or (list_lines.strip()=='')):
        st.markdown(f'<h1 style="color:#de4b4b;font-size:15px;">{"Please insert input!"}</h1>', unsafe_allow_html=True)

    # Create API client.
    credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
    client = bigquery.Client(credentials=credentials)



    if ('Time1' not in st.session_state) and ('Time2' not in st.session_state):
        query_time1="SELECT Date FROM `showheroes-bi.bi.bi_adstxt_join_sellerjson_with_count_domains` limit 1"
        df_time1= client.query(query_time1).to_dataframe()
        st.session_state['Time1']=df_time1['Date'][0]

        query_time2="SELECT Date FROM `showheroes-bi.bi.bi_appadstxt_join_sellersjson_with_count_domains` limit 1"
        df_time2= client.query(query_time2).to_dataframe()
        st.session_state['Time2']=df_time2['Date'][0]

	

    @st.cache(max_entries=1)
    def load_data1(time): 
        query1="SELECT * except(Date) FROM `showheroes-bi.bi.bi_adstxt_join_sellerjson_with_count_domains`"
        query_job1 = client.query(query1)
        return client.query(query1).to_dataframe().fillna('-')




    @st.cache(max_entries=1)
    def load_data2(time):
        query2="SELECT * except(Date) FROM `showheroes-bi.bi.bi_appadstxt_join_sellersjson_with_count_domains`"
        query_job2 = client.query(query2)
        return client.query(query2).to_dataframe().fillna('-')
	
    df1=load_data1(st.session_state['Time1']).copy()
    df2=load_data2(st.session_state['Time2']).copy()


    if (choice=="WEB") and (uploaded_file is not None):
        # first filter before looping
        df1=df1[(df1['AdvertisingSystem'].isin(upload_input[0])) & (df1['PubAccId'].isin(upload_input[1]))]
        df1=df1.reset_index(drop=True)

        # Initial setting
        data1=pd.DataFrame(columns=df1.columns.tolist())
	
        for row in range(upload_input.shape[0]):
            data1=pd.concat([data1, check_row(df1,upload_input,row)]) 
    
    
        # Download 	
        download(data1)
	
    elif (choice=="WEB") and (list_lines!='Ex: google.com, 12335, DIRECT') and (list_lines.strip()!=''):
        # first filter 
        df1=df1[(df1['AdvertisingSystem'].isin(input[0])) & (df1['PubAccId'].isin(input[1]))]
        df1=df1.reset_index(drop=True)
    
        data1=pd.DataFrame(columns=df1.columns.tolist())
	
        for row in range(input.shape[0]):
            data1=pd.concat([data1, check_row(df1,input,row)]) 
    

        # Download 
        download(data1)
    
	
    elif (choice=="APP") and (uploaded_file is not None):   
        # first filter 
        df2=df2[(df2['AdvertisingSystem'].isin(upload_input[0])) & (df2['PubAccId'].isin(upload_input[1]))]
        df2=df2.reset_index(drop=True)
 

        # Initial setting
        data2=pd.DataFrame(columns=df2.columns.tolist())
	
        for row in range(upload_input.shape[0]):
            data2=pd.concat([data2, check_row(df2,upload_input,row)]) 
    

        # Download 	
        download(data2)

	
    elif (choice=="APP") and (list_lines!='Ex: google.com, 12335, DIRECT') and (list_lines.strip()!=''):
        # first filter
        df2=df2[(df2['AdvertisingSystem'].isin(input[0])) & (df2['PubAccId'].isin(input[1]))]
        df2=df2.reset_index(drop=True)
	
        data2=pd.DataFrame(columns=df2.columns.tolist())
	
        for row in range(input.shape[0]):
            data2=pd.concat([data2, check_row(df2,input,row)]) 

        # Download
        download(data2)	
	 	
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
	

    elif choice=='Test2':
        st.write('Hello')
        st.caching.clear_cache() 
	
        @st.cache(suppress_st_warning=True)
        def expensive_computation(a, b):
            st.session_state["cache_updated"] = True
            time.sleep(2)  # This makes the function take 2s to run
            return a * b

        a = 3
        b = 21
        res = expensive_computation(a, b)
        st.write(res)
        st.write((st.session_state["cache_updated"]))
else:
    st.write('Write something here')
