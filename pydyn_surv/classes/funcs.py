import numpy as np
from ..LinearClassifier import basic_linear_classifier as blc
# from .item import item
# from .survey import survey

SELF_STD_W,SELF_COUNT_W,CAT_STD_W,CAT_COUNT_W = 0.5,-0.5,0.25,-0.25
PREDICTOR = blc.reg_predictor

def FUNC_FALSE(*args,**kargs):
    return False

def FUNC_TRUE(*args,**kargs):
    return True

def TRAIN_FUNCTION(self,gradient_des:callable = blc.gradient_descent,eta:float = 0.1,iter_:int = 2000,verbose:bool = False):
    dataset = self.get_training_dataset()
    w = self.get_weight()
    trained_w = gradient_des(blc.squared_loss,blc.squared_loss_derivative,dataset,eta,iter_,verbose,w)

    return trained_w

def FUNC_LIKERT_ITEM_PROBABILITY(self,axis_move = 2):
    if not self.get_predicted_label() is np.nan:
        prob = self.get_predicted_label() + axis_move + self.expertvalue
        if prob < 0:
            prob = 0

        return prob
    else:
        prob = axis_move+self.expertvalue
        if prob < 0:
            prob = 0
        
        return prob

def FUNC_APPLY_TO_ITEM_AND_CATEGORY_HISTORY(self,func:callable,*args,**kargs):


    categories = np.where(self.category_vector != 0)[0] # [0] is necessary to get the array from the tuple.
    answer_history = self.get_answer_history()
    srv_cat_history = self.get_origin_survey().get_category_answer_history()

    cat_func_list = []
    for i in categories:
        func_to_cat = func(srv_cat_history[i],*args,**kargs)
        cat_func_list.append(func_to_cat)


    cat_func = np.nanmean(cat_func_list)
    item_func = func(answer_history,*args,**kargs)

    return item_func, cat_func


def FUNC_LIKERT_ITEM_PROBABILITY_WITH_STATISTICS(self,axis_move = 2,not_repeated_since = 5,std_weight = SELF_STD_W,cat_std_weight = CAT_STD_W,launch_count_weight = SELF_COUNT_W,cat_launch_count_weight = CAT_COUNT_W):

    last_launch = self.get_last_launch()
    origin_srv = self.get_origin_survey()
    srv_launch_count = origin_srv.get_launch_count()

    launched_since = np.nansum([srv_launch_count, -last_launch])
    # print(launched_since)
    if launched_since < not_repeated_since:
        # print("Not repeated since ",launched_since," launches")
        return 0

    item_std, cat_std = FUNC_APPLY_TO_ITEM_AND_CATEGORY_HISTORY(self,FUNC_STD)
    item_count, cat_count = FUNC_APPLY_TO_ITEM_AND_CATEGORY_HISTORY(self,len)

    if srv_launch_count > 0:
        item_count_percent = item_count / srv_launch_count
        cat_count_percent = cat_count / srv_launch_count
    else:
        item_count_percent = 0
        cat_count_percent = 0

    prob_elements = [axis_move,self.expertvalue,item_std*std_weight,cat_std*cat_std_weight,item_count_percent*launch_count_weight,cat_count_percent*cat_launch_count_weight]

    if np.isnan(prob_elements).all():
        prob = 0
    else:
        prob = np.nansum(prob_elements)

    if prob < 0:
        prob = 0

    return prob


def FUNC_STD(l:list,return_when_empty = 0):
    if len(l) == 0:
        return return_when_empty
    return np.std(l)

def CONDITION_ORIGIN_LAUNCH_COUNT_OVER(self,count = 4,all_origins = False):
    if all_origins:
        for origin in self.origin:
            if origin.get_launch_count() < count:
                return False
        return True
    else:
        for origin in self.origin:
            if origin.get_launch_count() >= count:
                return True
        return False

def CONDITION_ORIGIN_LAUNCH_COUNT_BELOW(self,count = 4,all_origins = False):
    if all_origins:
        for origin in self.origin:
            if origin.get_launch_count() >= count:
                return False
        return True
    else:
        for origin in self.origin:
            if origin.get_launch_count() < count:
                return True
        return False


