from pydyn_surv import basic_linear_classifier as blc
from pydyn_surv import generate_dataset as gd
import numpy as np

WEIGHT = np.array([-1,2.1,-3.5,4.3,5.2])
DATASET_LEN = 100
ETA = 0.1
ETA_ST = 1
ITER = 2000
VERBOSE = False

print('WEIGHT: {}\n\
DATASET_LEN: {}\n\
ETA: {}\n\
ETA_ST: {}\n\
ITER: {}\n\
VERBOSE: {}'.format(WEIGHT,DATASET_LEN,ETA,ETA_ST,ITER,VERBOSE))

train_dataset = gd.generate_binary_features_dataset(WEIGHT,DATASET_LEN,blc.reg_predictor)
print(train_dataset)

print()
print('No randomness:')
print('--------------')

predicted_width = blc.gradient_descent(blc.squared_loss,blc.squared_loss_derivative,train_dataset,ETA,ITER,VERBOSE)
loss = sum(blc.squared_loss(predicted_width,x,y) for x,y in train_dataset)/len(train_dataset)
print('With normal gradient descent:        {}    {}'.format(predicted_width, loss))

# print(predicted_width*(1/abs(predicted_width[0])))

predicted_width = blc.stocastic_gradient_descent(blc.squared_loss,blc.squared_loss_derivative,train_dataset,ETA_ST,ITER,VERBOSE)
loss = sum(blc.squared_loss(predicted_width,x,y) for x,y in train_dataset)/len(train_dataset)
print('With stocastic gradient descent:     {}    {}'.format(predicted_width, loss))

# print(predicted_width*(1/abs(predicted_width[0])))


train_dataset = gd.generate_binary_features_dataset_with_randomness(WEIGHT,DATASET_LEN,blc.reg_predictor)
print(train_dataset)

print()
print('Randomness:')
print('-----------')

predicted_width = blc.gradient_descent(blc.squared_loss,blc.squared_loss_derivative,train_dataset,ETA,ITER,VERBOSE)
loss = sum(blc.squared_loss(predicted_width,x,y) for x,y in train_dataset)/len(train_dataset)
print('With normal gradient descent:        {}    {}'.format(predicted_width, loss))


predicted_width = blc.stocastic_gradient_descent(blc.squared_loss,blc.squared_loss_derivative,train_dataset,ETA_ST,ITER,VERBOSE)
loss = sum(blc.squared_loss(predicted_width,x,y) for x,y in train_dataset)/len(train_dataset)
print('With stocastic gradient descent:     {}    {}'.format(predicted_width, loss))
