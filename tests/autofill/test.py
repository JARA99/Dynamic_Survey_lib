import numpy as np
from pydyn_surv import ml
import itertools as it

points = []
true_w = np.array([-2,-1,0,1,2])
d = len(true_w)

category_vectors = it.product([-1,0,1], repeat=5)

for x in category_vectors:
    x = np.random.randint(-1,2,d)
    y = true_w.dot(x) + np.random.randn()
    points.append((x, y))

print(points)
input('Continue?')

def F(w):
    return sum((w.dot(x) - y)**2 for x, y in points) / len(points)

def dF(w):
    return sum(2*(w.dot(x) - y)*x for x, y in points) / len(points)


def gradient_descent(F, dF, w0, eta, iter):
    w = w0
    for t in range(iter):
        value = F(w)
        gradient = dF(w)
        w = w - eta*gradient
        print('iteration {}: w = {}, F(w) = {}'.format(t, w, value))
    return w

w0 = np.array([0, 0, 0, 0, 0])
eta = 0.1
iter = 2000

method1 = gradient_descent(F, dF, w0, eta, iter)

method2 = ml.gradient_descent(ml.squared_loss,ml.squared_loss_derivative,points,eta,iter,True,w0)

print('method1:',method1)
print('method2:',method2)