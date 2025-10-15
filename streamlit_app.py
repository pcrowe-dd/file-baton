import streamlit as st
import psycopg2

@st.cache_data
def validate_user():
    st.session_state['cursor'].execute("SELECT user_id FROM users WHERE username = %s AND password = %s", (st.session_state['fs_user'], st.session_state['fs_pwd']))
    result = st.session_state['cursor'].fetchone()
    if result is not None:
        st.session_state.fs_authenticated = True
        st.write("File sharing credentials validated successfully!")
        st.session_state['cursor'].execute("SELECT can_upload, can_add_user FROM user_permissions WHERE user_id = %s", result)
        result = st.session_state['cursor'].fetchone()
        st.write("User Permissions - Can Upload: ", result[0], ", Can Add User: ", result[1])
        if result[0]:
            st.session_state.can_upload = True
        if result[1]:
            st.session_state.can_add_user = True
    else:
        st.session_state.fs_authenticated = False
        st.write("Could not authenticate user. File sharing permissions inaccessible. Please try again.")   

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
def close_connection():
    st.session_state['connected'] = False
    # Close cursor and connection

    if 'cursor' in st.session_state:
        st.session_state['cursor'].close()
    if 'conn' in st.session_state:
        st.session_state['conn'].close()



#forms = {'connection': connect_credentials, 'authentication': authentication_credentials}

st.button("Close Connection", on_click=lambda: close_connection())

if 'connected' not in st.session_state:
    st.session_state['connected'] = False
    st.session_state['error'] = ''
    st.session_state['fs_authenticated'] = False

    connect_credentials = st.form('connect_credentials')
    connect_credentials.text_input("Database Host", key="host")
    connect_credentials.text_input("Database Username", key="user")
    connect_credentials.text_input("Database Password", key="pwd", type="password")
    connect_credentials.form_submit_button("Submit", on_click=lambda: connect_to_db(), key='submit');
elif (st.session_state.get("submit") is not None) & (st.session_state['connected'] == False):
    st.write("Connection failed. Please check your credentials and try again. Error: ", st.session_state['error'])
    connect_credentials = st.form('connect_credentials')
    connect_credentials.text_input("Database Host", key="host")
    connect_credentials.text_input("Database Username", key="user")
    connect_credentials.text_input("Database Password", key="pwd", type="password")
    connect_credentials.form_submit_button("Submit", on_click=lambda: connect_to_db(), key='submit');

elif (st.session_state.get("submit") is not None) & (st.session_state['connected'] == True):
    st.write("Connection successful!")
    authentication_credentials = st.form('authentication_credentials')
    authentication_credentials.text_input("File Sharing Username", key="fs_user")
    authentication_credentials.text_input("File Sharing Password", key="fs_pwd", type="password")
    authentication_credentials.form_submit_button("Validate File Sharing Credentials", on_click=lambda: validate_user(), key='auth_submit');

if (st.session_state['fs_authenticated'] == True):
    st.write("You are now authenticated to access file sharing features.")
    # Add file sharing features here
    if (st.session_state.get("can_add_user") is True):
        with st.form('add_user_form'):
            st.subheader("Add New User")
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            permission_can_upload = st.checkbox("Can Upload")
            permission_can_add_user = st.checkbox("Can Add User")
            submitted = st.form_submit_button("Add User")
            if submitted:
                try:
                    st.session_state['cursor'].execute("INSERT INTO users (username, password) VALUES (%s, %s) RETURNING user_id", (new_username, new_password))
                    user_id = st.session_state['cursor'].fetchone()[0]
                    st.session_state['cursor'].execute("INSERT INTO user_permissions (user_id, can_upload, can_add_user) VALUES (%s, %s, %s)", (user_id, permission_can_upload, permission_can_add_user))
                    st.session_state['conn'].commit()
                    st.write("User ", new_username, " added successfully!")
                except Exception as e:
                    st.error(f"Error adding user: {e}")


