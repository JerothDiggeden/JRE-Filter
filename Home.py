from icecream import ic
import streamlit as st
import bcrypt
import streamlit_authenticator as auth
import os
import pickle


# For demonstration, using an in-memory dictionary
# In production, use a proper database
BASE_DIR = "user_files"


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_password(password, hashed):
    st.write('hashed: ', hashed)
    st.write('password: ', password)
    password = password.encode('utf-8')
    return bcrypt.checkpw(password, hashed)


def create_user_folder(username):
    user_folder = os.path.join(BASE_DIR, username)
    os.makedirs(user_folder, exist_ok=True)
    return user_folder


def signup(username, password):
    # Check if the file exists and load data, handle file not found or invalid data
    if os.path.exists('hashed_psswds.pkl'):
        try:
            with open('data/hashed_psswds.pkl', 'rb') as f:
                user_data = pickle.load(f)
        except (pickle.UnpicklingError, EOFError, AttributeError, ValueError) as e:
            st.error(f"Error loading user data: {e}")
            user_data = {}
    else:
        user_data = {}

    if username in user_data:
        st.warning("Username already exists.")
    else:
        hashed_pw = hash_password(password)  # Assuming this function is defined
        user_data[username] = hashed_pw
        create_user_folder(username)  # Assuming this function is defined
        st.success("Signup successful. You can now log in.")

        # Write updated data back to the pickle file
        with open('data/hashed_psswds.pkl', 'wb') as f:
            pickle.dump(user_data, f)

        st.write(user_data)


def login(username, password):
    with open('data/hashed_psswds.pkl', 'rb') as f:
        user_data = pickle.load(f)
        st.write(user_data[username])
        on_file = (user_data[username])
    if username not in user_data:
        st.warning("Username not found.")
    elif check_password(password, on_file):
        st.success(f"Welcome {username}!")
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
        st.session_state['user_folder'] = os.path.join(BASE_DIR, username)
    else:
        st.warning("Incorrect password.")

# Main application logic
st.title("User Authentication")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    st.write(f"Logged in as {st.session_state['username']}")
    if st.button("Logout"):
        st.session_state['logged_in'] = False
else:
    option = st.selectbox("Choose Option", ["Login", "Signup"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Signup":
        if st.button("Signup"):
            signup(username, password)
    elif option == "Login":
        if st.button("Login"):
            login(username, password)
