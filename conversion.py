from .__utils__ import suppressor
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
        raise ValueError(">> Specify the path where to save the model: Ex: C:/Users/User/Desktop/My_Models")
    if format == "":
        raise ValueError(">> Specify the format in exporting the model. (Ex: tflite, save_model, keras, onnx, h5)")
    if not model:
        raise ValueError(">> No model to export. You need to pass it as a parameter when Calling exporter() function")
    if not model_name:
        raise ValueError(">> Enter the model name before saving..")

     # Extract directory and make sure it exists
    export_dir = os.path.dirname(save_path)
    os.makedirs(export_dir, exist_ok=True)

    if format == "h5":
        model.save(f"{model_name}.h5")
        print(f"[✔] Exported as HDF5: {model_name}.h5")

    elif format == "saved_model":
        model.save(save_path, save_format="tf")
        print(f"[✔] Exported as TensorFlow SavedModel at: {save_path}/")

    elif format == "tflite":
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        tflite_model = converter.convert()
        with open(f"{model_name}.tflite", "wb") as f:
            f.write(tflite_model)
        print(f"[✔] Exported as TFLite: {model_name}.tflite")

    elif format == "onnx":
        try:
            import keras2onnx
            import onnx
            onnx_model = keras2onnx.convert_keras(model, model.name)
            onnx.save_model(onnx_model, f"{model_name}.onnx")
            print(f"[✔] Exported as ONNX: {model_name}.onnx")
        except ImportError:
            print("[✘] ONNX export failed. Please install keras2onnx and onnx with pip.")
    else:
        raise ValueError(f"[✘] Unsupported export format: {format}")