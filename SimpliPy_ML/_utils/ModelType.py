import os
import tensorflow as tf
from ._ANSI import *
import sys
from keras.utils import custom_object_scope

class MeanMaxPooling(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super(MeanMaxPooling, self).__init__(**kwargs)
    def call(self, inputs):
        return (tf.reduce_mean(inputs, axis=1) + tf.reduce_max(inputs, axis=1)) / 2

def getModelType(model):
    """
        load a model to identify it's format automatically

        Returns:
            tuble : 
                - model: Loaded model
                - model_type (str): returns what type of format (.tflite, h5, onnx)
    """

    file_extension = os.path.splitext(model)[1].lower() # get the model fornat

    if file_extension == ".tflite":
        interpreter = tf.lite.Interpreter(model_path = model)
        interpreter.allocate_tensors()
        return interpreter, '.tflite'
    elif file_extension == ".h5":
        with custom_object_scope({'MeanMaxPooling': MeanMaxPooling}):
            model = tf.keras.models.load_model(model)
        return model, '.h5'
    elif file_extension == ".onnx":
        try:
            import onnxruntime as ort
            session = ort.InferenceSession(model)
            return session, '.onnx'
        except:
            print(f"{red()}>> [!] Please install onnxruntime first{reset()}")
    else:
        raise ValueError(f"\n{red()}>> Unsupported file extension {file_extension} {reset()}")