import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from dotenv import load_dotenv
from io import BytesIO
from os import environ
from PIL import Image
import requests

load_dotenv()

SPOTIPY_CLIENT_ID = environ.get('CLIENT_ID')
SPOTIPY_CLIENT_SECRET = environ.get('CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = 'http://localhost'
SCOPE = 'user-library-read'

class SpotifyClient():
  def __init__(self):
    self.client = self._get_client()

  def _get_client(self):
    auth_manager = SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
    return spotipy.Spotify(auth_manager=auth_manager)

  def get_playlist_tracks(self, playlist_id):
    items = self.client.playlist_tracks(playlist_id=playlist_id)['items']
    return [track['track'] for track in items]
  
  def get_playlist_name(self, playlist_id):
    return self.client.playlist(playlist_id)['name']


class ImageManager():
  @staticmethod
  def load_image_from_url(url):
    resp = requests.get(url)
    return Image.open(BytesIO(resp.content))  
