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
	
        st.dataframe(output_data.reset_index(drop=True))
    else:
        st.write('')
        st.write('No output found')
	

	
	
	
st.set_page_config(layout="wide")

st.markdown(
   f"""
   <style>
   p {
   background-image: url('images.png');
   }
   </style>
   """,
   unsafe_allow_html=True)


# streamlit_app.py


# initial setting
uploaded_file=None
list_lines='Ex: google.com, 12335, DIRECT'


choice = st.sidebar.radio("Select invironment",('WEB','APP'), horizontal=True)


choice2 = st.sidebar.radio("Insert input",('Upload','Type/Paste'), horizontal=True)

if choice2=='Upload':
    uploaded_file = st.sidebar.file_uploader("Choose a .csv file")

    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
	
        try:
            upload_input=pd.read_csv(uploaded_file,header=None)
            n=upload_input.shape[0]
	
	    # Clean
            upload_input[0]=upload_input[0].str.replace(' ', '').str.lower()   
            upload_input[1]=upload_input[1].astype('string').str.replace(' ', '').str.lower()
            upload_input[2]=upload_input[2].str.replace(' ', '').str.upper()
	    
            return_input_error(upload_input)
            st.sidebar.dataframe(upload_input)
		
        except Exception as ex:
            st.write(uploaded_file)
            abc=pd.read_table(StringIO(uploaded_file),sep=",", header=None)
            uploaded_file=None
            st.sidebar.write(ex)
        
		
        
	
	

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
    # first filter before looping
    df1=df1[(df1['AdvertisingSystem'].isin(upload_input[0])) & (df1['PubAccId'].isin(upload_input[1]))]
    df1=df1.reset_index(drop=True)

    # Initial setting
    data1=pd.DataFrame(columns=df1.columns.tolist())
	
    for row in range(upload_input.shape[0]):
        data1=pd.concat([data1, check_row(df1,upload_input,row)]) 
    



    
	
	
    # Download 	
    download(data1)
	
elif (choice=="WEB") and (list_lines!='Ex: google.com, 12335, DIRECT'):
   
    input=pd.read_table(StringIO(list_lines),sep=",", header=None)
	
    # Clean
    input[0]=input[0].str.replace(' ','').str.lower()
    input[1]=input[1].astype('string').str.replace(' ','').str.lower()
    input[2]=input[2].str.replace(' ','').str.upper()

    st.sidebar.write('uploaded data',input)

    # first filter before looping
    df1=df1[(df1['AdvertisingSystem'].isin(input[0])) & (df1['PubAccId'].isin(input[1]))]
    df1=df1.reset_index(drop=True)
    
    data1=pd.DataFrame(columns=df1.columns.tolist())
	
    for row in range(input.shape[0]):
        data1=pd.concat([data1, check_row(df1,input,row)]) 
    
    # Download 
    download(data1)
	
	
elif (choice=="APP") and (uploaded_file is not None):
	
    
    # first filter before looping
    df2=df2[(df2['AdvertisingSystem'].isin(upload_input[0])) & (df2['PubAccId'].isin(upload_input[1]))]
    df2=df2.reset_index(drop=True)


    # Initial setting
    data2=pd.DataFrame(columns=df2.columns.tolist())
	
    for row in range(upload_input.shape[0]):
        data2=pd.concat([data2, check_row(df2,upload_input,row)]) 
	
    # Download 	
    download(data2)

	
elif (choice=="APP") and (list_lines!='Ex: google.com, 12335, DIRECT'):
    
    input=pd.read_table(StringIO(list_lines),sep=",", header=None)
	
    # Clean
    input[0]=input[0].str.replace(' ','').str.lower()
    input[1]=input[1].astype('string').str.replace(' ','').str.lower()
    input[2]=input[2].str.replace(' ','').str.upper()

    st.sidebar.write('Uploaded data',input)


    df2=df2[(df2['AdvertisingSystem'].isin(input[0])) & (df2['PubAccId'].isin(input[1]))]
    df2=df2.reset_index(drop=True)
    #clean df2
    df2['AdvertisingSystem']=df2['AdvertisingSystem'].replace(' ','').str.lower()
    df2['PubAccId']=df2['PubAccId'].replace(' ','').str.lower()
    df2['Relationship']=df2['Relationship'].astype('string').replace(' ','').str.upper()

    data2=pd.DataFrame(columns=df2.columns.tolist())
	
    for row in range(input.shape[0]):
        dat2a=pd.concat([data2, check_row(df2,input,row)]) 
	
    # Download
    dowload(data2)	
	 	
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
	

