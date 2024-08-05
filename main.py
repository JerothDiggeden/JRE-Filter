import requests
from icecream import ic
import streamlit as st

st.title('JRE Spotify Episodes')
col1, col2 = st.columns(2)

url = "https://spotify23.p.rapidapi.com/podcast_episodes/"

querystring = {"id": "4rOoJ6Egrf8K2IrywzwOMk", "offset": "0", "limit": "330"}

headers = {
	"x-rapidapi-key": "1b6ce2494dmshf74f9c461b4cdbbp1d3b11jsndd6ab0d8575c",
	"x-rapidapi-host": "spotify23.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

ic(response.json())

response = response.json()
ic(response)
keyword = ['Patrick', 'Doblin', 'Stamets', 'Hancock', 'Carlson', 'Trussell',
		   'Degrass', 'Kaku', 'Ryan', 'Weinstein', 'Peterson', 'Musk',
		   'Shapiro', 'Harris', 'Rubin', 'UFO', 'UAP', 'Nutrition', 'Hunting', 'Psychedelic', 'PHD',
		   'Masters', 'Author', 'Anthropology', 'Archeology', 'Biology', 'Musician']
episodes_lst = []
episodes_dsc = []

ic(response['data']['podcastUnionV2']['episodesV2']['items'][0]['entity']['data']['description'])

for episode in response['data']['podcastUnionV2']['episodesV2']['items']:
	# Check if 'entity' key exists in the current episode
	if 'entity' in episode:
		entity_data = episode['entity']['data']

		# Get the episode's URI
		ep_code = entity_data.get('uri', '')

		# Get the description and split it into words
		description = entity_data.get('description', '').split()

		# Iterate over the words in the description
		for word in description:
			if word in keyword:
				# Append the URI to the list if the keyword is found
				episodes_lst.append(ep_code)
				break  # Stop searching in this episode's description after finding the keyword


# for i, code in enumerate(episodes_lst.copy()):
# 	episodes_lst[i] = code[16:]

ic(episodes_lst)

episodes_dict = {}
episode_names = []

for uri in response['data']['podcastUnionV2']['episodesV2']['items']:
	if 'entity' in uri:
		count = 0
		ic(uri)
		if uri['entity']['_uri'] in episodes_lst:
			ic(uri)
			entity_data = uri['entity']['data']['description']
			episodes_dict[uri['entity']['data']['name']] = entity_data
			episode_names.append(uri['entity']['data']['name'])
			uri = uri
		count += 1

ep_links = []

with (col1):
	for i, link in enumerate(episodes_lst):
		html = f"https://open.spotify.com/episode/{link[16:]}?si=123e7de133124692&nd=1&dlsi=ad207e177da14244"
		st.page_link(html, label=episode_names[i])
		ep_links.append(html)
		# for label in response['data']['podcastUnionV2']['episodesV2']['items']:
		# 	if 'entity' in label:
		# 		if label['entity']['_uri'] in episodes_lst:

