from .__utils__ import suppressor, ANSI
suppressor.suppress()
import tensorflow as tf
import os

def exporter(model, save_path, model_name, format):
    """
        Parameters:
            model: Pass the model variable returned from the function that trains the model

            save_path: Specify the path directory to save the model

            model_name: Specify the model name to use for exporting the model

            format: specify the format for converting and exporting
                available formats:
                - tflite
                - keras
                - h5
                - onnx
                - saved_model <- native tensorflow format
    """
    if save_path == "":
        raise ValueError(f"{ANSI.red()}>> Specify the path where to save the model: Ex: C:/Users/User/Desktop/My_Models{ANSI.reset()}")
    if format == "":
        raise ValueError(f"{ANSI.red()}>> Specify the format in exporting the model. (Ex: tflite, save_model, keras, onnx, h5){ANSI.reset()}")
    if not model:
        raise ValueError(f"{ANSI.red()}>> No model to export. You need to pass it as a parameter when Calling exporter() function{ANSI.reset()}")
    if not model_name:
        raise ValueError(f"{ANSI.red()}>> Enter the model name before saving..{ANSI.reset()}")

     # Extract directory and make sure it exists
    export_dir = os.path.dirname(save_path)
    os.makedirs(export_dir, exist_ok=True)

    if format == "h5":
        model.save(f"{model_name}.h5")
        print(f"[✔] Exported as HDF5: {model_name}.h5{ANSI.reset()}")

    elif format == "saved_model":
        model.save(save_path, save_format="tf")
        print(f"[✔] Exported as TensorFlow SavedModel at: {ANSI.green()}{save_path}/{ANSI.reset()}")

    elif format == "tflite":
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        tflite_model = converter.convert()
        with open(f"{model_name}.tflite", "wb") as f:
            f.write(tflite_model)
        print(f"[✔] Exported as TFLite: {ANSI.green()}{model_name}.tflite{ANSI.reset()}")

    elif format == "onnx":
        try:
            import keras2onnx
            import onnx
            onnx_model = keras2onnx.convert_keras(model, model.name)
            onnx.save_model(onnx_model, f"{model_name}.onnx")
            print(f"[✔] Exported as ONNX: {ANSI.green()}{model_name}.onnx{ANSI.reset()}")
        except ImportError:
            print(f"{ANSI.red()}[✘] ONNX export failed. Please install keras2onnx and onnx with pip.{ANSI.reset()}")
    else:
        raise ValueError(f"[✘] Unsupported export format: {format}")