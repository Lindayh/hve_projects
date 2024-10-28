import streamlit as st 
from  fns import make_gradcam_heatmap, save_and_display_gradcam

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


# Load model
model = load_model('../models/vgg16_01.h5')
model_base = ''

# Streamlit
st.set_page_config(layout="wide")

st.write('Upload an img and get result + grad-cam')

box = st.container()

row1, row2 = box.container(), box.container()

user_image = row1.file_uploader(label='Upload an image:', accept_multiple_files=False)

# try except if one upload a file that isnt an img


if user_image!=None:

        result_box = st.container()
        col1, col2 = row2.columns(2)

        # ---------- Col 2 ----------
        col2.write('Your image:')
        show_img = image.load_img(user_image)
        w, h = show_img.size
        show_img = image.load_img(user_image, target_size= (int(h*0.5), int(w*0.5)))
        col2.image(show_img )

        # Process img as needed for the model
        img = image.load_img(user_image, target_size=(32, 32))

        img = image.img_to_array(img)
        img = preprocess_input(img, data_format=None)
        img = img/255.0

        img = np.expand_dims(img, axis=0)

        # Predict
        img_pred = model.predict(img)
        result = (img_pred > 0.5).astype(int)

        # Show results
        if result == 0:
                col2.write('FAKE')
        else:
                col2.write('REAL')


        # ---------- Col 1 ----------
        col1.write('Choose a convolutional layer to show GRAD-CAM:')


        for i, layer in enumerate(model.layers):
                layer_name = col1.button(layer.name)

                if layer_name: 
                        layer_name = layer.name
                        try:
                                heatmap = make_gradcam_heatmap(img, model, layer_name, pred_index=0)

                                col2.write('Layer heatmap:')

                                plt.matshow(heatmap, aspect='auto')
                                plt.axis('off')
                                plt.savefig('layer_heatmap.png', transparent=True, bbox_inches='tight')

                                # img = heatmap_matshow.imgsave
                                # col2.write(type(heatmap))
                                col2.image('layer_heatmap.png')

                                col2.write('Superimposed heatmap:')
                                superimposed_img = save_and_display_gradcam(user_image, heatmap)     
                                col2.image(superimposed_img) 
                         
                        except Exception as e:
                                # col2.write(e)
                                col2.write('Error occurred while generating heatmap, choose another layer.')








