import base64
import requests

import music_data
from recommendation import hybrid_recommendations

CLIENT_ID = 'ad1f699a8c9c43b1882d7a1a456f8624'
CLIENT_SECRET = '7c2054c57248491e9ac3653a5e8bc1be'

client_credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
client_credentials_base64 = base64.b64encode(client_credentials.encode())

# Request the access token
TOKEN_URL = 'https://accounts.spotify.com/api/token'
headers = {
    'Authorization': f'Basic {client_credentials_base64.decode()}'
}
data = {
    'grant_type': 'client_credentials'
}
response = requests.post(TOKEN_URL, data=data, headers=headers)

playlist_id = '5SbbrGs1cwt3ATxFOBornM'

music_dataframe = None

if response.status_code == 200:
    access_token = response.json()['access_token']
    print("Access token obtained successfully.")

    music_dataframe = music_data.get_trending_playlist_data(playlist_id, access_token)

    input_song_name = "Možda nisam dobar"
    recommendations = hybrid_recommendations(input_song_name, music_dataframe)
    print(f"Hybrid recommended songs for '{input_song_name}':")
    print(recommendations)
else:
    print("Error obtaining access token.")
    exit()


