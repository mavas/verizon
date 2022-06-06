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

## Docker demonstration

```
git clone https://github.com/mavas/verizon
cd verizon
docker build -t verizon .
```
