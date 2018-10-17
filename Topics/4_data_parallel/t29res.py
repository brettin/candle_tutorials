import pandas as pd
import numpy as np
import os
import sys
import gzip
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
import keras
import keras as ke
from keras.layers import Input, Dense, Dropout, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.models import Sequential, Model, model_from_json, model_from_yaml
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint, CSVLogger, ReduceLROnPlateau
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler
import math
import tensorflow as tf
import horovod.keras as hvd
from keras import backend as K
# Horovod: initialize Horovod.
hvd.init()

# Horovod: pin GPU to be used to process local rank (one GPU per process)
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.visible_device_list = str(hvd.local_rank())
K.set_session(tf.Session(config=config))

# Horovod: adjust number of epochs based on number of GPUs.
epochs = int(math.ceil(12.0 / hvd.size()))


file_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(file_path, '..', '..', 'common'))
sys.path.append(lib_path)

EPOCH = epochs
BATCH = 32
nb_classes = 2
PL     = 6213   # 38 + 60483
PS     = 6212   # 60483
DR     = 0.2    # Dropout rate

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


# Horovod: adjust learning rate based on number of ranks.
opt = keras.optimizers.Adadelta(1.0 * hvd.size())

# Horovod: add Horovod Distributed Optimizer.
opt = hvd.DistributedOptimizer(opt)

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=opt,
              metrics=['accuracy'])

callbacks = [
    # Horovod: broadcast initial variable states from rank 0 to all other processes.
    # This is necessary to ensure consistent initialization of all workers when
    # training is started with random weights or restored from a checkpoint.
    hvd.callbacks.BroadcastGlobalVariablesCallback(0),
    csv_logger
]


# Horovod: save checkpoints only on worker 0 to prevent other workers from corrupting them.
if hvd.rank() == 0:
    callbacks.append(keras.callbacks.ModelCheckpoint('./checkpoint-{epoch}.h5'))

history = model.fit(X_train, Y_train,
                    batch_size=BATCH,
                    epochs=EPOCH,
                    verbose=1,
                    validation_data=(X_test, Y_test))
                    #callbacks = [reduce_lr])

if hvd.rank() == 0:
    score = model.evaluate(X_test, Y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

