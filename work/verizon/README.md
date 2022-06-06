# A Django-based administration interface for Super Smash Bros. video and image data

This is all for machine learning purposes.  The most important thing is a Django management command that outputs `tfrecord` files.

The directory parent to this one was initially started by the command `django-admin startproject verizon`, with Django version 4.0.5.

## Models

In TF you make wise use of their `features` for which ever way it is that you want to target your model.

https://www.tensorflow.org/datasets/api_docs/python/tfds/features#classes
https://www.tensorflow.org/datasets/features

- Binary classification, whether or not gameplay footage is present (menu,
  stages, etc.)

- Multiclassification stages: 26 stages

- Multiclassification stages and characters

- Multiclassification character moves

## Docker-based demonstration

The primary user interface is the web browser at http://localhost:8000/.  Using it, you can import videos into the database, perform object detection on videos and images, etc..

There are 4 containers: a PostgreSQL database, a Django web server, a TensorBoard server, and an Ubuntu operating system.

```
git clone https://github.com/mavas/verizon
docker build -f verizon/work/verizon/Dockerfile -t verizon .
```
