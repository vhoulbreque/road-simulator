import keras
from keras import callbacks
from keras.layers import Input, Convolution2D, MaxPooling2D, Activation
from keras.layers import Dropout, Flatten, Dense, BatchNormalization
from keras.models import Model
from keras.optimizers import Adam

import sys
sys.path.insert(0, '../src/')

from models.utils import get_datasets


paths = ['sample_simple', 'sample_dashed', 'my_dataset']
n_images = 100 * 1000  # number of images
model_path = 'my_autopilot.hdf5'

# Get train, test and val sets
train_X, train_Y, val_X, val_Y, test_X, test_Y = get_datasets(paths, n_images=n_images)

print('train_X[0]: ', train_X[0])
print('train_Y[0]: ', train_Y[0])

# Create the model

dropout_value = 0.1
input_shape = (70, 250, 3)

img_in = Input(shape=input_shape, name='img_in')
x = img_in

x = Convolution2D(1, 3, 3, activation='relu', border_mode='same')(x)
x = MaxPooling2D(pool_size=(2, 2), strides=(2,2))(x)
x = Dropout(dropout_value)(x)
x = BatchNormalization()(x)

x = Convolution2D(2, 3, 3, activation='relu', border_mode='same')(x)
x = MaxPooling2D(pool_size=(2, 2), strides=(2,2))(x)
x = Dropout(dropout_value)(x)
x = BatchNormalization()(x)

x = Convolution2D(2, 3, 3, activation='relu', border_mode='same')(x)
x = MaxPooling2D(pool_size=(2, 2), strides=(2,2))(x)
x = Dropout(dropout_value)(x)
x = BatchNormalization()(x)

x = Convolution2D(4, 3, 3, activation='relu', border_mode='same')(x)
x = MaxPooling2D(pool_size=(2, 2), strides=(2,2))(x)
x = Dropout(dropout_value)(x)
x = BatchNormalization()(x)

flat = Flatten()(x)

x = Dense(20)(flat)
x = Activation('relu')(x)

x = Dense(5)(x)
angle_out = Activation('softmax')(x)

adam = Adam()
model = Model(input=[img_in], output=[angle_out])
model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=['accuracy'])

model.summary()

#Save the model after each epoch if the validation loss improved.
save_best = callbacks.ModelCheckpoint(model_path,
                                        monitor='val_loss',
                                        verbose=1,
                                        save_best_only=True,
                                        mode='min')
#stop training if the validation loss doesn't improve for 5 consecutive epochs.
early_stop = callbacks.EarlyStopping(monitor='val_loss',
                                        min_delta=0,
                                        patience=2,
                                        verbose=0,
                                        mode='auto')
callbacks_list = [save_best, early_stop]


model.fit([train_X], train_Y,
            batch_size=100,
            nb_epoch=20,
            validation_data=([val_X], val_Y),
            callbacks=callbacks_list,
            verbose=2)
