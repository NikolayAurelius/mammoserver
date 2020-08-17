import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

model = tf.keras.models.load_model(f'{os.path.dirname(os.path.abspath(__file__))}/melanoma_model.h5')

def runModel(img, model):
	x = image.img_to_array(img)
	x = tf.image.resize_with_pad(x, 256, 256)
	x = x/255.0
	x = np.expand_dims(x, axis=0)
	prediction = model.predict(x)
	return prediction


