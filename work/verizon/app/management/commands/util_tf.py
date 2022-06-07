import datetime

import tensorflow as tf


def load_data():
  (x_train, y_train), (x_test, y_test) = load_data()
  return (x_train, y_train), (x_test, y_test)


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
