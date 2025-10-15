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


col1, col2 = st.columns([1,6])
connect_credentials = st.form('connect_credentials')
connect_credentials.text_input("Database Host", key="host")
connect_credentials.text_input("Database Username", key="user")
connect_credentials.text_input("Database Password", key="pwd", type="password")
submit = connect_credentials.form_submit_button("Submit", on_click=lambda: connect_to_db());
#connect_credentials.hide()
authentication_credentials = st.form('authentication_credentials')
authentication_credentials.text_input("File Sharing Username", key="fs_user")
authentication_credentials.text_input("File Sharing Password", key="fs_pwd", type="password")
auth_submit = authentication_credentials.form_submit_button("Validate File Sharing Credentials", on_click=lambda: validate_user());
#authentication_credentials.hide()
forms = {'connection': connect_credentials, 'authentication': authentication_credentials}

if 'connected' not in st.session_state:
    st.session_state['connected'] = False
    st.session_state['error'] = ''
    st.session_state['fs_authenticated'] = False

if submit & (st.session_state['connected'] == True):
    st.write("Connection successful!")
elif submit & (st.session_state['connected'] == False):
    st.write("Connection failed. Please check your credentials and try again. Error: ", st.session_state['error'])

#with col1:
#    st.button("Connection", on_click=lambda: toggle_connection_form(forms))
#with col2:
#    st.button("User Authentication", on_click=lambda: toggle_authentication_form(forms))


#if st.session_state['connected'] == False:
#    st.write("Connection failed. Please check your credentials and try again. Error: ", st.session_state['error'])
#    host = st.text_input("Host")
#    username = st.text_input("Username")
#    password = st.text_input("Password")

#    st.button("Connect", on_click=lambda: )

#def toggle_connection_form(forms):
#    if forms['connection'].form_state == 'visible':
#        forms['connection'].hide()
#    else:
#        forms['connection'].show()
#        forms['authentication'].hide()
#def toggle_authentication_form(forms):
#    if forms['authentication'].form_state == 'visible':
#        forms['authentication'].hide()
#    else:
#        forms['authentication'].show()
#        forms['connection'].hide()


