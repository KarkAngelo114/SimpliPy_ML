from ._utils import suppressor, _ANSI, ModelType, _visualizer
suppressor.suppress()
import os
import numpy as np
import tensorflow as tf
from PIL import Image
from sklearn.metrics import classification_report



def Image_classifier(dir, labels, model_name, input_shape, enable_visualize = False):
    """

        Paramerters:
            dir: specify the directory of the test sets that contains images that will be use for evaluaation of image classification model

            labels (str): labels will be use as bases for evaluation. The folder names used in training and containing the images are usually used as class namesbe sure that folder names that contains the images for model evaluation matches what is in the label_map.txt. You need to emter the filename of the text file that contains the label names

            model: load the model to be evaluated

            input_shape: specify the input_shape when loading the dataset, and training the model
                    - (ex: if you train the model in 224,224 or 224x224, then you need to input the same image shape)

            enable_visualize (bool): if set to True, it will show visualize the model's performance..
            

    """

    if not dir:
        raise ValueError(f"\n{_ANSI.red()}>> Please specify the directory and ensure that it exists {_ANSI.reset()}")
    if not labels:
        raise ValueError(f"\n{_ANSI.red()}>> Please enter the name of the text file that has the label names.{_ANSI.reset()} ")
    if not model_name:
        raise ValueError(f"\n{_ANSI.red()}>> No Model to be evaluated{_ANSI.reset()}")
    
    
    # get the loaded model and the file type
    model, model_format = ModelType.getModelType(model_name) 

    print("\n=========================================")
    print(f"{_ANSI.blue()}>> Evaluating {_ANSI.yellow()}{model_name}\n{_ANSI.blue()}>> Format: {_ANSI.yellow()}{model_format}{_ANSI.reset()}")

    class_names = []

    # load the txt file that contains class names for evaluation
    with open(f'{labels}', 'r') as labelReader:
        for line in labelReader:
            class_names.append(line.strip())

    total = 0
    correct = 0
    misclassified = []

    actual_label_list = []
    predicted_label_list = []
    prediction_score_list = []

    for class_name_index, className in enumerate(class_names):
        folder_path = os.path.join(dir, className)

        print(f"\n\n📂 Scanning folder: {folder_path}")

        # Filter only supported image files
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.png', '.jpeg', '.bmp', '.webp'))]
        total_items = len(image_files)

        if total_items == 0:
            print(f"⚠️ {_ANSI.red()}Skipping empty folder: {folder_path}{_ANSI.reset()}")
            continue

        item_num = 0

        for filename in image_files:
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
                    prediction_score = output[0] # Probability of the positive class (assuming label 1)
                else:
                    prediction = np.argmax(output)
                    prediction_score = output[1] if 1 < len(output) else output[0] # Probability of the positive class (assuming index 1)
            else:
                prediction = np.argmax(output)
                prediction_score = output[prediction] if prediction < len(output) else 0

            isCorrect = (prediction == class_name_index)
            correct += int(isCorrect)
            total += 1

            actual_label_list.append(class_name_index)
            predicted_label_list.append(prediction)
            prediction_score_list.append(prediction_score)

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
        print('=========================\n')
    else:
        print(f'{_ANSI.green()}\n=== No Misclassified data ==={_ANSI.reset()}\n')

    # Display classification report
    print("\n=========================================")
    print(f"{_ANSI.cyan()}Classification Report:{_ANSI.yellow()}")
    print(classification_report(actual_label_list, predicted_label_list, target_names=[names.replace("_", " ") for names in class_names]), _ANSI.reset())

    if enable_visualize:
        _visualizer.Visualize(actual_label_list, predicted_label_list, class_names, prediction_score_list, labels)


def multi_evaluate(dir, labels, input_shape, models = []):
    try:
        from tabulate import tabulate 

        """
        Evaluate all model's performance and will display in a table format showing their model name, format, accuracy, and number of misclassified data
        Note that when doing muiti-evaluation, be sure that the models are trained the same (ex: all must be trained to binary classification or multi-class classification or regression)
        to avoid errors.

        Parameters:
            
            dir (str): The directory of test sets to evaluate the models.

            labels (str): The text file that stores class names used in loading the datasets

            input_shape (tuple): Specfiy the input shape used when training the model.

            models (list): Iist all trained models regardless of their formats.
        """

        if not dir:
            raise ValueError(f"\n{_ANSI.red()}>> Please specify the directory and ensure that it exists {_ANSI.reset()}")
        
        if len(models) == 0:
            raise ValueError(f"\n{_ANSI.red()}>> No models to evaluate {_ANSI.reset()}")
        
        if not labels:
            raise ValueError(f"\n{_ANSI.red()}>> Please enter the labels will be used {_ANSI.reset()}")
        
    

        class_names = []
        model_formats = []
        models_accuracy = []
        model_num_misclassified = []

        # load the txt file that contains class names for evaluation
        with open(f'{labels}', 'r') as labelReader:
            for line in labelReader:
                class_names.append(line.strip())

        total = 0
        correct = 0
        misclassified_count = 0

        for trained_model in models:

            model, model_format = ModelType.getModelType(trained_model)
            model_formats.append(model_format)

            for class_name_index, className in enumerate(class_names):
                folder_path = os.path.join(dir, className)

                # Filter only supported image files
                image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.png', '.jpeg', '.bmp', '.webp'))]
                total_items = len(image_files)

                if total_items == 0:
                    continue

                for filename in image_files:
                    image_path = os.path.join(folder_path, filename)

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


                    if not isCorrect and prediction < len(class_names):
                        misclassified_count += 1

            accuracy = correct/total if total > 0 else 0
            models_accuracy.append(f'{accuracy * 100:.2f}')
            model_num_misclassified.append(misclassified_count)
                    

        print(f"\n{_ANSI.reset()}=========================================")
        print(f"{_ANSI.yellow()}>> Evaluating models:{_ANSI.reset()}\n")
        
        print("Results:")
        # Prepare data for the table
        table_data = []
        for i, trained_model in enumerate(models):
            table_data.append([
                trained_model,
                model_formats[i],
                models_accuracy[i],
                model_num_misclassified[i]
            ])

        # Define table headers
        headers = ["Model", "Format", "Accuracy (%)", "No. of Misclassified"]

        # Print the table using tabulate
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    except:
        print(f'{_ANSI.red()}\n[!] Unable to tabulate data, please install "tabulate" library first using pip or using the SimpliPy_ML own package installer function.{_ANSI.reset()}\n')
    