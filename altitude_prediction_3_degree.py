# -*- coding: utf-8 -*-
"""FODS_3_degree.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rOutD-WiUnKT6oVtZjSfnb7BPboH329A

#Data Preprocessing - Making DataFrame, Splitting data and Normalizing Values
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from tqdm import tqdm_notebook
import matplotlib.colors
from mpl_toolkits import mplot3d
from math import sqrt

from google.colab import drive
drive.mount('/content/drive/')
root_path = '/content/drive/My Drive/3D_spatial_network.csv'

training_data= pd.read_csv(root_path)
training_data_new= training_data.drop('id',axis=1)

train=training_data_new.sample(frac=0.7,random_state=1) #random state is a seed value
test=training_data_new.drop(train.index)

X_train = train.drop('altitude',axis=1)
Y_train = train['altitude']
X_test = test.drop('altitude',axis=1)
Y_test = test['altitude']

Y_train=pd.DataFrame(Y_train)
Y_test = pd.DataFrame(Y_test)

X_train_normalize = (X_train-X_train.mean())/X_train.std()

training_X = X_train_normalize.values   ##numpy arrays

Y_train_normalize = (Y_train-Y_train.mean())/Y_train.std()

training_Y = Y_train_normalize.values

X_test_normalize = (X_test-X_train.mean())/X_train.std()
Y_test_normalize = (Y_test-Y_train.mean())/Y_train.std()

testing_Y = Y_test_normalize.values
testing_X = X_test_normalize.values

training_data_new = X_train_normalize
testing_data_new = X_test_normalize

X_train_normalize.std()

x1_list = training_data_new['latitude'].tolist()
x1_square_list = list(map(lambda x: x**2 , x1_list))
training_data_new['x1_square'] = x1_square_list

x2_list = training_data_new['longitude'].tolist()
x2_square_list = list(map(lambda x: x**2 , x2_list))
training_data_new['x2_square'] = x2_square_list

x1_x2_list = list(map(lambda x,y: x*y , x1_list, x2_list))
training_data_new['x1_x2'] = x1_x2_list

x1_cube_list = list(map(lambda x: x**3 , x1_list))
training_data_new['x1_cube'] = x1_cube_list

x2_cube_list = list(map(lambda x: x**3 , x2_list))
training_data_new['x2_cube'] = x2_cube_list

x1_square_x2_list = list(map(lambda x,y: x*y , x1_square_list, x2_list))
training_data_new['x1_square_x2'] = x1_square_x2_list

x2_square_x1_list = list(map(lambda x,y: x*y , x2_square_list, x1_list))
training_data_new['x2_square_x1'] = x2_square_x1_list

##testing data

x1_list = testing_data_new['latitude'].tolist()
x1_square_list = list(map(lambda x: x**2 , x1_list))
testing_data_new['x1_square'] = x1_square_list

x2_list = testing_data_new['longitude'].tolist()
x2_square_list = list(map(lambda x: x**2 , x2_list))
testing_data_new['x2_square'] = x2_square_list

x1_list = testing_data_new['latitude'].tolist()
x2_list = testing_data_new['longitude'].tolist()
x1_x2_list = list(map(lambda x,y: x*y , x1_list, x2_list))
testing_data_new['x1_x2'] = x1_x2_list

x1_list = testing_data_new['latitude'].tolist()
x1_cube_list = list(map(lambda x: x**3 , x1_list))
testing_data_new['x1_cube'] = x1_cube_list

x2_list = testing_data_new['longitude'].tolist()
x2_cube_list = list(map(lambda x: x**3 , x2_list))
testing_data_new['x2_cube'] = x2_cube_list

x1_square_x2_list = list(map(lambda x,y: x*y , x1_square_list, x2_list))
testing_data_new['x1_square_x2'] = x1_square_x2_list

x2_square_x1_list = list(map(lambda x,y: x*y , x2_square_list, x1_list))
testing_data_new['x2_square_x1'] = x2_square_x1_list

training_data_new.head()

X_train_normalize = training_data_new
X_test_normalize = testing_data_new

training_X = X_train_normalize.values   ##numpy arrays
training_Y = Y_train_normalize.values

testing_Y = Y_test_normalize.values
testing_X = X_test_normalize.values


"""#Normal Equations Method"""

##Adding a column of 1's in training_X
normal_X = X_train_normalize
normal_Y = Y_train_normalize
normal_X['constant'] = 1
normal_X.head()

dot_product = np.dot((normal_X.T),normal_X)
normal_inverse = np.linalg.inv(dot_product)
temp = np.dot(normal_X.T, normal_Y) 
normal_wt = np.dot(normal_inverse, temp)
print(normal_wt)

H = np.dot(normal_X, normal_wt)
normal_error = 0.5*(np.dot(((H - normal_Y).T),(H - normal_Y)))
print(normal_error)

sums=0
for i in range(len(training_Y)):
  sq = (training_Y[i])**2
  sums+=sq
sst = sums

sse = normal_error[0,0]
r_square = 1 - (2*sse/sst)
print(r_square,sst)

rmse = sqrt(sse/training_Y.shape[0]) 
print(rmse)

print(sse/2,sst)

normal_test_X = X_test_normalize
normal_test_X['constant'] = 1

### Calculating error on Test Data ###
H_test = np.dot(normal_test_X, normal_wt)
Error_Test = 0.5*(np.dot(((H_test - testing_Y).T),(H_test - testing_Y)))
sse_test = 2*Error_Test[0][0]
print(sse_test)

sums=0
for i in range(len(testing_Y)):
  sq = (testing_Y[i])**2
  sums+=sq
sst_test = sums
r_square = 1 - (sse_test/sst_test)
print(r_square)

rmse_test = sqrt(sse_test/testing_Y.shape[0]) 
print(rmse_test)


"""#Main Code: Normal Gradient Descent"""

wt_matrix = []
wt = np.zeros((1,9))
b=0
Loss=[]
count=0

epochs = 300   
eta = 1e-7  
stopping_criteria= 1e-5 

for x in (range(0,epochs)):
  grad_w=0
  grad_b=0
  H = (np.dot(training_X,wt.T)) + b
  for i in tqdm_notebook(range(0,len(training_X)),total = len(training_X), unit = 'training_X'):
    grad_w += (H[i] - training_Y[i])* training_X[i]
    grad_b += H[i] - training_Y[i]
  wt = wt - eta*(grad_w)
  b = b- eta*(grad_b)    
  # wt_matrix.append(wt)

  Error = 0.5*(np.dot(((H - training_Y).T),(H - training_Y))) 
  count+=1
  print(Error,count)

  Loss.append(Error[0,0])        ## Here actual error starts from 1st iteration. 
  # print(Loss[0], Loss[1])
  if (abs(Loss[x-1]-Loss[x])<stopping_criteria and x!=0):
    print(x)
    print(Loss[x-1]-Loss[x])
    break                            ## So index of loss represents iteration number. 
                                ## 0th index has no meaning

# Check for overfitted weights
print(b,count)
print(wt)

plt.plot(Loss,'*-')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.show()
print(eta)

sums=0
for i in range(len(training_Y)):
  sq = training_Y[i]**2
  sums+=sq

sst = sums
sse = 2*Error
print(sst)
r_square = 1 - (sse/sst)
print(r_square)

rmse = sqrt(sse/training_Y.shape[0]) 
print(rmse)

### Calculating error on Test Data ###
H_test = np.dot(testing_X, wt.T) + b
Error_Test = 0.5*(np.dot(((H_test - testing_Y).T),(H_test - testing_Y)))
sse_test = 2*Error_Test[0][0]
print(sse_test)

sums=0
for i in range(len(testing_Y)):
  sq = (testing_Y[i])**2
  sums+=sq
sst_test = sums
r_square = 1 - (sse_test/sst_test)
print(r_square)

rmse_test = sqrt(sse_test/testing_Y.shape[0]) 
print(rmse_test)

print(rmse,rmse_test)

