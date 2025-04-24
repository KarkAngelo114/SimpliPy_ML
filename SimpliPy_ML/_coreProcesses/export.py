from .._utils import suppressor, _ANSI
suppressor.suppress()
import tensorflow as tf
import os


def export(model):

    model_name = "Trained_Model"


    path = os.path.join(os.getcwd(), f"{model_name}.h5")
    model.save(path)
    print(f"{_ANSI.cyan()}[✔] Exported as HDF5: {_ANSI.yellow()}{path}{_ANSI.reset()}")

    path = os.path.join(os.getcwd(), f"{model_name}_saved_model")
    model.save(path)
    print(f"{_ANSI.cyan()}[✔] Exported as TensorFlow SavedModel at: {_ANSI.yellow()}{path}{_ANSI.reset()}")

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    path = os.path.join(os.getcwd(), f"{model_name}.tflite")
    with open(path, "wb") as f:
        f.write(tflite_model)
    print(f"{_ANSI.cyan()}[✔] Exported as TFLite: {_ANSI.yellow()}{path}{_ANSI.reset()}")

    try:
        import keras2onnx
        import onnx

        onnx_model = keras2onnx.convert_keras(model, model.name)
        path = os.path.join(os.getcwd(), f"{model_name}.onnx")
        onnx.save_model(onnx_model, path)
        print(f"{_ANSI.cyan()}[✔] Exported as ONNX: {_ANSI.yellow()}{path}{_ANSI.reset()}")
    except ImportError:
        print(f"{_ANSI.red()}[✘] ONNX export failed. Please install keras2onnx and onnx with pip.{_ANSI.reset()}")