import requests
import streamlit as st
import pickle
from cryptography.fernet import Fernet
from icecream import ic


if 'username' not in st.session_state:
    st.session_state.username = None

username = st.session_state.username

ic(username)

users_db = {}
col1, col2 = st.columns([1, 2])

url = "https://spotify23.p.rapidapi.com/podcast_episodes/"

querystring = {"id": "4rOoJ6Egrf8K2IrywzwOMk", "offset": "0", "limit": "330"}

headers = {
    "x-rapidapi-key": "1b6ce2494dmshf74f9c461b4cdbbp1d3b11jsndd6ab0d8575c",
    "x-rapidapi-host": "spotify23.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

response = response.json()

users_db = {}
episodes_lst = []
episodes_dsc = []
episodes_dict = {}
episode_names = []
descriptions = []
key_names = []
keyword_lst = []
keyword = []
dec_lst = []


latest_desc = ''
response = response['data']['podcastUnionV2']['episodesV2']['items']

try:
    with open("data/keys.pkl", "rb") as f:
        keys = pickle.load(f)
        key = keys[username]
        cipher = Fernet(key)
        ic(cipher)
        with open(f"user_files/{username}/filter.txt", "rb") as f:
            encrypted_data = f.read()
            decrypted_data = cipher.decrypt(encrypted_data)
            decrypted_data = decrypted_data.decode('utf-8')
            decrypted_data = str(decrypted_data)
            decrypted_data = decrypted_data.replace('b', '')
            decrypted_data = decrypted_data.split(',')
            keyword = decrypted_data
        ic(decrypted_data)
except FileNotFoundError:
    st.dialog('Please Login')


for episode in response:
    if 'entity' in episode:
        entity_data = episode['entity']['data']
        ep_code = entity_data.get('uri', '')
        description = entity_data.get('description', '').split()
        for word in description:
            if word in keyword:
                episodes_lst.append(ep_code)
        ic(episodes_lst)

# EPISODE NAMES LIST
for uri in response:
    if 'entity' in uri:
        count = 0
        if uri['entity']['_uri'] in episodes_lst:
            entity_data = uri['entity']['data']['description']
            episodes_dict[uri['entity']['data']['name']] = entity_data
            episode_names.append(uri['entity']['data']['name'])
            uri = uri
        count += 1

# DESCRIPTIONS LIST
for k in response:
    if 'entity' in k:
        if k['entity']['_uri'] in episodes_lst:
            descriptions.append(k['entity']['data']['description'])
            ic(descriptions)

for l in response:
    if 'entity' in l:
        try:
            if l['entity']['_uri'] == episodes_lst[0]:
                latest_desc = l['entity']['data']['description']

        except IndexError:
            continue


def update_content(value):
    container.write(value)

def new_key():
    with open("keys/keys.pkl", "rb") as f:
        keys = pickle.load(f)
    i = username
    if i not in keys:
        key = Fernet.generate_key()
        keys[i] = key
        key_names.append(i)
    # Save the key to a file (optional)
    with open("keys/keys.pkl", "wb") as f:
        pickle.dump(keys, f)


def add():
    global add_txt, decrypted_data
    new_word = st.session_state.add_txt
    keyword_lst.append(new_word)
    try:
        with open("data/keys.pkl", "rb") as f:
            keys = pickle.load(f)
            key = keys[username]
            cipher = Fernet(key)
            with open(f"user_files/{username}/filter.txt", "rb") as f:
                encrypted_data = f.read()
                decrypted_data = cipher.decrypt(encrypted_data)
                f.close()
                with open(f'user_files/{username}/filter.txt', 'wb') as file:
                    key = keys[username]
                    cipher = Fernet(key)
                    new_word = new_word.encode('utf-8')
                    comma = ","
                    comma = comma.encode('utf-8')
                    file.write(decrypted_data + comma + new_word)
                    file.close()
                    with open(f"user_files/{username}/filter.txt", "rb") as f:
                        new_data = f.read()
                        encrypted_data = cipher.encrypt(new_data)
                        with open(f'user_files/{username}/filter.txt', 'wb') as file:
                            file.write(encrypted_data)
                            file.close()

    except FileNotFoundError:
        st.dialog('Please Login')


def sub():
    global add_txt
    sub_word = st.session_state.sub_txt
    try:
        with open("data/keys.pkl", "rb") as f:
            keys = pickle.load(f)
            key = keys[username]
            cipher = Fernet(key)
            with open(f"user_files/{username}/filter.txt", "rb") as f:
                encrypted_data = f.read()
                decrypted_data = cipher.decrypt(encrypted_data)
                decrypted_data = decrypted_data.decode('utf-8')
                decrypted_data = str(decrypted_data)
                decrypted_data = decrypted_data.replace('b', '')
                decrypted_data = decrypted_data.split(',')
                decrypted_data = decrypted_data.remove(sub_word)
                f.close()
                with open(f'user_files/{username}/filter.txt', 'wb') as file:
                    key = keys[username]
                    cipher = Fernet(key)
                    if decrypted_data:
                        file.write(decrypted_data)
                    else:
                        file.close()
                    with open(f"user_files/{username}/filter.txt", "rb") as f:
                        new_data = f.read()
                        encrypted_data = cipher.encrypt(new_data)
                        with open(f'user_files/{username}/filter.txt', 'wb') as file:
                            file.write(encrypted_data)
                            file.close()
    except FileNotFoundError:
        st.dialog('Please Login')

def clear():
    keyword.clear()
    keyword.append("")
    try:
        with open(f'user_files/{username}/filter.txt', 'w') as file:
            for word in keyword:
                file.writelines(word)
    except FileNotFoundError:
        st.dialog('Please Login')

ep_links = []
dec_filters = []

with open("data/keys.pkl", "rb") as f:
    keys = pickle.load(f)
    key = keys[username]
    cipher = Fernet(key)
    with open(f"user_files/{username}/filter.txt", "rb") as f:
        encrypted_data = f.read()
        decrypted_data = cipher.decrypt(encrypted_data)
        decrypted_data = decrypted_data.decode('utf-8')
        decrypted_data = str(decrypted_data)
        decrypted_data = decrypted_data.replace('b', '')
        decrypted_data = decrypted_data.split(',')
        for filter in decrypted_data:
            dec_filters.append(filter)


# Using "with" notation
with st.sidebar:
    container = st.empty()
    pic = response[0]['entity']['data']['podcastV2']['data']['coverArt']['sources'][1]['url']
    pic2 = response[0]['entity']['data']['coverArt']['sources'][1]['url']
    pic3 = response[0]['entity']['data']['coverArt']['sources'][1]['url']
    st.title('My JRE Filter')
    st.image(pic, use_column_width=False)
    st.title('Filter: ')
    add_txt = st.text_input(key='add_txt', label='Add Filter', placeholder='Enter a New Filter Word', on_change=add)
    sub_txt = st.text_input(key='sub_txt', label='Remove Filter', placeholder='Enter a Filter Word to Remove',
                            on_change=sub)
    clear = st.button('Clear', key='clear', on_click=clear)
    filter_lst = st.write(decrypted_data)

ic(episodes_lst)
with col1:
    latest_name = response[0]['entity']['data']['name']
    latest_desc = response[0]['entity']['data']['description']
    latest_html = response[0]['entity']['data']['sharingInfo']['shareUrl']
    try:
        length = len(episodes_lst)
        latest_filtered = episodes_lst[length - 1]
        latest_filtered = f"https://open.spotify.com/episode/{latest_filtered[16:]}?si=123e7de133124692&nd=1&dlsi=ad207e177da14244"
    except IndexError:
        print("Index Error")

    st.title('')
    st.title('')
    st.title('Latest Episode: ')
    st.image(pic2, use_column_width=False)
    st.page_link(latest_html, label=latest_name)
    st.write(latest_desc)

    st.title('Filtered Episode: ')
    st.image(pic3, use_column_width=False)
    try:
        st.write(descriptions[0])
    except IndexError:
        print("Index Error")

    try:
        st.page_link(latest_filtered, label=latest_name)

    except NameError:
        print("Name Error")

    st.title('Old Episodes: ')
    for i, link in enumerate(episodes_lst):

        html = f"https://open.spotify.com/episode/{link[16:]}?si=123e7de133124692&nd=1&dlsi=ad207e177da14244"
        st.page_link(html, label=episode_names[i])
        ep_links.append(html)
        st.write(descriptions[i])
