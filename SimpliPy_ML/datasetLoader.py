from ._utils import suppressor, _ANSI
suppressor.suppress()
import tensorflow as tf
import os

"""
    This module contains all the functionalities to import datasets for training a model
    
    Functions includes:
        - load_Image_datasets(Param1, Param2, Param3, . . . ) - this is used when dealing with datasets containing images in a folder. Sub folder names will be used as class names

"""



def load_Image_datasets(dir, autoResize=True, input_size=(0,0), mode='', split_size=0.0, batch_size = 0):
    """
    Loads image datasets from a specified directory for training and validation.

    Parameters:
        dir (str): Path to the dataset directory.
        input_size (tuple): Target size for resizing images (ignored if autoResize=True).
        mode (str): Label mode ('int', 'categorical', 'binary').
        split_size (float): Fraction of data to reserve for validation and training.
        batch_size (int): Number of samples per batch.

    Returns:
        tuple: Training and validation datasets
    """
    # Validate directory
    if not os.path.exists(dir):
        raise FileNotFoundError(f"\n{_ANSI.red()}>> Directory '{dir}' does not exist.{_ANSI.reset()}")

    # Set image size based on autoResize
    if autoResize:
        image_size = (224, 224)
    else:
        if input_size == (0, 0):
            raise ValueError(f"\n{_ANSI.red()}>> input_size must be specified if autoResize is False.{_ANSI.reset()}")
        image_size = input_size

    if mode == '':
        raise ValueError(f"\n{_ANSI.red()}>> Mode is not specified.{_ANSI.reset()}")
    
    if split_size == 0.0:
        raise ValueError(f"\n{_ANSI.red()}>> Split size must not be 0.0 and must be specified.{_ANSI.reset()}")
    
    if batch_size == 0 or batch_size <= 10:
        raise ValueError(f"\n{_ANSI.red()}>> batch size must not be 0 or less than 10.{_ANSI.reset()}")
    
    # Load training dataset
    train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        directory=dir,
        validation_split=split_size,
        subset="training",
        seed=123,
        image_size=image_size,
        batch_size=batch_size,
        label_mode=mode
    )

    # Load validation dataset
    validation_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        directory=dir,
        validation_split=split_size,
        subset="validation",
        seed=123,
        image_size=image_size,
        batch_size=batch_size,
        label_mode=mode
    )

    # Print class names
    print("\n>> Found labels:")
    print(train_dataset.class_names)

    # Save class names to a file in the same directory as main.py
    label_map_path = os.path.join(os.getcwd(), "label_map.txt")
    print(f"\n>> Saving class names to {_ANSI.green()}{label_map_path}{_ANSI.reset()}")
    with open(label_map_path, "w") as f:
        for class_name in train_dataset.class_names:
            f.write(f"{class_name}\n")
    print(f">> Successfully saved {_ANSI.green()}label_map.txt{_ANSI.reset()}\n")

    return train_dataset, validation_dataset