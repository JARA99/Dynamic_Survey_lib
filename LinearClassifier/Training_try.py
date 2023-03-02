import basic_linear_classifier as blc
import generate_dataset as gd
import numpy as np

WEIGHT = np.array([-1,1,0,1,-1])
DATASET_LEN = 100
ETA = 0.1
ITER = 10000
VERBOSE = True

train_dataset = gd.generate_dataset(WEIGHT,DATASET_LEN)
# print(train_dataset)

predicted_width = blc.gradient_descent(blc.hinge_loss,blc.hinge_loss_derivative,train_dataset,ETA,ITER,VERBOSE)
print(predicted_width)

train_dataset = gd.generate_dataset_with_randomness(WEIGHT,DATASET_LEN)
# print(train_dataset)

predicted_width = blc.gradient_descent(blc.hinge_loss,blc.hinge_loss_derivative,train_dataset,ETA,ITER,VERBOSE)
print(predicted_width)