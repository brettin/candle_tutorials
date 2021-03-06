import pandas as pd
import numpy as np
import os
import sys
import gzip
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import keras as ke
from keras.layers import Input, Dense, Dropout, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.models import Sequential, Model, model_from_json, model_from_yaml
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint, CSVLogger, ReduceLROnPlateau
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler

EPOCH = 4
BATCH = 32
nb_classes = 2
PL     = 6213   # 38 + 60483
PS     = 6212   # 60483
DR     = 0.2    # Dropout rate

import tensorflow as tf
from keras import backend as K

# set theta = True if running on Theta for threading option
theta = False
if theta == True:
	session_conf = tf.ConfigProto(inter_op_parallelism_threads=int(os.environ['NUM_INTER_THREADS']),
    		intra_op_parallelism_threads=int(os.environ['NUM_INTRA_THREADS']))
	sess = tf.Session(graph=tf.get_default_graph(), config=session_conf)
	K.set_session(sess)

def load_data():
    train_path = 'rip.it.train.csv'
    test_path = 'rip.it.test.csv'
    df_train = (pd.read_csv(train_path,header=None).values).astype('float32')
    df_test = (pd.read_csv(test_path,header=None).values).astype('float32')

    print('df_train shape:', df_train.shape)
    print('df_test shape:', df_test.shape)

    df_y_train = df_train[:,0].astype('int')
    df_y_test = df_test[:,0].astype('int')
    Y_train = np_utils.to_categorical(df_y_train,nb_classes)
    train_classes = np.argmax(Y_train, axis=1)

    np.savetxt("train_classes.csv", train_classes, delimiter=",", fmt="%d")

    Y_test = np_utils.to_categorical(df_y_test,nb_classes)
    test_classes = np.argmax(Y_test, axis=1)

    np.savetxt("test_classes.csv", test_classes, delimiter=",", fmt="%d")

    df_x_train = df_train[:, 1:PL].astype(np.float32)
    df_x_test = df_test[:, 1:PL].astype(np.float32)
    X_train = df_x_train
    X_test = df_x_test

    scaler = MaxAbsScaler()
    mat = np.concatenate((X_train, X_test), axis=0)
    mat = scaler.fit_transform(mat)
    X_train = mat[:X_train.shape[0], :]
    X_test = mat[X_train.shape[0]:, :]
        
    return X_train, Y_train, X_test, Y_test

X_train, Y_train, X_test, Y_test = load_data()

print('X_train shape:', X_train.shape)
print('X_test shape:', X_test.shape)

print('Y_train shape:', Y_train.shape)
print('Y_test shape:', Y_test.shape)


inputs = Input(shape=(PS,))

x = Dense(2000, activation='relu')(inputs)
x = Dense(1000, activation='relu')(x)
x = Dropout(DR)(x)
y = Dense(1000, activation='relu')(x)
z = ke.layers.add([x,y])
z = Dropout(DR)(z)
y = Dense(1000, activation='relu')(z)
x = ke.layers.add([z,y])
x = Dropout(DR)(x)
y = Dense(1000, activation='relu')(x)
z = ke.layers.add([x,y])
z = Dropout(DR)(z)
y = Dense(1000, activation='relu')(z)
x = ke.layers.add([z,y])
x = Dropout(DR)(x)
x = Dense(500, activation='relu')(x)
x = Dropout(DR)(x)
x = Dense(250, activation='relu')(x)
x = Dropout(DR)(x)
x = Dense(125, activation='relu')(x)
x = Dropout(DR)(x)
x = Dense(62, activation='relu')(x)
x = Dropout(DR)(x)
x = Dense(30, activation='relu')(x)
x = Dropout(DR)(x)

outputs = Dense(2, activation='softmax')(x)
model = Model(inputs=inputs, outputs=outputs)
model.summary()
model.compile(loss='categorical_crossentropy',
              optimizer=SGD(lr=0.001, momentum=0.9),
              metrics=['accuracy'])

# set up a bunch of callbacks to do work during model training.
checkpointer = ModelCheckpoint(filepath='t29res.autosave.model.h5', verbose=0, save_weights_only=False, save_best_only=True)
csv_logger = CSVLogger('t29res.training.log')
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.4, patience=10, verbose=1, mode='auto', epsilon=0.0001, cooldown=3, min_lr=0.000000001)

history = model.fit(X_train, Y_train,
                    batch_size=BATCH,
                    epochs=EPOCH,
                    verbose=1,
                    validation_data=(X_test, Y_test),
                    callbacks = [checkpointer, csv_logger, reduce_lr])

score = model.evaluate(X_test, Y_test, verbose=0)

# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model Accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig('t29res.accuracy.png', bbox_inches='tight')
plt.savefig('t29res.accuracy.pdf', bbox_inches='tight')
plt.close()

# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig('t29res.loss.png', bbox_inches='tight')
plt.savefig('t29res.loss.pdf', bbox_inches='tight')
print('Test val_loss:', score[0])
print('Test accuracy:', score[1])

# serialize model to JSON                                            
model_json = model.to_json()
with open("t29res.model.json", "w") as json_file:
        json_file.write(model_json)

# serialize model to YAML
model_yaml = model.to_yaml()
with open("t29res.model.yaml", "w") as yaml_file:
        yaml_file.write(model_yaml)

# serialize weights to HDF5
model.save_weights("t29res.model.h5")
print("Saved model to disk")

# load json and create model
json_file = open('t29res.model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model_json = model_from_json(loaded_model_json)

# load yaml and create model                                                                      
yaml_file = open('t29res.model.yaml', 'r')
loaded_model_yaml = yaml_file.read()
yaml_file.close()
loaded_model_yaml = model_from_yaml(loaded_model_yaml)

# load weights into new model                                            
loaded_model_json.load_weights("t29res.model.h5")
print("Loaded json model from disk")

# evaluate json loaded model on test data
loaded_model_json.compile(loss='binary_crossentropy', optimizer='SGD', metrics=['accuracy'])
score_json = loaded_model_json.evaluate(X_test, Y_test, verbose=0)
print('json Validation loss:', score_json[0])
print('json Validation accuracy:', score_json[1])
print("json %s: %.2f%%" % (loaded_model_json.metrics_names[1], score_json[1]*100))

# load weights into new model
loaded_model_yaml.load_weights("t29res.model.h5")
print("Loaded yaml model from disk")

# evaluate loaded model on test data
loaded_model_yaml.compile(loss='binary_crossentropy', optimizer='SGD', metrics=['accuracy'])
score_yaml = loaded_model_yaml.evaluate(X_test, Y_test, verbose=0)
print('yaml Validation loss:', score_yaml[0])
print('yaml Validation accuracy:', score_yaml[1])
print("yaml %s: %.2f%%" % (loaded_model_yaml.metrics_names[1], score_yaml[1]*100))

# predict using loaded yaml model on test and training data
predict_yaml_train = loaded_model_yaml.predict(X_train)
predict_yaml_test = loaded_model_yaml.predict(X_test)
print('Yaml_train_shape:', predict_yaml_train.shape)
print('Yaml_test_shape:', predict_yaml_test.shape)

predict_yaml_train_classes = np.argmax(predict_yaml_train, axis=1)
predict_yaml_test_classes = np.argmax(predict_yaml_test, axis=1)

np.savetxt("predict_yaml_train.csv", predict_yaml_train, delimiter=",", fmt="%.3f")
np.savetxt("predict_yaml_test.csv", predict_yaml_test, delimiter=",", fmt="%.3f")

np.savetxt("predict_yaml_train_classes.csv", predict_yaml_train_classes, delimiter=",",fmt="%d")
np.savetxt("predict_yaml_test_classes.csv", predict_yaml_test_classes, delimiter=",",fmt="%d")
