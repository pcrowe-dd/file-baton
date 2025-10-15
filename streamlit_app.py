import streamlit as st
import psycopg2

@st.cache_data
def validate_user():
    st.session_state['cursor'].execute("SELECT * FROM users WHERE username = %s AND password = %s", (st.session_state['fs_user'], st.session_state['fs_pwd']))
    result = st.session_state['cursor'].fetchone()
    if result is not None:
        st.session_state['fs_authenticated'] = True
        st.write("File sharing credentials validated successfully!")
    else:
        st.session_state['fs_authenticated'] = False
        st.write("Could not authenticate user. File sharing permissions inaccessible. Please try again.")   
        # Close cursor and connection
        #st.session_state['cursor'].close()
        #st.session_state['conn'].close()
        #st.session_state['connected'] = ''

@st.cache_resource
def init_connection():
    # Connect to your PostgreSQL database
    return psycopg2.connect(
        host=st.session_state['host'],        # or your server IP/hostname
        database="postgres", # your database name
        user=st.session_state['user'],    # your username
        password=st.session_state['pwd'], # your password
        port="5432"              # default PostgreSQL port
    )

def connect_to_db():
    try:
        st.session_state['conn'] = init_connection()
        st.session_state['cursor'] = st.session_state['conn'].cursor()
        st.session_state['connected'] = True
    except psycopg2.OperationalError as e:
        print("✗ Connection failed!")
        print(f"Error: {e}")
        st.session_state['connected'] = False
        st.session_state['error'] = str(e)  
    except Exception as e:
        print("✗ An error occurred!")
        print(f"Error: {e}")
        st.session_state['connected'] = False
        st.session_state['error'] = str(e)

#forms = {'connection': connect_credentials, 'authentication': authentication_credentials}

if 'connected' not in st.session_state:
    connect_credentials = st.form('connect_credentials')
    connect_credentials.text_input("Database Host", key="host")
    connect_credentials.text_input("Database Username", key="user")
    connect_credentials.text_input("Database Password", key="pwd", type="password")
    connect_credentials.form_submit_button("Submit", on_click=lambda: connect_to_db(), key='submit');

    st.session_state['connected'] = False
    st.session_state['error'] = ''
    st.session_state['fs_authenticated'] = False

if (st.session_state.get("submit") is not None) & (st.session_state['connected'] == True):
    st.write("Connection successful!")
    authentication_credentials = st.form('authentication_credentials')
    authentication_credentials.text_input("File Sharing Username", key="fs_user")
    authentication_credentials.text_input("File Sharing Password", key="fs_pwd", type="password")
    authentication_credentials.form_submit_button("Validate File Sharing Credentials", on_click=lambda: validate_user(), key='auth_submit');

elif (st.session_state.get("submit") is not None) & (st.session_state['connected'] == False):
    st.write("Connection failed. Please check your credentials and try again. Error: ", st.session_state['error'])
    connect_credentials = st.form('connect_credentials')
    connect_credentials.text_input("Database Host", key="host")
    connect_credentials.text_input("Database Username", key="user")
    connect_credentials.text_input("Database Password", key="pwd", type="password")
    connect_credentials.form_submit_button("Submit", on_click=lambda: connect_to_db(), key='submit');




