import requests
from icecream import ic
import streamlit as st
import pickle
from pathlib import Path
import bcrypt
import streamlit_authenticator as auth


st.set_page_config(page_title="Episodes", page_icon=":material/edit:", layout="wide",
				   initial_sidebar_state="collapsed")

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
latest_desc = ''
response = response['data']['podcastUnionV2']['episodesV2']['items']

with open('data/filter.txt', 'r') as file:
	keyword = file.readlines()
	keyword = [keywords.strip() for keywords in keyword]

for episode in response:

	if 'entity' in episode:
		entity_data = episode['entity']['data']

		ep_code = entity_data.get('uri', '')

		description = entity_data.get('description', '').split()

		for word in description:
			if word in keyword:
				episodes_lst.append(ep_code)
				break

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

for l in response:
	if 'entity' in k:
		try:
			if k['entity']['_uri'] == episodes_lst[0]:
				latest_desc = k['entity']['data']['description']
		except IndexError:
			continue


def update_content(value):
	container.write(value)


def add():
	global add_txt
	new_word = st.session_state.add_txt
	keyword.append(new_word)
	with open('data/filter.txt', 'w') as file:
		for word in keyword:
			file.writelines(word + "\n")


def sub():
	global add_txt
	sub_word = st.session_state.sub_txt
	keyword.remove(sub_word)
	with open('data/filter.txt', 'w') as file:
		for word in keyword:
			file.writelines(word + "\n")


def clear():
	keyword.clear()
	keyword.append("")
	with open('data/filter.txt', 'w') as file:
		for word in keyword:
			file.writelines(word)

ep_links = []

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
	sub_txt = st.text_input(key='sub_txt', label='Remove Filter', placeholder='Enter a Filter Word to Remove', on_change=sub)
	clear = st.button('Clear', key='clear', on_click=clear)
	st.write(keyword)

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


# dialog_placeholder = st.empty()
# 	# A button to trigger the "popup" dialog
# 	if st.button("Sign-Up"):
# 		# Use the placeholder to display the dialog content
# 		with dialog_placeholder.container():
# 			st.write("Sign-Up")
# 			try:
# 				for i in range(1):
# 					st.write("Username: ")
# 					uname_s = st.text_input(label="Username", key="username", on_change=None, type='default')
# 					st.write("Password: ")
# 					psswd_s = st.text_input(label="Password", key="password", on_change=None, type="password")
# 			except Exception as e:
# 				ic('Exception')
#
# 			if st.button("Sign-Up"):
# 				add_user(uname_s, psswd_s)
# 			if st.button("Close"):
# 				# Clear the dialog content
# 				dialog_placeholder.empty()
#
# 	if st.button("Login"):
# 		# Use the placeholder to display the dialog content
# 		with dialog_placeholder.container():
# 			st.write("Login")
# 			st.write("Username: ")
# 			uname_l = st.text_input(key='uname', label="Username")
# 			st.write("Password: ")
# 			uname_l = st.text_input(key='pwd', label="Password")
# 			if st.button("Login"):
# 				check_user(uname_l, uname_s)
# 			if st.button("Close"):
# 				# Clear the dialog content
# 				dialog_placeholder.empty()
