## Models

In TF you make wise use of their `features` for whatever way you want to target your model.

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
