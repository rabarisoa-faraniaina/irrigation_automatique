import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow import keras 
from keras import layers
from keras.layers import Normalization

dataframe = pd.read_csv("cotton.csv")
dataframe.shape

dataframe.head()

val_dataframe = dataframe.sample(frac=0.2, random_state=1337)
train_dataframe = dataframe.drop(val_dataframe.index)
print(
     "Using %d samples for training and %d for validation"
     % (len(train_dataframe), len(val_dataframe))
    )

def dataframe_to_dataset(dataframe):
    dataframe = dataframe.copy()
    labels = dataframe.pop("pump")
    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
    ds = ds.shuffle(buffer_size=len(dataframe))
    return ds

train_ds = dataframe_to_dataset(train_dataframe)
val_ds = dataframe_to_dataset(val_dataframe)

for x, y in train_ds.take(1):
    print("Input:",x)
    print("Target:", y)

train_ds = train_ds.batch(32)
val_ds = val_ds.batch(32)

def encode_numerical_feature(feature, name, dataset):
    # Create a Normalization layer for our feature
    normalizer = Normalization()

    # Prepare a Dataset that only yields our feature
    feature_ds = dataset.map(lambda x, y: x[name])
    feature_ds = feature_ds.map(lambda x: tf.expand_dims(x, -1))

    # Learn the statistics of the data
    normalizer.adapt(feature_ds)

    # Normalize the input feature
    encoded_feature = normalizer(feature)
    return encoded_feature

# Build the model

# Numerical features
humidity = keras.Input(shape=(1,), name="temp")
moisture = keras.Input(shape=(1,), name="moisture")
all_inputs = [
    humidity,
    moisture,
]
hum_encoded = encode_numerical_feature(humidity, "temp", train_ds)
moi_encoded = encode_numerical_feature(moisture, "moisture", train_ds)

all_features = layers.concatenate(
    [
        hum_encoded,
        moi_encoded,
    ]
)

x = layers.Dense(32, activation="relu")(all_features)
x = layers.Dropout(0.5)(x)

output = layers.Dense(1, activation="sigmoid")(x)
model = keras.Model(all_inputs, output)
model.compile("adam","binary_crossentropy", metrics=["accuracy"])

# rankdir=LR is to make the graph horizontal
# cette partie ne marche pas
"""tf.keras.utils.model_to_dot(
    model,
    show_shapes=False,
    show_dtype=False,
    show_layer_names=True,
    rankdir="TB",
    expand_nested=False,
    dpi=96,
    subgraph=False,
    layer_range=None,
    show_layer_activations=False,
)"""
"""tf.keras.utils.plot_model(
    model,
    to_file='model.png',
    show_shapes=False,
    show_dtype=False,
    show_layer_names=True,
    rankdir='TB',
    expand_nested=False,
    dpi=96,
    layer_range=None,
    show_layer_activations=False
)"""

model.fit(train_ds,epochs=50,validation_data = val_ds)
_,accuracy = model.evaluate(val_ds,verbose=1)

# show model accuracy
print("accuracy: "+str(accuracy))



# test the model with a sample
sample = {
    "temp": 981,
    "moisture": 37,
}

input_dic = {name: tf.convert_to_tensor([value]) for name, value in sample.items()}
predictions = model.predict(input_dic,batch_size=1)

# show value of pump prediction
print(predictions)

# save model
model.save('my_model')

