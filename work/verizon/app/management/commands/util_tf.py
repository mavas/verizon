"""
In TF you make wise use of their `features` for which ever way it is that you
want to target your model.

- https://www.tensorflow.org/datasets/api_docs/python/tfds/features#classes

- https://www.tensorflow.org/datasets/features
"""


import datetime

import tensorflow as tf


def load_data():
    (train_images, train_labels), (test_images, test_images) = load_data()
    return (train_images, train_labels), (test_images, test_images)


def create_model():
  return tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='softmax')
  ])


def train_model():
    model = create_model()
    model.compile(optimizer='adam',
		loss='sparse_categorical_crossentropy',
		metrics=['accuracy'])

    log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

    model.fit(x=x_train,
	    y=y_train,
	    epochs=5,
	    validation_data=(x_test, y_test), 
	    callbacks=[tensorboard_callback])

    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    train_log_dir = 'logs/gradient_tape/' + current_time + '/train'
    test_log_dir = 'logs/gradient_tape/' + current_time + '/test'
    train_summary_writer = tf.summary.create_file_writer(train_log_dir)
    test_summary_writer = tf.summary.create_file_writer(test_log_dir)

    # Sets up a timestamped log directory.
    logdir = "logs/train_data/" + datetime.now().strftime("%Y%m%d-%H%M%S")
    # Creates a file writer for the log directory.
    file_writer = tf.summary.create_file_writer(logdir)

    # Using the file writer, log the reshaped image.
    with file_writer.as_default():
        tf.summary.image("Training data", img, step=0)
