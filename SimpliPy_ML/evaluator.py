from ._utils import suppressor, _ANSI, ModelType, _visualizer
suppressor.suppress()
import os
import numpy as np
import tensorflow as tf
from PIL import Image
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt


def Image_classifier(dir, labels, model_name, input_shape):
    """

        Paramerters:
            dir: specify the directory of the test sets that contains images that will be use for evaluaation of image classification model

            labels: labels will be use as bases for evaluation. The folder names used in training and containing the images are usually used as class names
                be sure that folder names that contains the images for model evaluation matches what is in the label_map.txt.
                You need to emter the filename of the text file that contains the label names
            
            model: load the model to be evaluated

            input_shape: specify the input_shape when loading the dataset, and training the model
                (ex: if you train the model in 224,224 or 224x224, then you need to input the same image shape)
            
            visualize (bool): if set to True, a pop-up window will appear to visualized the performance of the model.

    """

    if not dir:
        raise ValueError(f"\n{_ANSI.red()}>> Please specify the directory and ensure that it exists")
    if not labels:
        raise ValueError(f"\n{_ANSI.red()}>> Please enter the name of the text file that has the label names. ")
    if not model_name:
        raise ValueError(f"\n{_ANSI.red()}>> No Model to be evaluated")
    
    model, model_format = ModelType.getModelType(model_name) # get the loaded model and the file type
    class_names = []

    # load the txt file that contains class names for evaluation
    with open(f'{labels}', 'r') as labelReader:
        for line in labelReader:
            class_names.append(line.strip())

    total = 0
    correct = 0
    total_items = 0
    item_num = 0
    misclassified = []

    actual_label_list = []
    predicted_label_list = []
    prediction_score_list = []

    for class_name_index, className in enumerate(class_names):
        folder_path = os.path.join(dir, className)

        print(f"\n\n📂 Scanning folder: {folder_path}")

        total_items = len(os.listdir(folder_path))
        if total_items == 0:
            print(f"⚠️ {_ANSI.red()}Skipping empty folder: {folder_path}{_ANSI.reset()}")
            continue

        item_num = 0

        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.jpg', '.png', '.jpeg', '.bmp', '.webp')):
                image_path = os.path.join(folder_path, filename)
                
                item_num += 1
                progress = item_num / total_items * 100

                # Preprocess the image
                img = tf.keras.preprocessing.image.load_img(image_path, target_size=input_shape)
                img = tf.keras.preprocessing.image.img_to_array(img)
                img = np.expand_dims(img, axis=0).astype(np.float32)

                # Run inference based on model type
                if model_format == ".tflite":
                    model.set_tensor(model.get_input_details()[0]['index'], img)
                    model.invoke()
                    output = model.get_tensor(model.get_output_details()[0]['index'])[0]
                elif model_format == ".h5":
                    output = model.predict(img)[0]
                elif model_format == ".onnx":
                    input_name = model.get_inputs()[0].name
                    output_name = model.get_outputs()[0].name
                    output = model.run([output_name], {input_name: img})[0][0]

                output = np.array(output)  # Ensure it's a NumPy array

                if len(class_names) == 2:
                    if output.shape[0] == 1:
                        prediction = 1 if output[0] > 0.5 else 0
                    else:
                        prediction = np.argmax(output)
                else:
                    prediction = np.argmax(output)

                isCorrect = (prediction == class_name_index)
                correct += int(isCorrect)
                total += 1

                actual_label_list.append(class_name_index)
                predicted_label_list.append(prediction)
                prediction_score_list.append(output[prediction] if prediction < len(output) else 0)

                if not isCorrect and prediction < len(class_names):
                    misclassified.append(f'{filename} - Predicted: {class_names[prediction]} || Actual: {className} || Filepath: {folder_path}')
            
                print(f'>> Scanning in progress: [{_ANSI.yellow()}{progress:.0f}%{_ANSI.reset()}]', end="\r")

    # Calculate accuracy
    accuracy = correct / total if total > 0 else 0
    print("\n\n=== Evaluation Complete ===")
    print(f"Accuracy: {accuracy * 100:.2f}% ({correct}/{total})")    
    
    if len(misclassified) > 0:
        # Show misclassified data if there is/are any
        print('\n==== Misclassified ====')
        print(f"No. of misclassified: {_ANSI.red()}",len(misclassified), f'{_ANSI.reset()}\n')
        for incorrect in misclassified:
            print(incorrect)
        print('')
    else:
        print(f'{_ANSI.green()}\m=== No Misclassified data ==={_ANSI.reset()}\n')

    # Display classification report
    print("=== Classification Report ===")
    print(classification_report(actual_label_list, predicted_label_list, target_names=[names.replace("_", " ") for names in class_names]))

    _visualizer.Visualize(actual_label_list, predicted_label_list, class_names, prediction_score_list, labels)
    



