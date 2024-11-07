import streamlit as st
import os


def show_model_info(model_name, model_type:str):

    if 'VGG' in model_name:
        from  fns import load_VGG_models
        model_base, model = load_VGG_models(load_weights=False)
    
    if model_name == 'Custom CNN':
        from tensorflow.keras.models import load_model
        model = load_model('models/GridSearch_customModel.keras') 

    box2.header(f'Model: {model_name}')
    box2.write('')
    box2.write(f'Optimizer: {model.optimizer.name}')
    box2.write('')

    for i, layer in enumerate(model.layers):

        if type(layer).__name__==model_type:
            box2.write(layer.name.capitalize())
            col1, col2 = box2.columns([0.03, 1])
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

            layer_info_box = box2.container(height=100)
            cols = layer_info_box.columns(3)

            cols[0].write(layer.name)
            cols[0].write(f'Type: {type(layer).__name__}')

            if 'input' in layer.name: cols[1].write(f'Input: {layer.input}') if layer.input != [] else ''
            if hasattr(layer, 'units'): cols[1].write(f'Neurons: {layer.units}')
            cols[1].write(f'Output: {layer.output.shape}')

            if hasattr(layer, 'activation'): cols[2].write(f'{layer.activation.__name__}')


box1 = st.container()

box1.header('Models:')
box1_col1, box1_col2, _ = box1.columns([0.2,0.2, 0.7])

box1_col1.button('VGG 16', on_click=show_model_info, args=('VGG 16', 'Functional') )
box1_col2.button('Custom CNN', on_click=show_model_info, args=('Custom CNN', 'Sequential'))

box2 = st.container()








