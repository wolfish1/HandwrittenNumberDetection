# -*- coding: utf-8 -*-
"""HandWrite.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eCXCnxNm43B3ngntnf4y_xxW__wcvadF
"""

#!unzip 1-102

import os
import numpy as np
from sklearn.model_selection import train_test_split
from keras.preprocessing import image
from keras.utils.vis_utils import plot_model
from tensorflow.keras.utils import to_categorical

def load_data():
    path = './1-102/'
    files = os.listdir(path)
    images = []
    labels = []
    for f in files:
        img_path = path + f
        img = image.load_img(img_path, grayscale=False, target_size=(28,28))
        img_array = image.img_to_array(img)
        images.append(img_array)
        
        lb = f.split('_');
        lb = lb[1].split('.png')
        lb = lb[0]
        labels.append(lb);

    data = np.array(images)
    labels = np.array(labels)

    return data, labels

print('Loading data...')
images, lables = load_data()
images /= 255
x_train, x_test, y_train, y_test = train_test_split(images, lables, test_size=0.2)
y_train_onehot = to_categorical(y_train)
y_test_onehot = to_categorical(y_test)

from keras.models import Sequential, model_from_yaml, load_model
from keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.optimizers import SGD,Adam

model = Sequential() #建置線性堆疊模型

#建立卷積層1
model.add(Conv2D(filters=16,        #濾鏡層數
        kernel_size=(5, 5),    #濾鏡大小
        padding='same',       #影像經過卷積計算後大小不變
        input_shape=(28, 28, 3), #輸入影像的大小，顏色彩色
        activation='relu'))     #設定激勵函數
model.add(MaxPooling2D(pool_size=(2, 2))) #建立池化層1
model.add(Dropout(0.25))          #避免overfitting

#建立卷積層2
model.add(Conv2D(filters=36, 
        kernel_size=(5, 5),
        padding='same',
        activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2))) #建立池化層2
model.add(Dropout(0.5))           #避免overfitting

model.add(Flatten())            #建立平坦層
model.add(Dense(10, activation='softmax')) #建立輸出層
model.summary()               #輸出模型

sgd = Adam(learning_rate=0.0003)    #優化器(學習率)
model.compile(loss='binary_crossentropy',optimizer=sgd, metrics=['accuracy'])
      #(損失函數，優化器，評量準則)
train_history = model.fit(x_train, y_train_onehot, batch_size=50, epochs=10, verbose=2, validation_data=(x_test, y_test_onehot))
#model.fit(輸入資料，輸入資料，訓練週期，每一批次訓練幾筆資料，顯示訓練過程，加入驗證集去讓超參數跑得更好)

import matplotlib.pyplot as plt
def show_train_history(train_history, title, train, validation):
    plt.plot(train_history.history[train])
    plt.plot(train_history.history[validation])
    plt.title(title)
    plt.ylabel(train)
    plt.xlabel('Epoch')
    plt.legend(['train', 'validation'], loc = 'upper left')
    plt.show()

show_train_history(train_history, 'Accuracy', 'accuracy', 'val_accuracy')
show_train_history(train_history, 'Loss', 'loss', 'val_accuracy')

import pandas as pd
predict_x = model.predict(x_test)
classes_x=np.argmax(predict_x,axis=1)
pd.crosstab(y_test, classes_x, rownames=['label'], colnames=['predict'])

