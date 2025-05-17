# import streamlit_authenticator as stauth

# hashed_password = stauth.Hasher().generate(['plantoai'])
# print(hashed_password)

from streamlit_authenticator.utilities.hasher import Hasher
hashed_passwords = Hasher(['plantoai']).generate()
print(hashed_passwords)