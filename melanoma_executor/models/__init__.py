import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

model = tf.keras.models.load_model(f'{os.path.dirname(os.path.abspath(__file__))}/melanoma_model.h5')

def runModel(img_path, model):
    img = image.load_img(img_path, target_size=(256, 256))
    x = image.img_to_array(img) / 255.0
    x = np.expand_dims(x, axis=0)
    prediction = model.predict(x)
    return prediction


