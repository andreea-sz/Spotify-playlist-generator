from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
import requests
import spotipy
import os

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

user_answer = input("What year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{user_answer}")
soup = BeautifulSoup(response.text, "html.parser")

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

spotipy_obj = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                        client_secret=client_secret,
                                                        redirect_uri="http://example.com",
                                                        scope="playlist-modify-private",
                                                        cache_path="token.txt"))

spotify_user_id = spotipy_obj.current_user()['id']


song_uri_list = []
for song_name in song_names:
    song_search = spotipy_obj.search(q=f'track:{song_name} year:{user_answer[:4]}', limit=1, type='track')
    try:
        song_uri= song_search['tracks']['items'][0]['uri']
        song_uri_list.append(song_uri)
    except IndexError:
        print(f"{song_name} was not found. It will be skipped!")


playlist = spotipy_obj.user_playlist_create(user=spotify_user_id,
                                            name=f"{user_answer} Billboard",
                                            public=False,
                                            description=f"Top songs from {user_answer}")

spotipy_obj.playlist_add_items(playlist_id=playlist['id'], items=song_uri_list)

