import streamlit as st
import bcrypt
import os
import pickle
from pathlib import Path
from cryptography.fernet import Fernet
from icecream import ic


st.set_page_config(page_title="Episodes", page_icon=":material/edit:", layout="wide",
                   initial_sidebar_state="collapsed")

col1, col2, col3 = st.columns([2, 1, 2])


# For demonstration, using an in-memory dictionary
# In production, use a proper database
BASE_DIR = "user_files"

global username

key_names = []
keys1 = {}
keys2 = {}

# # GENERATE KEYS FOR EMPTY FILES
#
# i = 'admin'
# key = Fernet.generate_key()
# keys1[i] = key
# key_names.append(i)
# # Save the key to a file (optional)
# with open("data/keys.pkl", "wb") as f:
#     pickle.dump(keys1, f)
#
# i = 'admin'
# key = Fernet.generate_key()
# keys2[i] = key
# key_names.append(i)
# # Save the key to a file (optional)
# with open("data/hashed_psswds.pkl", "wb") as f:
#     pickle.dump(keys2, f)


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_password(password, hashed):
    password = password.encode('utf-8')
    return bcrypt.checkpw(password, hashed)


def create_user_folder(username):
    user_folder = os.path.join(BASE_DIR, username)
    os.makedirs(user_folder, exist_ok=True)
    return user_folder


def signup(username, password):
    # Check if the file exists and load data, handle file not found or invalid data
    if os.path.exists('data/hashed_psswds.pkl'):
        try:
            with open('data/hashed_psswds.pkl', 'rb') as f:
                user_data = pickle.load(f)
                i = username
                if i not in user_data:
                    key = Fernet.generate_key()
                    keys1[i] = key
                    key_names.append(i)
                # Save the key to a file (optional)
                with open("data/hashed_psswds.pkl", "wb") as f:
                    pickle.dump(keys1, f)

        except (pickle.UnpicklingError, EOFError, AttributeError, ValueError) as e:
            st.error(f"Error loading user data: {e}")
            user_data = {}

    if os.path.exists('data/keys.pkl'):
        try:
            with open('data/keys.pkl', 'rb') as f:
                filter_keys = pickle.load(f)
                i = username
                keys2 = filter_keys
                if i not in filter_keys:
                    key = Fernet.generate_key()
                    keys2[i] = key
                    key_names.append(i)
                # Save the key to a file (optional)
                with open("data/keys.pkl", "wb") as f:
                    pickle.dump(keys2, f)

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

        with open("data/keys.pkl", "rb") as f:
            keys = pickle.load(f)
        b = username
        b = b.encode('utf-8')
        if b not in keys:
            key = Fernet.generate_key()
            keys[username] = key
            key_names.append(username)
        # Save the key to a file (optional)
        with open("data/keys.pkl", "wb") as f:
            pickle.dump(keys, f)

        # Write updated data back to the pickle file
        with open('data/hashed_psswds.pkl', 'wb') as f:
            pickle.dump(user_data, f)

        # Get the home directory of the current user
        home_directory = Path.home()

        # Define the user-specific directory path
        nested_directory = home_directory / 'user_files' / username

        # Create the directories
        nested_directory.mkdir(parents=True, exist_ok=True)

        with open(f'user_files/{username}/filter.txt', 'w') as f:
            f.write('')


def login(username, password):
    username = username.strip()
    with open('data/hashed_psswds.pkl', 'rb') as f:
        user_data = pickle.load(f)
        on_file = (user_data[username])
    if username not in user_data:
        st.warning("Username not found.")
    elif check_password(password, on_file):
        st.success(f"Welcome {username}!")
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
        st.session_state['user_folder'] = os.path.join(BASE_DIR, username)
        if username not in st.session_state:
            st.session_state.username = username
    else:
        st.warning("Incorrect password.")


with col2:

    st.title("Authentication")

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
