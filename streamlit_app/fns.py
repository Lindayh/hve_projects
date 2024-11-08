import os

import numpy as np
import tensorflow as tf
import keras

import matplotlib as mpl
from keras import backend as K
from keras.preprocessing import image
import numpy as np
import seaborn as sns
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import tensorflow.keras

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, Conv2D, Flatten
from tensorflow.keras import regularizers
from IPython.display import Image

import warnings 
warnings.filterwarnings('ignore')

def load_VGG_models(load_weights=True):
    VGG16_base_model = tf.keras.applications.VGG16(
    include_top = False, 
    weights = 'imagenet', 
    input_shape = (32,32, 3),
    # pooling = 'max'
    )
    VGG16_base_model.trainable = False

    inputs = tf.keras.Input(shape = (32,32, 3))
    x = VGG16_base_model(inputs, training = False)

    x = BatchNormalization(axis = -1, momentum = 0.99, epsilon = 0.001)(x)
    x = Dense(256, 
            kernel_regularizer = regularizers.l2(0.01), 
            activity_regularizer = regularizers.l1(0.01), 
            bias_regularizer = regularizers.l1(0.01),
            activation = 'relu')(x)
    x = Dropout(rate = .4, seed = 512)(x)       
    x = Dense(64, activation = 'relu')(x)

    outputs = Dense(1, activation = 'sigmoid')(x)
    VGG16_model = tf.keras.Model(inputs, outputs)

    VGG16_model.compile(
        optimizer = 'adam',
        loss = tf.keras.losses.BinaryCrossentropy(),
        metrics = ['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
    )

    if load_weights == True:
        VGG16_model.load_weights("models/VGG16_model.weights.h5")

    return [VGG16_base_model, VGG16_model]


def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):

    grad_model = keras.models.Model(
        model.inputs, [model.get_layer(last_conv_layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)  
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    grads = tape.gradient(class_channel, last_conv_layer_output)

    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

def save_and_display_gradcam(img, heatmap, cam_path="cam.jpg", alpha=0.9):
    img = image.load_img(img)
    img = keras.utils.img_to_array(img)

    heatmap = np.uint8(255 * heatmap)

    jet = mpl.colormaps["jet"]

    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap]

    jet_heatmap = keras.utils.array_to_img(jet_heatmap)
    jet_heatmap = jet_heatmap.resize((img.shape[1], img.shape[0]))
    jet_heatmap = keras.utils.img_to_array(jet_heatmap)

    superimposed_img = jet_heatmap * alpha + img
    superimposed_img = keras.utils.array_to_img(superimposed_img)

    return superimposed_img

