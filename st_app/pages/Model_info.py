import streamlit as st
from  fns import load_models
import keras

model_base, model = load_models()

model_plot = keras.utils.plot_model(model, expand_nested=True)

st.pyplot( model_plot )








