import sqlite3
import re
from typing import Tuple, Union
from datetime import datetime

import streamlit as st
import streamlit_authenticator as stauth

#import datetime
import re

def get_db_connection():
    """Create and return a database connection"""
    return sqlite3.connect('users.db')

def init_db():
    """Initialize the database tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            date_joined TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()


def insert_user(email, username, password):
    """Insert a new user into the database"""
    init_db()  # Add this line
    date_joined = str(datetime.now())
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (email, username, password, date_joined)
            VALUES (?, ?, ?, ?)
        ''', (email, username, password, date_joined))
        
        conn.commit()
        return {
            'email': email,
            'username': username,
            'password': password,
            'date_joined': date_joined
        }
        
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        return None
        
    finally:
        if conn:
            conn.close()



def fetch_users():
    """
    Fetches all users from the SQLite3 database.
    
    Returns:
        dict: A dictionary of users in the format {email: user_data}.
              Returns None if there's an error.
    """
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        
        # Convert rows to a dictionary {email: {user_data}}
        users = {}
        for row in rows:
            email, username, password, date_joined = row
            users[email] = {
                'username': username,
                'password': password,
                'date_joined': date_joined
            }
        
        return users
    
    except sqlite3.Error as e:
        print(f"SQLite Error: {e}")
        return None
    
    finally:
        if conn:
            conn.close()



def fetch_users():
    """
    Fetches all users from the SQLite3 database.
    
    Returns:
        dict: A dictionary of users in the format {email: user_data}.
              Returns None if there's an error.
    """
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        
        # Convert rows to a dictionary {email: {user_data}}
        users = {}
        for row in rows:
            email, username, password, date_joined = row
            users[email] = {
                'username': username,
                'password': password,
                'date_joined': date_joined
            }
        
        return users
    
    except sqlite3.Error as e:
        print(f"SQLite Error: {e}")
        return None
    
    finally:
        if conn:
            conn.close()



def get_user_emails():
    """
    Fetches all user emails from the SQLite3 database.
    
    Returns:
        list: A list of user emails (strings).
              Returns empty list if no users or error occurs.
    """
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT email FROM users')
        emails = [row[0] for row in cursor.fetchall()]
        
        return emails
    
    except sqlite3.Error as e:
        print(f"SQLite Error: {e}")
        return []
    
    finally:
        if conn:
            conn.close()



def get_usernames():
    """
    Fetches all usernames from the SQLite3 database.
    
    Returns:
        list: A list of usernames (strings).
              Returns empty list if no users or error occurs.
    """
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT username FROM users')
        usernames = [row[0] for row in cursor.fetchall()]
        
        return usernames
    
    except sqlite3.Error as e:
        print(f"SQLite Error: {e}")
        return []
    
    finally:
        if conn:
            conn.close()



def validate_email(email: str) -> Tuple[bool, str]:
    """
    Enhanced email validation with SQLite compatibility checks
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple: (is_valid: bool, error_message: str)
    """
    if not email:
        return False, "Email cannot be empty"
    
    # More comprehensive email regex pattern
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    if len(email) > 254:  # Max email length per RFC
        return False, "Email too long (max 254 chars)"
    
    return True, "Email is valid"

def validate_username(username: str) -> Tuple[bool, str]:
    """
    Enhanced username validation with SQLite compatibility checks
    
    Args:
        username: Username to validate
        
    Returns:
        Tuple: (is_valid: bool, error_message: str)
    """
    if not username:
        return False, "Username cannot be empty"
    
    # Allow letters, numbers, underscores, hyphens
    pattern = r'^[a-zA-Z0-9_-]+$'
    
    if not re.match(pattern, username):
        return False, "Only alphanumeric, underscore and hyphen characters allowed"
    
    if len(username) < 3:
        return False, "Username too short (min 3 chars)"
    
    if len(username) > 30:
        return False, "Username too long (max 30 chars)"
    
    return True, "Username is valid"



def email_exists(email: str) -> bool:
    """Check if email exists in database"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM users WHERE email = ?', (email,))
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"Error checking if email exists: {e}")
        return False  # or re-raise if you want to fail loudly
    finally:
        if conn:
            conn.close()



def sign_up():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':green[Sign Up]')
        email = st.text_input(':blue[Email]', placeholder='Enter Your Email')
        username = st.text_input(':blue[Username]', placeholder='Enter Your Username')
        password1 = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
        password2 = st.text_input(':blue[Confirm Password]', placeholder='Confirm Your Password', type='password')

        btn1, btn2, btn3, btn4, btn5 = st.columns(5)
        with btn3:
            submitted = st.form_submit_button('Sign Up')

        if submitted:
            # Validate step-by-step with early returns
            email_valid, email_msg = validate_email(email)
            if not email_valid:
                st.warning(f"Email Error: {email_msg}")
                return
                
            if email in get_user_emails():
                st.warning('Email already exists!')
                return
                
            username_valid, username_msg = validate_username(username)
            if not username_valid:
                st.warning(f"Username Error: {username_msg}")
                return
                
            if username in get_usernames():
                st.warning('Username already exists!')
                return
                
            if len(password1) < 6:
                st.warning('Password must be at least 6 characters')
                return
                
            if password1 != password2:
                st.warning('Passwords do not match')
                return
                
            # All validations passed - create account
            try:
                hashed_password = stauth.Hasher().hash(password2) #stauth.Hasher([password2]).generate()[0]
                insert_user(email, username, hashed_password)
                st.success('Account created successfully!')
                st.snow() 
                # st.write("🎉" * 10) 
            except Exception as e:
                st.error(f"Account creation failed: {str(e)}")



# new_user = insert_user(
#     email="admin@example.com",
#     username="admin_user",
#     password="planto"  # Use a real hashed password
# )

# if new_user:
#     print("User created successfully:", new_user)
# else:
#     print("Failed to create user.")
# Add to your existing code
def main():

    
    if st.session_state.get('show_signup', False):
        sign_up()
    else:
        st.title("Welcome to Nexus.ai")
        st.write("If you are new user, please sign up and register your account below.")
        if st.button("🎉 Sign Up", help="Click to create a new account"):
            st.session_state.show_signup = True





    # # Sidebar button
    # if st.button("🎉 Sign Up", help="Click to create a new account"):
    #     # This will rerun the app and show the sign-up form
    #     st.session_state.show_signup = True
    
    # # Main page logic
    # if st.session_state.get('show_signup', False):
    #     sign_up()  # Your existing sign_up function
    # else:
    #     # Your default page content
    #     st.title("Welcome to Nexus.ai")
    #     st.write("If you are a new user, please sign up using the button in the sidebar")

if __name__ == "__main__":
    main()