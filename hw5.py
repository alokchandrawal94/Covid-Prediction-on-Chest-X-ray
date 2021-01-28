# -*- coding: utf-8 -*-
"""HW5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gye2FfcCC9rG1jgUbgGIu4ZyPIrmye8y
"""

from google.colab import drive
drive.mount('/content/drive')

import cv2
import os
from skimage.io import imread, imshow, imread_collection
from skimage.transform import resize
from skimage.feature import hog
from skimage import exposure
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#%matplotlib inline

#reading the image
img_1 = imread('/content/drive/Shareddrives/CSCE 633(Fall 2020) HW5/train_resized/img_102.jpg',as_gray=True)
imshow(img_1)
print(img_1.shape)

# skimage  takes the input as height x width.
#resizing image 
resized_img_1 = resize(img_1, (128,64)) #64x128 default values of original file. 1:2 ratio important..
imshow(resized_img_1) 
print(resized_img_1.shape)

#creating hog features , use default values..
fd_1, hog_image_1 = hog(resized_img_1, feature_vector=True, visualize=True)
fd_1.shape
#pixels_per_cell=3,3 --> 3218436, 8,8 -->443556

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), sharex=True, sharey=True) 
ax1.imshow(resized_img_1, cmap=plt.cm.gray) 
ax1.set_title('Input image') 
# Rescale histogram for better display 
hog_image_rescaled_1 = exposure.rescale_intensity(hog_image_1, in_range=(0, 10)) 
ax2.imshow(hog_image_rescaled_1, cmap=plt.cm.gray) 
ax2.set_title('Histogram of Oriented Gradients')
plt.show()

images = []
def load_images_from_folder(folder):
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename),cv2.IMREAD_GRAYSCALE)
        if img is not None:
            #print(img.shape) #((2823, 2823, 3))
            images.append(img)
    #return images

load_images_from_folder("/content/drive/Shared drives/CSCE 633(Fall 2020) HW5/train_resized")

len(images)

# skimage  takes the input as height x width.
#resizing image 
resized_images=[]
for i in images:
  r_im= resize(i, (128,64)) 
  resized_images.append(r_im)

print(resized_images[1].shape)

fd_list=[]
hog_images=[]
for imge in resized_images:
  fd_i, hog_image = hog(imge, feature_vector=True, visualize=True)
  fd_list.append(fd_i)
  hog_images.append(hog_image)

print(hog_image.shape)
print(fd_i) #one image as a feacture vectore array

print(len(hog_images))
print(len(fd_list))
print(fd_i.shape)

#can I make a new data to see what is happenening
dataframe = pd.read_csv('/content/drive/Shared drives/CSCE 633(Fall 2020) HW5/train.csv')
dataframe.head(3)
dataframe.tail(3) #249 images
dataframe = dataframe.dropna()

X_train = dataframe.iloc[:, 1:-1].values #filename did not added
y_train = dataframe.iloc[:, -1].values
print(X_train.shape)

np.shape(fd_list)

import pandas as pd 
import csv
resultFile = open("/content/drive/MyDrive/Colab Notebooks/fd_list.csv",'w')
wr = csv.writer(resultFile)
for i in fd_list:
    wr.writerows([i])

columns = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/fd_list.csv',header=None)
new_values = columns.iloc[:, 1:].values
print(new_values.shape)
columns.head(3)

print(new_values.shape)
print(y_train.shape)

result= np.concatenate((new_values, y_train.reshape(len(y_train),1)), axis=1)
print(result.shape)

import pandas as pd 
import csv
resultwithlabel = open("/content/drive/MyDrive/Colab Notebooks/resultwithlabel.csv",'w')
wr = csv.writer(resultwithlabel)
for i in result:
    wr.writerows([i])

wholedata = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/resultwithlabel.csv',header=None)
checkvalues = wholedata.iloc[:, 1:].values
checkresult = wholedata.iloc[:, -1].values
print(checkvalues.shape)
wholedata.head(3)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(checkvalues, checkresult, test_size = 0.2, random_state = 0)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
print(X_train.shape)
print(X_test.shape)

from sklearn.decomposition import PCA
pca = PCA(n_components = 8)
X_train = pca.fit_transform(X_train)
X_test = pca.transform(X_test)

from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state = 0)
classifier.fit(X_train, y_train)

from sklearn.metrics import confusion_matrix, accuracy_score
y_pred = classifier.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
print(cm)
accuracy_score(y_test, y_pred)

Boosting is an Ensemble learning methods that makes use of multiple learners. In boosting different algorithms work closer by learning from each other.

#importing Adaboost library and k-fold
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import KFold

kf = KFold(n_splits=5)
 #dataframe = training data
 kf.get_n_splits(X_train)

print(X_train.shape)
print(y_train.shape)

adaboost = AdaBoostClassifier(n_estimators=100, base_estimator= None,learning_rate=1, random_state = 1)
for train_index, test_index in kf.split(X_train):
  train_x, test_x = X_train[train_index], X_train[test_index]
  train_y, test_y = y_train[train_index], y_train[test_index]
  adaboost.fit(X_train, y_train)

adaboost = AdaBoostClassifier(n_estimators=100, base_estimator= None,learning_rate=1, random_state = 1)
# base_estimator default is decision tree
# n_estimators - The maximum number of estimators at which boosting is terminated
adaboost.fit(X, y)