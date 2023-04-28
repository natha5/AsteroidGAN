# -*- coding: utf-8 -*-
"""AsteroidGAN.ipynb

Automatically generated by Colaboratory.

Original file is AsteroidGan.ipynb

# Imports
"""

import numpy as np
import pandas as pd
import random as rand

from keras.layers import Dense, Conv1D
from keras.models import Sequential

"""# Data pre-processing

Due to the large size of dataset, many columns that are not needed and some rows containing null values have already been dropped
"""


def pre_process():
    print("pre-processing data")
    data = pd.read_csv("dataset.csv")

    data = data.drop(['class', 'epoch_cal'], axis=1)
    data = data.dropna()
    data['neo'] = data['neo'].replace(('Y', 'N'), (1, 0))
    data['pha'] = data['pha'].replace(('Y', 'N'), (1, 0))

    data = data.astype('float32')
    data /= 255

    return data


"""# Generator model
16 outputs as there are 16 columns in the dataset
"""


def make_generator():
    print("creating generator")
    model = Sequential()

    model.add(Dense(40, activation='relu', input_shape=INPUT_SHAPE))
    model.add(Dense(1, activation='sigmoid'))

    return model


def generate_fakes():
    neo = rand.choice([1, 0])
    pha = rand.choice([1, 0])
    H = rand.uniform(0, 10000)
    diameter = rand.uniform(0, 100000)
    albedo = rand.uniform(0, 1)
    e = rand.uniform(0, 0.002)
    a = rand.uniform(0, 1)
    q = rand.uniform(0, 1)
    i = rand.uniform(0, 1)
    om = rand.uniform(0, 1)
    w = rand.uniform(0, 2)
    ad = rand.uniform(0, 0.05)
    n = rand.uniform(0, 0.01)
    tp_cal = rand.uniform(0, 100000)
    per = rand.uniform(0, 10)
    moid = rand.uniform(0, 0.1)

    X = np.array([[neo, pha, H, diameter, albedo, e, a, q, i, om, w, ad, n, tp_cal, per, moid]])
    return X


# Discriminator model This is a binary CNN classifier, to determine whether the input is 'real' or not

def make_discriminator():
    print("creating discriminator")
    model = Sequential()

    model.add(Conv1D(64, kernel_size=5, padding='same', activation='relu', input_shape=INPUT_SHAPE))

    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


# Putting the GAN together

def make_gan(generator, discriminator):
    print("creating gan")
    discriminator.trainable = False
    model = Sequential()
    model.add(generator)
    model.add(discriminator)
    model.compile(loss='binary_crossentropy', optimizer=OPTIMIZER)
    return model


"""Training parameters

"""

INPUT_SHAPE = (16, 1)
OPTIMIZER = 'adam'
LOSS = 'binary_crossentropy'
METRICS = 'accuracy'

BATCH_SIZE = 128
N_EPOCHS = 2048
VERBOSE = 1
VALIDATION_SPLIT = 0.2


def training(generator, discriminator, gan, batch_size, n_epochs, data):

    print("training gan for " + str(n_epochs) + " epochs")

    current_row = 0

    half_batch = int(batch_size / 2)
    for i in range(n_epochs):

        print("Epoch : " + str(i + 1) + "/" + str(n_epochs))

        x_real = data[current_row:half_batch + current_row]
        y_real = np.ones((half_batch, 16))

        current_row = current_row + half_batch

        x_fake = np.array([[]])
        for j in range(half_batch):
            current_fake = generate_fakes()
            x_fake = np.append(x_fake, current_fake)

        y_fake = np.zeros((half_batch, 16))

        x_fake = x_fake.reshape(half_batch, 16)

        discriminator.train_on_batch(x_real, y_real)
        discriminator.train_on_batch(x_fake, y_fake)

        x_gan = np.array([[]])

        for j in range(batch_size):
            current_gan = generate_fakes()
            x_gan = np.append(x_gan, current_gan)

        y_gan = np.ones((batch_size, 16))
        x_gan = x_gan.reshape(batch_size, 16)

        gan.train_on_batch(x_gan, y_gan)

    # now training is complete, generate a value to use
    value_real = np.zeros((1, 16))
    while value_real.all() == 0:
        x_using = generate_fakes()

        value = generator.predict(x_using)
        # check value fools discriminator
        value_real = discriminator.predict(value)

    print(value)

    return value


def run_program():
    data = pre_process()
    generator = make_generator()
    discriminator = make_discriminator()
    gan = make_gan(generator, discriminator)
    gan.summary()

    value_to_use = training(generator, discriminator, gan, BATCH_SIZE, N_EPOCHS, data)

    print(value_to_use)

    return value_to_use
