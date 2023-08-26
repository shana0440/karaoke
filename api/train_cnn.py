import json
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow.keras as keras
import matplotlib.pyplot as plt
import config

def load_data(dataset_path):
   with open(dataset_path, "r") as fp:
    data = json.load(fp)

    inputs = np.array(data["mfcc"])
    targets = np.array(data["labels"])

    return inputs, targets


def prepare_datasets(test_size, validation_size):
    # load data
    inputs, targets = load_data(config.JSON_PATH)

    # create train/test split
    x_train, x_test, y_train, y_test = train_test_split(inputs, targets, test_size=test_size)

    # create train/validation split
    x_train, x_validation, y_train, y_validation = train_test_split(x_train, y_train, test_size=validation_size)

    x_train = x_train[..., np.newaxis]
    x_validation = x_validation[..., np.newaxis]
    x_test = x_test[..., np.newaxis]
    return x_train, x_validation, x_test, y_train, y_validation, y_test


def build_model(input_shape):
    # create model
    model = keras.Sequential()

    # 1st conv layer, 32 filter(kernel) that size is 3x3
    model.add(keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(keras.layers.MaxPool2D((3, 3), strides=(2, 2), padding='same'))
    model.add(keras.layers.BatchNormalization())

    # 2nd conv layer
    model.add(keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(keras.layers.MaxPool2D((3, 3), strides=(2, 2), padding='same'))
    model.add(keras.layers.BatchNormalization())

    # 3rd conv layer
    model.add(keras.layers.Conv2D(32, (2, 2), activation='relu', input_shape=input_shape))
    model.add(keras.layers.MaxPool2D((2, 2), strides=(2, 2), padding='same'))
    model.add(keras.layers.BatchNormalization())

    # flatten the output and feed it into dense layer
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(64, activation='relu'))
    model.add(keras.layers.Dropout(0.5))

    # output layer, 2 neurons to represent is karaoke or zatsudan
    model.add(keras.layers.Dense(2, activation='softmax'))

    return model


def plot_history(history):
    fig, axs = plt.subplots(2)

    # create accuracy subplot
    axs[0].plot(history.history["accuracy"], label="train accurancy")
    axs[0].plot(history.history["val_accuracy"], label="test accurancy")
    axs[0].set_ylabel("Accurancy")
    axs[0].legend(loc="lower right")
    axs[0].set_title("Accuracy eval")

    # create error subplot
    axs[1].plot(history.history["loss"], label="train error")
    axs[1].plot(history.history["val_loss"], label="test error")
    axs[1].set_ylabel("Error")
    axs[1].set_xlabel("Epoch")
    axs[1].legend(loc="upper right")
    axs[1].set_title("Error eval")

    plt.show()


if __name__ == "__main__":
    # create train, validation and test sets
    x_train, x_validation, x_test, y_train, y_validation, y_test = prepare_datasets(0.1, 0.2)

    # build the CNN net
    input_shape = (x_train.shape[1], x_train.shape[2], x_train.shape[3])
    model = build_model(input_shape)

    # compile the network
    optimizer = keras.optimizers.Adam(learning_rate=0.0001)
    model.compile(optimizer=optimizer, loss="sparse_categorical_crossentropy", metrics=["accuracy"])

    model.summary()

    # train the CNN
    history = model.fit(x_train, y_train, validation_data=(x_validation, y_validation), epochs=50, batch_size=32)

    # evaluate the CNN on the test set
    test_error, test_accuracy = model.evaluate(x_test, y_test, verbose=1)
    print("Accuracy on test set is: {}".format(test_accuracy))

    # save model
    model.save(config.MODEL_PATH)
    
    # plot accuracy and error over the epochs
    plot_history(history)