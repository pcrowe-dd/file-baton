import streamlit as st
import psycopg2

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

if 'connected' not in st.session_state or st.session_state['connected'] == '':
    st.session_state['connected'] = ''
    host = st.text_input("Host")
    username = st.text_input("Username")
    password = st.text_input("Password")

    st.button("Connect", on_click=lambda: connect_to_db(host, username, password))


if st.session_state['connected'] == False:
    st.write("Connection failed. Please check your credentials and try again. Error: ", st.session_state['error'])
    host = st.text_input("Host")
    username = st.text_input("Username")
    password = st.text_input("Password")

    st.button("Connect", on_click=lambda: connect_to_db(host, username, password))

if st.session_state['connected'] == True:
    st.write("Connection successful!")
    fs_user = st.text_input("File Sharing Username")
    fs_password = st.text_input("File Sharing Password")
    st.button("Validate File Sharing Credentials", on_click=lambda: validate_user(fs_user, fs_password))

def validate_user(user, pwd):
    result = st.session_state['cursor'].execute("SELECT * FROM users WHERE username = %s AND password = %s", (user, pwd))
    if result is not None:
        st.session_state['fs_authenticated'] = True
        st.write("File sharing credentials validated successfully!")
                
        # Close cursor and connection
        st.session_state['cursor'].close()
        st.session_state['conn'].close()
        st.session_state['connected'] = ''

def connect_to_db(host, user, pwd):

    try:
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(
            host=host,        # or your server IP/hostname
            database="postgres", # your database name
            user=user,    # your username
            password=pwd, # your password
            port="5432"              # default PostgreSQL port
        )
    
        # Create a cursor object
        st.session_state['cursor'] = conn.cursor()
        st.session_state['conn'] = conn
    
        st.session_state.connected = True
    
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
