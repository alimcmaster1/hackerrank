import pandas as pd
import tensorflow as tf
import logging as logger
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

#Estimate number of distinct words in the dataset
NUM_FEATURES = 50000

#Max sentence length words

MAX_LEN = 200

logPath = "./tb_logs"

def get_data(filename):
    df = pd.read_csv(filename)
    logger.info("======Loaded {} Data======".format(filename))
    logger.info(df.head(5))
    return df

def simple_neural_network():

    df = get_data("train.csv")
    comment_data_train = df["comment_text"]
    tokenized_train_data = data_Tokenize(comment_data_train)
    padded_tokenized_train_data = pad_sequences(tokenized_train_data, maxlen=MAX_LEN)
    toxicity_data_train = df[["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]].as_matrix()

    df = get_data("test.csv")
    comment_data_test = df["comment_text"]
    tokenized_test_data = data_Tokenize(comment_data_test)
    padded_tokenized_test_data = pad_sequences(tokenized_train_data, maxlen=MAX_LEN)
    ##toxicity_data_test = df[["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]].as_matrix()

    with tf.name_scope("Input_Data"):
    #6 Element Vector containing the probability of a type of toxicity
        y_ = tf.placeholder(tf.float32, shape=[None, 6],   name="predicted_toxicity_probs")
        x = tf.placeholder(tf.float32,  shape=[None, 200], name="comment_data" )

    Weights = tf.Variable(tf.zeros([200,6]))
    Bias = tf.Variable(tf.zeros([6]))

    #Define our model
    y = tf.nn.softmax(tf.matmul(x,Weights)+ Bias )

    #loss is the cross entropy
    cross_entropy = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=y_, logits=y))

    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

    #Initialise all the variables
    init = tf.global_variables_initializer()

    #Create an Interactive Session
    sess = tf.Session()
    sess.run(init)

    sess.run(train_step, feed_dict={x:padded_tokenized_train_data, y_:toxicity_data_train})

    #Evaluate how well the model did. Do this by comparing the sum of the 0,1 for comment types
    correct_prediction = tf.equal(tf.round(y), tf.round(y_))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    test_accuracy = sess.run(accuracy, feed_dict={x:padded_tokenized_train_data, y_: toxicity_data_train})

    print("Test accuracy: {0}".format(test_accuracy * 100))


    ## Now the model is trained run for test data
    trained_results = sess.run(y, feed_dict={x: padded_tokenized_test_data,
                                             Weights: sess.run(Weights),
                                             Bias: sess.run(Bias)})

    tbWriter = tf.summary.FileWriter(logPath, sess.graph)
    sess.close()

def data_Tokenize(dataset):
    ##number of distinct words in data set
    features = NUM_FEATURES
    tokenizer = Tokenizer(num_words=features)
    tokenizer.fit_on_texts(dataset)
    tokenized_set = tokenizer.texts_to_sequences(dataset)
    return tokenized_set

def main():
    simple_neural_network()


if __name__ == "__main__":
    main()