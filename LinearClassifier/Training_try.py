import basic_linear_classifier as blc
import generate_dataset as gd
import numpy as np

WEIGHT = np.array([-1,1,0,1,-1])
DATASET_LEN = 100
ETA = 0.01
ETA_ST = 1
ITER = 10000
VERBOSE = False

train_dataset = gd.generate_dataset(WEIGHT,DATASET_LEN)
# print(train_dataset)

print()
print('No randomness:')
print('--------------')

predicted_width = blc.gradient_descent(blc.hinge_loss,blc.hinge_loss_derivative,train_dataset,ETA,ITER,VERBOSE)
loss = sum(blc.hinge_loss(predicted_width,x,y) for x,y in train_dataset)/len(train_dataset)
print('With normal gradient descent:        {}    {}'.format(predicted_width, loss))


predicted_width = blc.stocastic_gradient_descent(blc.hinge_loss,blc.hinge_loss_derivative,train_dataset,ETA_ST,ITER,VERBOSE)
loss = sum(blc.hinge_loss(predicted_width,x,y) for x,y in train_dataset)/len(train_dataset)
print('With stocastic gradient descent:     {}    {}'.format(predicted_width, loss))

train_dataset = gd.generate_dataset_with_randomness(WEIGHT,DATASET_LEN)
# print(train_dataset)

print()
print('Randomness:')
print('-----------')

predicted_width = blc.gradient_descent(blc.hinge_loss,blc.hinge_loss_derivative,train_dataset,ETA,ITER,VERBOSE)
loss = sum(blc.hinge_loss(predicted_width,x,y) for x,y in train_dataset)/len(train_dataset)
print('With normal gradient descent:        {}    {}'.format(predicted_width, loss))


predicted_width = blc.stocastic_gradient_descent(blc.hinge_loss,blc.hinge_loss_derivative,train_dataset,ETA_ST,ITER,VERBOSE)
loss = sum(blc.hinge_loss(predicted_width,x,y) for x,y in train_dataset)/len(train_dataset)
print('With stocastic gradient descent:     {}    {}'.format(predicted_width, loss))
