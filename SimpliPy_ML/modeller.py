from ._utils import suppressor, _ANSI
suppressor.suppress()
import tensorflow as tf
from tensorflow.keras.optimizers import Adam, SGD, RMSprop, Adagrad, Adadelta, Adamax, Nadam
from tensorflow.keras import layers
import os


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def build_CNN_model(train_set, val_set, allow_augmentation=False, input_shape=(224, 224, 3), num_Conv_layers = 3, num_Dense_layers = 1, output_neuron=0, activation_function='', output_activation=''):
    """
    Builds a Convolutional Neural Network (CNN) model for image classification.

    Parameters:
        train_set (tf.data.Dataset): The training dataset.

        val_set (tf.data.Dataset): The validation dataset.

        allow_augmentation: once set to True, data augmentation will be trigger. The purpose is to train the model from diverse data points and introduce
            diversity. This make the model robust when introduce to new and unseen data
        
        input_shape (tuple): Shape of the input images (e.g., (224, 224, 3)).
            - 224x224 pixels with 3 channels = RGB color images.
            - Match this with the size passed during dataset loading.
        
        num_Conv_layers (int): Number of Convolutional layers before connecting to dense layers
            - if not set, the model architecture will have only 3 Convolutional layers by default
        
        num_Dense_layers (int): Number of Dense layers that connects Convolutional layers to output layer
            - if not set, the model architecture will have only 1 Dense layer by default
        
        output_neuron (int): Number of output neurons.
            - For binary classification: set to 1
            - For multiclass classification: set to the number of target classes
        
        activation_function (str): Activation function for the hidden layers.
            - Options: 'relu', 'sigmoid', 'tanh'
        
        output_activation (str): Activation function for the output layer.
            - For binary: usually 'sigmoid'
            - For multiclass: usually 'softmax'

        Returns:
            A compiled Keras CNN model ready for training.
    """
    if not train_set:
        raise ValueError(f"\n{_ANSI.red()}>> No training set. ")
    if not val_set:
        raise ValueError(f"\n{_ANSI.red()}>> No Validation set. {_ANSI.reset()}")
    if input_shape == (0, 0, 0):
        raise ValueError(f"\n{_ANSI.red()}>> Please specify the input size {_ANSI.reset()}")
    if num_Conv_layers == 0:
        raise ValueError(f"\n{_ANSI.red()}>> Convolutional layers must not be 0 {_ANSI.reset()}")
    if num_Dense_layers == 0:
        raise ValueError(f"\n{_ANSI.red()}>> Dense layers must not be 0")
    if output_neuron == 0:
        raise ValueError(f"\n{_ANSI.red()}>> Output Neuron cannot be empty or 0 {_ANSI.reset()}")
    if activation_function == "":
        raise ValueError(f"\n{_ANSI.red()}>> Enter activation function that will be use across the hidden layers. {_ANSI.reset()}")
    if output_activation == '':
        raise ValueError(f"\n{_ANSI.red()}>> Enter activation function that will be use in the output neuron.{_ANSI.reset()}")

    # Prefetching for performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_set.prefetch(buffer_size=AUTOTUNE)
    val_ds = val_set.prefetch(buffer_size=AUTOTUNE)

    # Data Augmentation layer
    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
    ])

    model_layers = [
        layers.Rescaling(1./255, input_shape=input_shape),
    ]

    if allow_augmentation:
        model_layers.append(data_augmentation)

    # Convolutional layers
    filters = 32
    for _ in range(num_Conv_layers):
        model_layers.append(layers.Conv2D(filters, (3, 3), activation=activation_function))
        model_layers.append(layers.MaxPooling2D())
        filters *= 2

    # Flatten before any dense layers
    model_layers.append(layers.Flatten())

    # Hidden dense layers (same size)
    for _ in range(num_Dense_layers):
        model_layers.append(layers.Dense(128, activation=activation_function))

    # Funnel-Shape layers that connects to the layers having 128 neurons
    model_layers.extend([
        layers.Dense(64, activation=activation_function),
        layers.Dense(32, activation=activation_function),
        layers.Dense(16, activation=activation_function),
    ])

    # Output layer
    model_layers.append(layers.Dense(output_neuron, activation=output_activation))

    model = tf.keras.Sequential(model_layers)

    print(f"{_ANSI.yellow()}\n================= Preparing your model ====================={_ANSI.reset()}")
    print("Model's Architecture: ")
    print('Input Shape: ', input_shape)
    print("Number of Convolutional layers: ",num_Conv_layers)
    print('Number of Dense layers: ',num_Dense_layers)
    print("Activation functions on Convolutional layers: "+activation_function)
    print("Activation function on output layer: "+output_activation)

    return model, train_ds, val_ds # returns the model and other parameters ready for training

def train_CNN_model(model, train_data, val_data, optimizer, loss_function, learning_rate = None, metrics = [], epoch = 0):
    """
    Parameters:
        train_ds: pass the train_ds returned from the build_CNN_model() function to this parameter

        val_ds: pass the val_ds returned from the build_CNN_model() function to this parameter

        epoch: Determines the epoch where the model will iterate through the entire training set epoch strictly should not below 10

        optimizer: pass the optimizer parameter.
            optimizers:
                - adam
                - nadam
                - sgd
                - rmsprop
                - adagrad
        
        loss_function: pass the loss parameter
            loss
            - binary_crossentropy
            - categorical_crossentropy
            - sparse_categorical_crossentropy
            - 'mse', 'mae' <- for regression tasks only

        learning_rate: specify the learning rate for training the model. 
            Be careful of tweaking the learning rate as it will have an affect in 
            the training process and affect the performance of the model.

        metrics: pass the metrics use for validating the accuracy of the model
            metrics
            - 'accuracy'
            - 'precision', 'recall', 'AUC'
            - 'mse', 'mae' <- for regression tasks only
    """
    if optimizer == "":
        raise ValueError(F"\n{_ANSI.red()}>> Specify the optimizer (ex: adam, nadam, sgd, rmsprop, adagrad, adadelta){_ANSI.reset()}")
    if loss_function == "":
        raise ValueError(F"\n{_ANSI.red()}>> Specify the loss function (ex: binary_crossentropy, categorical_crossentropy, sparse_categorical_crossentropy, ['mse', 'mae']){_ANSI.reset()}")
    if len(metrics) == 0:
        raise ValueError(F"\n{_ANSI.red()}>> Specify the Metrics (ex: ['accuracy'], ['precision', 'recall', 'AUC'], ['mse', 'mae']){_ANSI.reset()}")
    if epoch == 0 or epoch < 2:
        raise ValueError(F"\n{_ANSI.red()}>> Epoch must not below 10 or 0 at all{_ANSI.reset()}")
    
    if isinstance(optimizer, str):
        optimizer = optimizer.lower()
        if learning_rate:
            if optimizer == "adam":
                optimizer = Adam(learning_rate=learning_rate)
            elif optimizer == "nadam":
                optimizer = Nadam(learning_rate=learning_rate)
            elif optimizer == "adamax":
                optimizer = Adamax(learning_rate=learning_rate)
            elif optimizer == "sgd":
                optimizer = SGD(learning_rate=learning_rate)
            elif optimizer == "rmsprop":
                optimizer = RMSprop(learning_rate=learning_rate)
            elif optimizer == "adagrad":
                optimizer = Adagrad(learning_rate=learning_rate)
            elif optimizer == "adadelta":
                optimizer = Adadelta(learning_rate=learning_rate)
            else:
                raise ValueError(f"\n{_ANSI.red()}>> Unknown optimizer: {optimizer}")
        else:
            # Use default learning rate
            if optimizer == "adam":
                optimizer = Adam()
            elif optimizer == "nadam":
                optimizer = Nadam()
            elif optimizer == "adamax":
                optimizer = Adamax()
            elif optimizer == "sgd":
                optimizer = SGD()
            elif optimizer == "rmsprop":
                optimizer = RMSprop()
            elif optimizer == "adagrad":
                optimizer = Adagrad()
            elif optimizer == "adadelta":
                optimizer = Adadelta()
            else:
                raise ValueError(f"\n>> Unknown optimizer: {optimizer}")

    print(f"\n{_ANSI.green()}============== Your model is now training 😍 =============={_ANSI.reset()}\n")
    model.compile(
        optimizer = optimizer,
        loss = loss_function,
        metrics = metrics
    )

    history = model.fit(
        train_data,
        validation_data = val_data, 
        epochs = epoch,
    )
    return  model, history
