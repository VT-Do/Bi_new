import pandas as pd
import numpy as np
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
from io import StringIO
import streamlit_authenticator as stauth
import yaml
import time
import extra_streamlit_components as stx
import smtplib

st.set_page_config(layout="wide")
container=st.container()





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
	
        st.dataframe(output_data.reset_index(drop=True),2100,1000)

    else:
        st.write('')
        st.write('No output found')
	

	
	
	
placeholder = st.empty() 
col01, col02,col03 = placeholder.columns(3)
with col01:
    st.write('')
with col02:
    with open('config.yaml') as file:
        config = yaml.safe_load(file)

    authenticator = stauth.Authenticate(config['credentials'],config['cookie']['name'],config['cookie']['key'],config['cookie']['expiry_days'],config['preauthorized'])	
    name, authentication_status, username = authenticator.login('Login', 'main')
with col03:
    st.write('')


# initial setting
uploaded_file=None
list_lines='Ex: google.com, 12335, DIRECT'


if st.session_state["authentication_status"]:

    choice =st.sidebar.radio("Select invironment",('WEB','APP'), horizontal=True)
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
                st.sidebar.error('Please check the input format')
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
            st.sidebar.error('Please check the input format')
            list_lines=''




    col4, col5,col6 = container.columns((4, 7, 1))

    with col4:
        st.image("images.png", width=80)

    with col5:
       st.title("📊 IAB dataset")
    with col6:
       authenticator.logout('Logout', 'main')
    
	
    tab1, tab2, tab3 = container.tabs(["Main","Documentation", "Contact"])
    with tab1:
        if (uploaded_file is None) and ((list_lines=='Ex: google.com, 12335, DIRECT') or (list_lines.strip()=='')):
            placeholder = st.empty()
            placeholder.markdown(f'<h1 style="color:#de4b4b;font-size:15px;">{"Please insert input!"}</h1>', unsafe_allow_html=True)

        # Create API client.
        credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        client = bigquery.Client(credentials=credentials)



        if ('Time1' not in st.session_state) and ('Time2' not in st.session_state):
            query_time1="SELECT Date FROM `showheroes-bi.bi.bi_adstxt_join_sellersjson_with_count_domains` limit 1"
            df_time1= client.query(query_time1).to_dataframe()
            st.session_state['Time1']=df_time1['Date'][0]

            query_time2="SELECT Date FROM `showheroes-bi.bi.bi_appadstxt_join_sellersjson_with_count_domains` limit 1"
            df_time2= client.query(query_time2).to_dataframe()
            st.session_state['Time2']=df_time2['Date'][0]

	

        @st.cache(max_entries=1)
        def load_data1(time): 
            query1="SELECT * except(Date) FROM `showheroes-bi.bi.bi_adstxt_join_sellersjson_with_count_domains`"
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
    with tab2: 
        col07, col08 = st.columns(2)
        with col07:
            with st.expander("Main dataset"):
                st.write("""Write something here """)
           #     st.image("https://static.streamlit.io/examples/dice.jpg")
        with col08:
            with st.expander("Invironment"):
                st.write("""Write something here. """)
       #         st.image("https://static.streamlit.io/examples/dice.jpg")
        col09, col10 = st.columns(2)
        with col09:
            with st.expander("Upload file"):
                st.write("""Write something here. """)
          #      st.image("https://static.streamlit.io/examples/dice.jpg")
        with col10:
            with st.expander("Write/paste option"):
                st.write("""Write something here. """)
         #       st.image("https://static.streamlit.io/examples/dice.jpg")
    with tab3:
        col11, col12 = st.columns(2)
        with col11:
            option = st.selectbox("Please choose type of contact",("Report an error", "Ask questions", "Comment"))
            text_input = st.text_input(label='Your name or email')
        with col12:
            form = st.form(key='my_form')
            text=form.text_area('Enter some text', '')
            submit_button = form.form_submit_button(label='Submit')
	
        if submit_button and text !='':
            st.success('Successfully submitted. Thank you for contacting us!', icon="✅")




elif st.session_state['authentication_status'] == False:
    col04, col05,col06 = st.columns(3)
    with col04:
        st.write('')
    with col05:
        st.error('Username/password is incorrect')
    with col06:
        st.write('')
elif st.session_state['authentication_status'] == None:
    col07, col08,col09 = st.columns(3)
    with col07:
        st.write('')
    with col08:
        st.warning('Please enter your username and password')
    with col09:
        st.write('')
    	 	
