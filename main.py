import requests
from icecream import ic


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


# for episode in response['data']['podcastUnionV2']['episodesV2']['items']:
# 	if ep_code in episode['entity']['data']['uri']:
# 		episodes_dsc.append(episode['entity']['data']['description'])


ic(episodes_lst)
ic(episodes_dsc)

# for k, item in enumerate(response['data']['podcastUnionV2']['episodesV2']['items'][0]['entity']['data']):
# 	if item == 'description':
# 		if keyword in item['description']:
# 			ic(response['data']['podcastUnionV2']['episodesV2']['items'][0]['entity'][episodes[k]])
