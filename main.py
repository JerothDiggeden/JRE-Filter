import requests
from icecream import ic
import streamlit as st


st.set_page_config(page_title="Episodes", page_icon=":material/edit:", layout="wide",
				   initial_sidebar_state="expanded")

col1, col2 = st.columns([1, 2])

url = "https://spotify23.p.rapidapi.com/podcast_episodes/"

querystring = {"id": "4rOoJ6Egrf8K2IrywzwOMk", "offset": "0", "limit": "330"}

headers = {
	"x-rapidapi-key": "1b6ce2494dmshf74f9c461b4cdbbp1d3b11jsndd6ab0d8575c",
	"x-rapidapi-host": "spotify23.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

response = response.json()

keyword = ['Patrick', 'Doblin', 'Stamets', 'Hancock', 'Carlson', 'Trussell',
		   'Degrass', 'Kaku', 'Ryan', 'Weinstein', 'Peterson', 'Musk',
		   'Shapiro', 'Harris', 'Rubin', 'UFO', 'UAP', 'Nutrition', 'Hunting', 'Psychedelic', 'PhD', 'Ph.D', 'Ph.D.',
		   'Masters', 'Dr', 'Author', 'Anthropology', 'Archeology', 'Biology', 'Musician']

# EPISODE CODE LIST
episodes_lst = []
episodes_dsc = []
response = response['data']['podcastUnionV2']['episodesV2']['items']

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
episodes_dict = {}
episode_names = []

for uri in response:
	if 'entity' in uri:
		count = 0
		if uri['entity']['_uri'] in episodes_lst:
			ic(uri)
			entity_data = uri['entity']['data']['description']
			episodes_dict[uri['entity']['data']['name']] = entity_data
			episode_names.append(uri['entity']['data']['name'])
			uri = uri
		count += 1

# DESCRIPTIONS LIST
descriptions = []
latest_desc = ''

for k in response:
	if 'entity' in k:
		if k['entity']['_uri'] in episodes_lst:
			descriptions.append(k['entity']['data']['description'])

for l in response:
	if 'entity' in k:
		if k['entity']['_uri'] == episodes_lst[0]:
			latest_desc = k['entity']['data']['description']


def clear():
	keyword.clear()


def update_content(value):
	container.write(value)


# PAGE LAYOUT
ep_links = []

# Using object notation
# st.sidebar.selectbox(label="Sidebar", options='', index=0)

# Using "with" notation
with st.sidebar:
	container = st.empty()
	pic = response[0]['entity']['data']['podcastV2']['data']['coverArt']['sources'][1]['url']
	pic2 = response[0]['entity']['data']['coverArt']['sources'][1]['url']
	pic3 = response[0]['entity']['data']['coverArt']['sources'][1]['url']
	st.title('My JRE Filter')
	st.image(pic, use_column_width=False)
	st.title('Filter: ')
	st.write(keyword)

with col1:
	latest_name = response[0]['entity']['data']['name']
	latest_desc = response[0]['entity']['data']['description']
	latest_html = response[0]['entity']['data']['sharingInfo']['shareUrl']

	length = len(episodes_lst)
	latest_filtered = episodes_lst[length - 1]
	latest_filtered = f"https://open.spotify.com/episode/{latest_filtered[16:]}?si=123e7de133124692&nd=1&dlsi=ad207e177da14244"

	st.title('Latest Episode: ')
	st.image(pic2, use_column_width=False)
	st.page_link(latest_html, label=latest_name)
	st.write(latest_desc)

	st.title('Filtered Episode: ')
	st.image(pic3, use_column_width=False)
	st.write(descriptions[0])

	st.page_link(latest_filtered, label=latest_name)

	st.title('Old Episodes: ')

	for i, link in enumerate(episodes_lst):
		html = f"https://open.spotify.com/episode/{link[16:]}?si=123e7de133124692&nd=1&dlsi=ad207e177da14244"
		st.page_link(html, label=episode_names[i])
		ep_links.append(html)
		st.write(descriptions[i])
