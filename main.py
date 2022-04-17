import keras
import tensorflow as tf

def run(temp, moisture):

    sample = {
        "temp": temp,
        "moisture": moisture,
    }
    # call saved model
    old_model = keras.models.load_model('my_model')
    input_dic_test = {name: tf.convert_to_tensor([value]) for name, value in sample.items()}
    predictions_test = old_model.predict(input_dic_test,batch_size=1)

    # real value
    print("Real predictions: "+str(predictions_test))

    # round the value
    print("Round: "+str(round(predictions_test[0][0])))

if __name__ == "__main__":
    run()

