from .__utils__ import suppressor, ANSI
suppressor.suppress()
import tensorflow as tf
import os


def exporter(model, model_name, format):
    """
        Parameters:
            model: Pass the model variable returned from the function that trains the model

            model_name: Specify the model name to use for exporting the model

            format: specify the format for converting and exporting
                available formats:
                - tflite
                - keras
                - h5
                - onnx
                - saved_model <- native tensorflow format
    """


    # This will save the model by default but as a keras format only. The purpose is this will serve as backup model if there's a problem in exporting to other formats.
    print(f'\n{ANSI.yellow()}===============================================================')
    print(">> This is Fail-Safe mechanism in action.. Exporting keras model..")
    model_path = os.path.join(os.getcwd(), 'Saved_model.keras')
    model.save(model_path)
    print(f"[!] Saved_model.keras is exported by default. You can convert this to other formats later on.")
    print(f'==============================================================={ANSI.reset()}\n')

    if format == "":
        raise ValueError(f"{ANSI.red()}>> Specify the format in exporting the model. (Ex: tflite, save_model, keras, onnx, h5){ANSI.reset()}")
    if not model:
        raise ValueError(f"{ANSI.red()}>> No model to export. You need to pass it as a parameter when Calling exporter() function{ANSI.reset()}")
    if not model_name:
        raise ValueError(f"{ANSI.red()}>> Enter the model name before saving..{ANSI.reset()}")
    
    


    if format == "h5":
        path = os.path.join(os.getcwd(), f"{model_name}.h5")
        model.save(path)
        print(f"[✔] Exported as HDF5: {ANSI.green()}{path}{ANSI.reset()}")

    elif format == "saved_model":
        path = os.path.join(os.getcwd(), f"{model_name}_saved_model")
        model.save(path)
        print(f"[✔] Exported as TensorFlow SavedModel at: {ANSI.green()}{path}{ANSI.reset()}")

    elif format == "tflite":
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        tflite_model = converter.convert()
        path = os.path.join(os.getcwd(), f"{model_name}.tflite")
        with open(path, "wb") as f:
            f.write(tflite_model)
        print(f"[✔] Exported as TFLite: {ANSI.green()}{path}{ANSI.reset()}")

    elif format == "onnx":
        try:
            import keras2onnx
            import onnx
            onnx_model = keras2onnx.convert_keras(model, model.name)
            path = os.path.join(os.getcwd(), f"{model_name}.onnx")
            onnx.save_model(onnx_model, path)
            print(f"[✔] Exported as ONNX: {ANSI.green()}{path}{ANSI.reset()}")
        except ImportError:
            print(f"{ANSI.red()}[✘] ONNX export failed. Please install keras2onnx and onnx with pip.{ANSI.reset()}")
    else:
        raise ValueError(f"{ANSI.red()}[✘] Unsupported export format: {format}{ANSI.reset()}")