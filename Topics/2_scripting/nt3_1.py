from __future__ import print_function
import pandas as pd
import numpy as np
import os
import sys
import gzip
import argparse

from keras import backend as K
from keras.layers import Input, Dense, Dropout, Activation, Conv1D, MaxPooling1D, Flatten
from keras import optimizers
from keras.optimizers import SGD, Adam, RMSprop
from keras.models import Sequential, Model, model_from_json, model_from_yaml
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint, CSVLogger, ReduceLROnPlateau

from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler


url_nt3 = 'ftp://ftp.mcs.anl.gov/pub/candle/public/benchmarks/Pilot1/normal-tumor/'
file_train = url_nt3 + 'nt_train2.csv'
file_test = url_nt3  + 'nt_test2.csv'


EPOCHS = 2
BATCH_SIZE = 20
CLASSES = 2
DROPOUT_RATE = 0.1


def load_data(train_path, test_path):
    import threading
    import queue
    
    
    def load_train(train_path, queue):
        print('looking for ', train_path)
        df_train = (pd.read_csv(train_path,header=None).values).astype('float32')
        print('done loading training data')
        queue.put(df_train)
    
    def load_test(test_path, queue):
        print('looking for ', test_path)
        df_test = (pd.read_csv(test_path,header=None).values).astype('float32')
        print('done loading test data')
        queue.put(df_test)

    q1 = queue.Queue()
    q2 = queue.Queue()
    
    thread1 = threading.Thread(name='load_train', target=load_train, args=(train_path, q1,))
    thread2 = threading.Thread(name='load_test' , target=load_test, args=(test_path, q2,))
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()
    
    df_train = q1.get()
    df_test = q2.get()
    
    print('df_train shape:', df_train.shape)
    print('df_test shape:', df_test.shape)

    seqlen = df_train.shape[1]

    df_y_train = df_train[:,0].astype('int')
    df_y_test = df_test[:,0].astype('int')

    Y_train = np_utils.to_categorical(df_y_train,CLASSES)
    Y_test = np_utils.to_categorical(df_y_test,CLASSES)

    df_x_train = df_train[:, 1:seqlen].astype(np.float32)
    df_x_test = df_test[:, 1:seqlen].astype(np.float32)

    X_train = df_x_train
    X_test = df_x_test

    scaler = MaxAbsScaler()
    mat = np.concatenate((X_train, X_test), axis=0)
    mat = scaler.fit_transform(mat)

    X_train = mat[:X_train.shape[0], :]
    X_test = mat[X_train.shape[0]:, :]

    return X_train, Y_train, X_test, Y_test


X_train, Y_train, X_test, Y_test = load_data(file_train, file_test)
num_params = 60483
num_params = X_train.shape[1]
print('num_params=', num_params)

# this reshaping is critical for the Conv1D to work
X_train = np.expand_dims(X_train, axis=2)
X_test = np.expand_dims(X_test, axis=2)

print('X_train shape:', X_train.shape)
print('X_test shape:', X_test.shape)


# Reference case
model = Sequential()
model.add(Conv1D(filters=128, kernel_size=20, strides=1, padding='valid', input_shape=(num_params, 1)))
model.add(Activation('relu'))
model.add(MaxPooling1D(pool_size=1))
model.add(Conv1D(filters=128, kernel_size=10, strides=1, padding='valid'))
model.add(Activation('relu'))
model.add(MaxPooling1D(pool_size=10))
model.add(Flatten())
model.add(Dense(200))
model.add(Activation('relu'))
model.add(Dropout(DROPOUT_RATE))
model.add(Dense(20))
model.add(Activation('relu'))
model.add(Dropout(DROPOUT_RATE))
model.add(Dense(CLASSES))
model.add(Activation('softmax'))


# Define optimizer
OPTIMIZER='sgd'
LEARNING_RATE = 0.001
DECAY_RATE = 0.

optimizer = optimizers.SGD(lr=LEARNING_RATE, decay=DECAY_RATE)


METRICS='accuracy'
LOSS='categorical_crossentropy'
model.summary()
model.compile(loss=LOSS,
              optimizer=optimizer,
              metrics=[METRICS])


# Set up some variables for output files
MODEL_NAME = 'nt3'
OUTPUT_DIR = 'save'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)



# set up a bunch of callbacks to do work during model training..
# model_name = gParameters['model_name']

# path = '{}/{}.autosave.weights.h5'.format(OUTPUT_DIR, MODEL_NAME)
# checkpointer = ModelCheckpoint(filepath=path, verbose=1, save_weights_only=False, save_best_only=True)    csv_logger = CSVLogger('{}/training.log'.format(output_dir))
# candleRemoteMonitor = CandleRemoteMonitor(params=gParameters)

csv_logger = CSVLogger('{}/training.log'.format(OUTPUT_DIR))


reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=10, verbose=1, mode='auto', epsilon=0.0001, cooldown=0, min_lr=0)
history = model.fit(X_train, Y_train,
                    batch_size=BATCH_SIZE,
                    epochs=EPOCHS,
                    verbose=1,
                    validation_data=(X_test, Y_test),
                    callbacks = [csv_logger, reduce_lr
                                ])

score = model.evaluate(X_test, Y_test, verbose=0)

# serialize model to JSON
model_json = model.to_json()
with open("{}/{}.model.json".format(OUTPUT_DIR, MODEL_NAME), "w") as json_file:
            json_file.write(model_json)
print('Saved model to disk')

# serialize weights to HDF5
model.save_weights("{}/{}.weights.h5".format(OUTPUT_DIR, MODEL_NAME))
print('Saved weights to disk')
