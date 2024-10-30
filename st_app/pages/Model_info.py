import streamlit as st
from  fns import load_models
import keras


model_base, model = load_models()

st.header(f'Model: {model_base.name.capitalize()}')
# Layer details 
for i, layer in enumerate(model.layers):

    if type(layer).__name__=="Functional":
        for j, nested_layer in enumerate(layer.layers):
            layer_info_box = st.container(height=100)
            cols = layer_info_box.columns(3)

            cols[0].write(f'{nested_layer.name}')
            cols[0].write(f'Type: {type(nested_layer).__name__}')

            if 'input' in nested_layer.name and layer.input.shape: cols[1].write(f'Input: {layer.input.shape}')
            if hasattr(nested_layer, 'units'): cols[1].write(f'Neurons: {nested_layer.units}')
            if hasattr(nested_layer, 'kernel'): cols[1].write(f'Kernel: {nested_layer.kernel.shape}')
            cols[1].write(f'Output: {nested_layer.output.shape}')

            if hasattr(nested_layer, 'activation'): cols[2].write(f'{nested_layer.activation.__name__}')


        # activation_fn = layer.activation.__name__ if hasattr(layer, 'activation') else None,
        # params = layer.count_params(),

        # )
    else:

        layer_info_box = st.container(height=100)
        cols = layer_info_box.columns(3)

        cols[0].write(layer.name)
        cols[0].write(f'Type: {type(layer).__name__}')

        if 'input' in layer.name: cols[1].write(f'Input: {layer.input}')
        if hasattr(layer, 'units'): cols[1].write(f'Neurons: {layer.units}')
        cols[1].write(f'Output: {layer.output.shape}')

        if hasattr(layer, 'activation'): cols[2].write(f'{layer.activation.__name__}')










