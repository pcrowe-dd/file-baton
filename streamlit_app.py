import streamlit as st
import psycopg2

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

username = st.text_input("User name")

try:
    # Connect to your PostgreSQL database
    conn = psycopg2.connect(
        host="localhost",        # or your server IP/hostname
        database="definian_data", # your database name
        user=username,    # your username
        password="your_password", # your password
        port="5432"              # default PostgreSQL port
    )
    
    # Create a cursor object
    cursor = conn.cursor()
    
    # Execute a simple query
    cursor.execute("SELECT version();")
    
    # Fetch and print the result
    db_version = cursor.fetchone()
    print("✓ Connection successful!")
    print(f"PostgreSQL version: {db_version[0]}")
    
    # Close cursor and connection
    cursor.close()
    conn.close()
    print("✓ Connection closed successfully")
    
except psycopg2.OperationalError as e:
    print("✗ Connection failed!")
    print(f"Error: {e}")
    
except Exception as e:
    print("✗ An error occurred!")
    print(f"Error: {e}")
