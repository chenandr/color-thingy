import urllib.request
import tensorflow as tf
import numpy as np


class Classifier():
  color_map={
    0 : 'Red',
    1 : 'Green',
    2 : 'Blue',
    3 : 'Yellow',
    4 : 'Orange',
    5 : 'Pink',
    6 : 'Purple',
    7 : 'Brown',
    8 : 'Grey',
    9 : 'Black',
    10 : 'White'
  }
  
  def __init__(self):
    urllib.request.urlretrieve('https://github.com/AjinkyaChavan9/RGB-Color-Classifier-with-Deep-Learning-using-Keras-and-Tensorflow/blob/master/RGB%20Color%20Classifier%20ML%20Model/colormodel_trained_89.h5?raw=true', 'colormodel_trained_89.h5')
    self.model = tf.keras.models.load_model('colormodel_trained_89.h5') 

  def evaluate_image(self, image_pxs):
    input = np.asarray(image_pxs)
    pixel_color_confidences = self.model.predict(input)
    color_indexes = np.argmax(pixel_color_confidences, axis=1)
    colors = [self.color_map[int(color_index)] for color_index in color_indexes]
    return colors
    

  def get_pixel_color(self, px):
    input = np.asarray(px)
    input = np.reshape(input, (-1,3))
    color_class_confidence = self.model.predict(input)
    color_index = np.argmax(color_class_confidence, axis=1)
    color = self.color_map[int(color_index)]
    return color
