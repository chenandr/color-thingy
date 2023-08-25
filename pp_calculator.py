from helpers import SpotifyClient, ImageManager
from classifier import Classifier

from urllib.parse import urlparse
from PIL import Image
import time
import os


UNSCALED_HUE_LB = 300
UNSCALED_HUE_UB = 350

def naive(im: Image):
  hue_lb = UNSCALED_HUE_LB * 255 / 360
  hue_ub = UNSCALED_HUE_UB * 255 / 360

  hsv = list(im.convert('HSV').getdata())
  predicate = lambda px: px[0] > hue_lb and px[0] < hue_ub
  filtered = [px if predicate(px) else (0,0,0) for px in hsv]
  pink_count = sum(1 if predicate(px) else 0 for px in hsv)
  pink_proportion = pink_count / (im.width * im.height)

  im2 = Image.new('HSV',im.size)
  im2.putdata(filtered)
  im2 = im2.convert('RGB')
  return im2, pink_proportion


def ml(im):
  ColorClassifier = Classifier()
  rgb = im.getdata()
  pixel_predictions = ColorClassifier.evaluate_image(rgb)
  pink_count = pixel_predictions.count('Pink')
  filtered = [rgb[idx] if color == 'Pink' else (0,0,0) for idx, color in enumerate(pixel_predictions)]
  
  im2 = Image.new('RGB',im.size)
  im2.putdata(filtered)
  pink_proportion = pink_count / (im.width * im.height)
  return im2, pink_proportion


if __name__ == '__main__':
  playlist_url = input('Playlist URI:\n')
  
  start = time.time()
  playlist_id = urlparse(playlist_url).path.split('/')[-1]
  SC = SpotifyClient()
  playlist_name = SC.get_playlist_name(playlist_id)
  print(playlist_name)
  if not os.path.exists(playlist_name):
    os.makedirs(playlist_name)
  
  tracks = SC.get_playlist_tracks(playlist_id)
  track_names = [track['name'] for track in tracks]
  image_urls = [track['album']['images'][0]['url'] for track in tracks]
  
  proportions = []
  for idx, url in enumerate(image_urls):
    with ImageManager.load_image_from_url(url) as im:
      naive_im, naive_pp = naive(im.copy())
      ml_im, ml_pp = ml(im.copy())
      proportions.append({
        'naive_pp': naive_pp,
        'classifier_pp': ml_pp
      })
      im.save(f'./{playlist_name}/{track_names[idx]}.pdf', save_all=True, append_images=[naive_im,ml_im])
  
  with open(f'./{playlist_name}/pp.txt', 'w+') as f:
    for idx, track_name in enumerate(track_names):
      naive_pp = proportions[idx]['naive_pp']
      classifier_pp = proportions[idx]['classifier_pp']
      f.write(f'{track_name:}\n\tnaive_pp: {naive_pp}\n\tclassifier_pp: {classifier_pp}\n')
  
  print(f'Processed {len(track_names)} songs in {time.time() - start} seconds')
