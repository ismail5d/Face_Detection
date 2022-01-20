import tensorflow as tf

import os

from keras_applications.imagenet_utils import _obtain_input_shape

from tensorflow.keras.layers import (Input, GlobalAveragePooling2D, 
    Activation, Conv2D, MaxPooling2D, BatchNormalization, 
    AveragePooling2D)

from tensorflow.keras import (Model, backend, layers)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
full_dir=lambda x,y: x+y


utils={
        'WEIGHTS': full_dir(BASE_DIR,
        "/weights/vggface_tf_resnet50.h5")

}

def RESNET50_extra():

    weights='vggface'
    input_tensor=None
    include_top=False
    input_shape=(224, 224, 3)

    input_shape = _obtain_input_shape(input_shape,
                                      default_size=224,
                                      min_size=32,
                                      data_format=backend.image_data_format(),
                                      require_flatten=include_top,
                                      weights=weights) #(224,224,3)
    
    img_input = Input(shape=input_shape)
    
    bn_axis = 3 if backend.image_data_format() == 'channels_last' else 1

    x = Conv2D(
        64, 7, use_bias=False, strides=(2, 2), padding='same')(img_input)

    x = BatchNormalization(axis=bn_axis)(x)
    #https://www.tensorflow.org/api_docs/python/tf/keras/layers/BatchNormalization
    
    x = Activation('relu')(x)#https://www.tensorflow.org/api_docs/python/tf/keras/layers/Activation
    x = MaxPooling2D((3, 3), strides=(2, 2))(x) #https://www.tensorflow.org/api_docs/python/tf/keras/layers/MaxPool2D

    x = resnet_convolution_block(x, 3, [64, 64, 256], stage=2, block=1, strides=(1, 1))
    for i in range(2,4):
        x = resnet_id_block(x, 3, [64, 64, 256], stage=2, block=i)

    x = resnet_convolution_block(x, 3, [128, 128, 512], stage=3, block=1)
    for i in range(2,5):
        x = resnet_id_block(x, 3, [128, 128, 512], stage=3, block=i)

    x = resnet_convolution_block(x, 3, [256, 256, 1024], stage=4, block=1)
    for i in range(2,7):
        x = resnet_id_block(x, 3, [256, 256, 1024], stage=4, block=i)

    x = resnet_convolution_block(x, 3, [512, 512, 2048], stage=5, block=1)
    for i in range(2,4):
        x = resnet_id_block(x, 3, [512, 512, 2048], stage=5, block=i)

    x = AveragePooling2D((7, 7))(x)#https://www.tensorflow.org/api_docs/python/tf/keras/layers/AveragePooling2D

    x = GlobalAveragePooling2D()(x)#https://www.tensorflow.org/api_docs/python/tf/keras/layers/GlobalAveragePooling2D


    # Nv model (Module)
    model = Model(img_input, x)

    # telechargement des donnèes d'entrainement

    model.load_weights(utils['WEIGHTS'])

    return model
def resnet_convolution_block(input_tensor, kernel_size, filters, stage, block,
                      strides=(2, 2), bias=False):
    filters1, filters2, filters3 = filters
    bn_axis = 3 if backend.image_data_format() == 'channels_last' else 1
    
    x = Conv2D(filters1, (1, 1), strides=strides, use_bias=bias)(input_tensor)
    x = BatchNormalization(axis=bn_axis)(x)
    x = Activation('relu')(x)

    x = Conv2D(filters2, kernel_size, padding='same', use_bias=bias)(x)
    x = BatchNormalization(axis=bn_axis)(x)
    x = Activation('relu')(x)

    x = Conv2D(filters3, (1, 1), use_bias=bias)(x)
    x = BatchNormalization(axis=bn_axis)(x)

    shortcut = Conv2D(filters3, (1, 1), strides=strides, use_bias=bias)(input_tensor)
    shortcut = BatchNormalization(axis=bn_axis)(
        shortcut)

    x = layers.add([x, shortcut])
    x = Activation('relu')(x)
    return x


def resnet_id_block(input_tensor, kernel_size, filters, stage, block,
                          bias=False):
    filters1, filters2, filters3 = filters
    bn_axis = 3 if backend.image_data_format() == 'channels_last' else 1

    x = Conv2D(filters1, (1, 1), use_bias=bias)(
        input_tensor)
    x = BatchNormalization(axis=bn_axis)(x)
    x = Activation('relu')(x)

    x = Conv2D(filters2, kernel_size, use_bias=bias,
               padding='same')(x)
    x = BatchNormalization(axis=bn_axis)(x)
    x = Activation('relu')(x)

    x = Conv2D(filters3, (1, 1), use_bias=bias)(x)
    x = BatchNormalization(axis=bn_axis)(x)

    x = layers.add([x, input_tensor])
    x = Activation('relu')(x)
    return x
