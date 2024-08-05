import requests
from icecream import ic
import streamlit as st


st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

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
		   'Shapiro', 'Harris', 'Rubin', 'UFO', 'UAP', 'Nutrition', 'Hunting', 'Psychedelic', 'PHD',
		   'Masters', 'Author', 'Anthropology', 'Archeology', 'Biology', 'Musician']

episodes_lst = []
episodes_dsc = []

for episode in response['data']['podcastUnionV2']['episodesV2']['items']:

	if 'entity' in episode:
		entity_data = episode['entity']['data']

		ep_code = entity_data.get('uri', '')

		description = entity_data.get('description', '').split()

		for word in description:
			if word in keyword:
				episodes_lst.append(ep_code)
				break

episodes_dict = {}
episode_names = []

for uri in response['data']['podcastUnionV2']['episodesV2']['items']:
	if 'entity' in uri:
		count = 0
		if uri['entity']['_uri'] in episodes_lst:
			ic(uri)
			entity_data = uri['entity']['data']['description']
			episodes_dict[uri['entity']['data']['name']] = entity_data
			episode_names.append(uri['entity']['data']['name'])
			uri = uri
		count += 1

ep_links = []

with (col1):
	pic = response['data']['podcastUnionV2']['episodesV2']['items'][0]['entity']['data']['podcastV2']['data']['coverArt']['sources'][1]['url']
	pic2 = response['data']['podcastUnionV2']['episodesV2']['items'][0]['entity']['data']['coverArt']['sources'][1]['url']
	pic3 = response['data']['podcastUnionV2']['episodesV2']['items'][0]['entity']['data']['coverArt']['sources'][1]['url']
	st.title('My JRE Filter')
	st.image(pic, caption='JRE Filter', use_column_width=False)


with col2:
	latest_name = response['data']['podcastUnionV2']['episodesV2']['items'][0]['entity']['data']['name']
	latest_desc = response['data']['podcastUnionV2']['episodesV2']['items'][0]['entity']['data']['description']
	latest_html = response['data']['podcastUnionV2']['episodesV2']['items'][0]['entity']['data']['sharingInfo']['shareUrl']

	length = len(episodes_lst)
	latest_filtered = episodes_lst[length - 1]
	latest_filtered = f"https://open.spotify.com/episode/{latest_filtered[16:]}?si=123e7de133124692&nd=1&dlsi=ad207e177da14244"

	st.title('Latest Episode: ')
	st.image(pic2, caption='JRE Filter', use_column_width=False)
	st.page_link(latest_html, label=latest_name)

	st.title('Filtered Episode: ')
	st.image(pic3, caption='JRE Filter', use_column_width=False)

	st.page_link(latest_filtered, label=latest_name)

	st.title('Old Episodes: ')

	for i, link in enumerate(episodes_lst):
		html = f"https://open.spotify.com/episode/{link[16:]}?si=123e7de133124692&nd=1&dlsi=ad207e177da14244"
		st.page_link(html, label=episode_names[i])
		ep_links.append(html)
