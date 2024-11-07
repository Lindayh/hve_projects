import streamlit as st
from  fns import load_VGG_models
import tensorflow as tf


model_base, model = load_VGG_models()

custom_CNN = tf.keras.models.load_model('models/GridSearch_customModel.keras') 

def show_model_info(model, model_name, model_type:str):
    st.header(f'Model: {model_name}')
    st.write('')
    st.write(f'Optimizer: {model.optimizer.name}')
    st.write('')

    for i, layer in enumerate(model.layers):

        if type(layer).__name__==model_type:
            st.write(layer.name.capitalize())
            col1, col2 = st.columns([0.03, 1])
            for j, nested_layer in enumerate(layer.layers):
                layer_info_box = col2.container(height=100)
                cols = layer_info_box.columns(3)

                cols[0].write(f'{nested_layer.name}')
                cols[0].write(f'Type: {type(nested_layer).__name__}')

                if 'input' in nested_layer.name and layer.input.shape: cols[1].write(f'Input: {layer.input.shape}')
                if hasattr(nested_layer, 'units'): cols[1].write(f'Neurons: {nested_layer.units}')
                if hasattr(nested_layer, 'kernel'): cols[1].write(f'Kernel: {nested_layer.kernel.shape}')
                cols[1].write(f'Output: {nested_layer.output.shape}')

                if hasattr(nested_layer, 'activation'): cols[2].write(f'{nested_layer.activation.__name__}')
        else:

            layer_info_box = st.container(height=100)
            cols = layer_info_box.columns(3)

            cols[0].write(layer.name)
            cols[0].write(f'Type: {type(layer).__name__}')

            if 'input' in layer.name: cols[1].write(f'Input: {layer.input}') if layer.input != [] else ''
            if hasattr(layer, 'units'): cols[1].write(f'Neurons: {layer.units}')
            cols[1].write(f'Output: {layer.output.shape}')

            if hasattr(layer, 'activation'): cols[2].write(f'{layer.activation.__name__}')

   


st.header('Models:')

st.button('VGG 16', on_click=show_model_info, args=(model, model_base.name.capitalize(), 'Functional') )
st.button('Custom CNN', on_click=show_model_info, args=(custom_CNN, 'Custom CNN', 'Sequential'))








