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
import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

import warnings 
warnings.filterwarnings('ignore')

def dl_vgg16_weights():
    import urllib.request
    urllib.request.urlretrieve("https://drive.usercontent.google.com/download?id=1pjhNKzdLn1Oci58fp50dxU198rApb4_8&export=download&confirm=t&uuid=8513c6b5-33a4-43f9-a966-d2e464974dac", 
                               "models/VGG16_model.weights.h5")





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
        # img_pred = model.predict(img)
        # print(img_pred)
        # result = (img_pred > 0.5).astype(int)

        # if result == 0:
        #         row1_col2.write('Image classified as: FAKE')
        # else:
        #         row1_col2.write('Image classified as: REAL')
        
        # row1_col2.write(f'{img_pred}')

        row1_col2.write('Your image:')

        row1_col2.image(show_img)
        

        # ---------- Col 1 ----------
        # Load model

        if os.path.isfile('models/VGG16_model.weights.h5')==False:
                st.write('Important: weights for VGG16 not found, can\'t run the model without them.')
                st.write('Do you want to download?')
                st.button('Download weights', on_click=dl_vgg16_weights)

        else:

                model_base, model = load_VGG_models()

                col1.write('Choose a layer to show GRAD-CAM:')

                for i, layer in enumerate(model_base.layers):
                        if "conv" in layer.name or 'pool' in layer.name:

                                layer_name = col1.button(layer.name)

                                if layer_name: 
                                        layer_name = layer.name
                                        try:
                                                heatmap = make_gradcam_heatmap(img, model_base, layer_name, pred_index=0)

                                                col2.write('Layer heatmap:')

                                                plt.matshow(heatmap, aspect='auto')
                                                plt.axis('off')
                                                plt.savefig('layer_heatmap.png', transparent=True, bbox_inches='tight')

                                                # img = heatmap_matshow.imgsave
                                                # col2.write(type(heatmap))
                                                col2.image('layer_heatmap.png')

                                                col3.write('Superimposed heatmap:')
                                                superimposed_img = save_and_display_gradcam(user_image, heatmap)     
                                                col3.image(superimposed_img) 
                                        
                                        except Exception as e:
                                                col2.write('Error occurred while generating heatmap, choose another layer.')










