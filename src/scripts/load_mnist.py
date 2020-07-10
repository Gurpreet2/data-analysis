# Borrowed from https://www.kaggle.com/hojjatk/read-mnist-dataset/execution
import struct
from array import array
import numpy as np
import logging
logging = logging.getLogger(__name__)


def read_images_labels(images_filepath, labels_filepath, amount):
    labels = []
    with open(labels_filepath, 'rb') as f:
        magic_num, size = struct.unpack('>II', f.read(8))
        amount = size if amount > size else amount
        if magic_num != 2049:
            logging.error("This is not a labels file!")
            exit(1)
        labels = np.array(array('B', f.read(amount)))
    with open(images_filepath, 'rb') as f:
        magic_num, size, rows, cols = struct.unpack('>IIII', f.read(16))
        amount = size if amount > size else amount
        if magic_num != 2051:
            logging.error("This is not an images file!")
            exit(1)
        image_data = array('B', f.read(amount*rows*cols))
    images = np.array([0]*(amount*rows*cols)).reshape((amount, rows*cols))
    for i in range(amount):
        images[i] = np.array(image_data[i*rows*cols:(i+1)*rows*cols])
    return images, labels
