import os
import numpy as np

from tqdm import tqdm
from scipy.misc import imread
from random import shuffle


def get_images(paths, n_images=1000):

    if isinstance(paths, str):
        paths = [paths]

    images = []
    labels = []

    n = 0
    for path in paths:
        if n > n_images: break
        print(path)
        for image_file in tqdm(os.listdir(path)):
            if n > n_images: break
            if '.jpg' not in image_file: continue
            try:
                img = imread(os.path.join(path, image_file))
                itc = image_file[:-4].split('_')
                lbl = [float(itc[3]), float(itc[5])]
                if img is not None:
                    images.append(img[:, :])
                    labels.append(lbl)
                    n += 1
            except Exception as e:
                pass

    images = np.array(images)
    labels = np.array(labels)

    return images, labels


def shuffle_data(X, Y):
    assert len(X) == len(Y)
    p = np.random.permutation(len(X))
    return X[p], Y[p]


def from_continue_to_discrete(Y):

    def one_hot(i, n):
        t = [0 for j in range(n)]
        t[i] = 1
        return t

    # transform direction angle into a 5 dimensions array of 0 and 1
    arr_discr = [i for i in range(-2, 3)]
    threshs = [-100000, -0.7, -0.25, 0.25, 0.7, 100000]
    ns = [0 for i in range(-2, 3)]

    Y_new = []
    for elt in Y:
        e = elt[1]
        for i in range(len(threshs)):
            if threshs[i] < e < threshs[i+1]:
                t = one_hot(i, 5)
                Y_new.append(t)
                ns[i] += 1
                break

    Y = np.array(Y_new)
    return Y, ns


def equilibrate_dataset(X, Y, ns):
    m = min(ns)

    X_by_label = [[] for i in ns]
    Y_by_label = [[] for i in ns]

    for i in range(len(Y)):
        index = np.argmax(Y[i])
        Y_by_label[index].append(Y[i])
        X_by_label[index].append(X[i])

    all_X = []
    all_Y = []

    for i in range(len(ns)):
        x, y = np.array(X_by_label[i]), np.array(Y_by_label[i])
        x, y = shuffle_data(x, y)
        x = x[:m]
        y = y[:m]
        all_X.extend(x)
        all_Y.extend(y)

    return np.array(all_X), np.array(all_Y)


def get_datasets(paths, n_images):

    X, Y = get_images(paths, n_images=n_images)

    # A classifier is better (when talking about performance) than a simple
    # sigmoid
    Y, ns = from_continue_to_discrete(Y)

    # Equilibrate the dataset between all the possible directions
    X, Y = equilibrate_dataset(X, Y, ns)

    # Shuffle everything
    X, Y = shuffle_data(X, Y)

    # Normalization of the input data (between 0 and 1)
    X = X.astype('float32') / 255.

    # Split between train, val and test
    test_cutoff = int(len(X) * .8) # 80% of data used for training
    val_cutoff = test_cutoff + int(len(X) * .1) # 10% of data used for validation and 10% for test data

    train_X, train_Y = X[:test_cutoff], Y[:test_cutoff]
    val_X, val_Y = X[test_cutoff:val_cutoff], Y[test_cutoff:val_cutoff]
    test_X, test_Y = X[val_cutoff:], Y[val_cutoff:]

    return train_X, train_Y, val_X, val_Y, test_X, test_Y
