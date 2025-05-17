from signupuser import sign_up, fetch_users, email_exists
import streamlit as st
import streamlit_authenticator as stauth
import sqlite3


# from dependancies import sign_up, fetch_users


def custom_login():
    with st.form("Login"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign In")
        
        if submitted:
            if email_exists(email):
                st.session_state.logged_in = True
                st.session_state.email = email
                st.session_state.login_successful = True
                st.success("🎉 Login successful! You can now access Nexus.AI")
                # st.sidebar(f"Welcome, {email}!")
                # st.switch_page("pages/pages/NexusAI.py")
            else:
                st.error("Email not registered! Please SignUp")
                return False




       

def main():
    # st.title("Welcome to Nexus.ai")
    # Show login or signup form based on session state
    if st.session_state.get('show_signup', False):
        sign_up()
        if st.button("Back to Login/Signup"):
            st.session_state.show_signup = False
            st.session_state.show_login = False
    elif st.session_state.get('show_login', False):
        custom_login()
        if st.button("Back to Login/Signup"):
            st.session_state.show_signup = False
            st.session_state.show_login = False
    else:
        st.title("Welcome to Nexus.ai")
        st.write("If you are new user, please sign up for an account")

        # col1, col2, col3 = st.columns([2, 2, 6]) 
        # with col1:
        if st.button("🎉 Sign Up", help="Click to create a new account"):
            st.session_state.show_signup = True
            st.session_state.show_login = False
        # with col2:
        st.write("If you already have an account, you can log in here")
        if st.button("🔐 Login", help="Click to log in to your account"):
            st.session_state.show_login = True
            st.session_state.show_signup = False
        
       

if __name__ == "__main__":
    main()
    






















# st.set_page_config(page_title='Streamlit', page_icon='🐍', initial_sidebar_state='collapsed')


# try:
#     users = fetch_users()
#     emails = []
#     usernames = []
#     passwords = []

#     for user in users:
#         emails.append(user['key'])
#         usernames.append(user['username'])
#         passwords.append(user['password'])

#     credentials = {'usernames': {}}
#     for index in range(len(emails)):
#         credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

#     Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)

#     email, authentication_status, username = Authenticator.login(':green[Login]', 'main')

#     info, info1 = st.columns(2)

#     if not authentication_status:
#         sign_up()

#     if username:
#         if username in usernames:
#             if authentication_status:
#                 # let User see app
#                 st.sidebar.subheader(f'Welcome {username}')
#                 Authenticator.logout('Log Out', 'sidebar')

#                 st.subheader('This is the home page')
#                 st.markdown(
#                     """
#                     ---
#                     Created with ❤️ by SnakeByte
                    
#                     """
#                 )

#             elif not authentication_status:
#                 with info:
#                     st.error('Incorrect Password or username')
#             else:
#                 with info:
#                     st.warning('Please feed in your credentials')
#         else:
#             with info:
#                 st.warning('Username does not exist, Please Sign up')


# except:
#     st.success('Refresh Page')







# def main():
#     # Sidebar button
#     if st.sidebar.button("🎉 Sign Up", help="Click to create a new account"):
#         # This will rerun the app and show the sign-up form
#         st.session_state.show_signup = True
    
#     # Main page logic
#     if st.session_state.get('show_signup', False):
#         sign_up()  # Your existing sign_up function
#     else:
#         # Your default page content
#         st.title("Welcome to Nexus.ai")
#         st.write("If you are a new user, please sign up using the button in the sidebar")

# if __name__ == "__main__":
#     main()