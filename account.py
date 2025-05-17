import streamlit as st
import streamlit_authenticator as stauth
import yaml

def read_config_file(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def write_config_file(path, config):
    with open(path, "w") as f:
        yaml.dump(config, f)

def auth_init():
    if 'authenticator' not in st.session_state:
        config = read_config_file("credentials.yaml")
        # print(config)
        # Check if passwords are already hashed
        if not config['credentials'].get('hashed', False):
            # Hash all passwords
            for user in config['credentials']['usernames']:
                pwd = config['credentials']['usernames'][user]['password']
                hashed_pwd = stauth.Hasher().hash(pwd)
                config['credentials']['usernames'][user]['password'] = hashed_pwd
            config['credentials']['hashed'] = True
            write_config_file("credentials.yaml", config)
        # Initialize the authenticator
        st.session_state['authenticator'] = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            auto_hash=False,
        )
auth_init()
authenticator = st.session_state['authenticator']
authenticator.login('main')

st.write("Auth status:", st.session_state.get("authentication_status"))
st.write("Username:", st.session_state.get("username"))

if st.session_state["authentication_status"]:
    st.success(f"Welcome *{st.session_state['name']}*")
    # Your main app code here
elif st.session_state["authentication_status"] is False:
    st.error("Username/password is incorrect")
elif st.session_state["authentication_status"] is None:
    st.warning("Please enter your username and password")

# authenticator.login('main')


# import streamlit as st

# authenticator = st.session_state['authenticator']

# Call login and get the results
login_result = authenticator.login('main')
st.write("Login result:", login_result)

if st.session_state['authentication_status'] is not None:
    name, authentication_status, username = login_result
    
    if authentication_status:
        st.success(f"Welcome *{name}*")
        # Your app logic here for logged-in users
    elif authentication_status is False:
        st.error("Username/password is incorrect")
    elif authentication_status is None:
        st.warning("Please enter your username and password")
else:
    # Before user submits login form
    st.info("Please enter your login credentials")





# if st.session_state['authentication_status'] is False:
#     st.error("Username/password is incorrect")

# if st.session_state['authentication_status'] is None:
#     st.warning("Please enter your username and password")

# if st.session_state['authentication_status']:
#     # plot function
#     # @st.cache_data
#     st.write(f'Welcome *{st.session_state["name"]}*')
    # authenticator.logout()
    # def plot(x,y,z):
    # #   my code continues
# name, auth_status, username = authenticator.login('main')
# if auth_status:
#     st.success(f"Welcome, {name}!")

