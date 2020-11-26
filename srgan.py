import tensorflow as tf

import numpy as np
from numpy import asarray
import matplotlib.pyplot as plt
from tensorflow.keras import Input, Model


from image_preprocess import crop, preprocessing


def apply_srgan(image):
    # model load
    srgan = tf.keras.models.load_model("./model/srgan_G.h5")

    image = tf.cast(image[np.newaxis, ...], tf.float32)
    sr = srgan.predict(image)
    sr = tf.clip_by_value(sr, 0, 255)
    sr = tf.round(sr)
    sr = tf.cast(sr, tf.uint8)
    return np.array(sr)[0]