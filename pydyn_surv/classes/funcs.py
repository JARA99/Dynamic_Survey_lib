import numpy as np
from ..LinearClassifier import basic_linear_classifier as blc

def FUNC_FALSE(*args,**kargs):
    return False

def FUNC_TRUE(*args,**kargs):
    return True

def TRAIN_FUNCTION(self,gradient_des:callable = blc.gradient_descent,eta:float = 0.1,iter_:int = 2000,verbose:bool = False):
    dataset = self.get_training_dataset()
    w = self.get_weight()
    trained_w = gradient_des(blc.squared_loss,blc.squared_loss_derivative,dataset,eta,iter_,verbose,w)
    
    return trained_w

PREDICTOR = blc.reg_predictor

def FUNC_LIKERT_ITEM_PROBABILITY(self):
    if not self.get_predicted_label() is np.nan:
        prob = self.get_predicted_label() + 2 + self.expertvalue
        if prob < 0:
            prob = 0

        return prob
    else:
        return 2+self.expertvalue


