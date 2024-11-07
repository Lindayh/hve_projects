import streamlit as st 
from  fns import make_gradcam_heatmap, save_and_display_gradcam, load_VGG_models

import numpy as np
import tensorflow as tf
import keras

# Display
from IPython.display import Image, display
import matplotlib as mpl
import matplotlib.pyplot as plt

from keras import backend as K
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import pandas as pd
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.applications.vgg16 import decode_predictions
import numpy as np
import seaborn as sns
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

import warnings 
warnings.filterwarnings('ignore')

model = tf.keras.models.load_model('models/GridSearch_customModel.keras')  



# Streamlit
st.set_page_config(layout="wide")

box = st.container()

row1, row2 = box.container(), box.container()

row1_col1, row1_col2 = row1.columns(2)

user_image = row1_col1.file_uploader(label='Upload an image:', accept_multiple_files=False, type=['png', 'jpg', 'webp', 'bmp'])

if user_image!=None:

        result_box = st.container()
        col1, col2, col3 = row2.columns([0.3, 0.2, 0.7])

        # ---------- Col 2 ----------
        # Show results
        show_img = image.load_img(user_image)
        w, h = show_img.size

        base_height = 300
        if h > base_height:
                hpercent = base_height / float(h)
                w = int(w * hpercent)
                h = base_height

        show_img = image.load_img(user_image, target_size= (h, w))


        # Process img as needed for the model
        img = image.load_img(user_image, target_size=(32, 32))

        img = image.img_to_array(img)
        img = preprocess_input(img, data_format=None)
        img = img/255.0

        img = np.expand_dims(img, axis=0)

        # Predict
        img_pred = model.predict(img)
        print(img_pred)
        result = (img_pred > 0.5).astype(int)

        row1_col2.image(show_img)


        if result == 0:
                st.html('<center><h1>Image classified as: FAKE</h1></center>')
        else:
                st.html('<center><h1>Image classified as: REAL</h1></center>')

        









