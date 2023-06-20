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

def FUNC_APPLY_TO_ITEM_AND_SURVEY_HISTORY(self,func:callable,*args,**kargs):


    categories = np.where(self.category_vector != 0)[0]
    answer_history = self.get_answer_history()
    srv_cat_history = self.get_origin_survey().get_category_answer_history()

    srv_func_list = []
    for i in categories:
        try:
            func_to_cat = func(srv_cat_history[i],*args,**kargs)
        except:
            func_to_cat = np.nan
        srv_func_list.append(func_to_cat)
    
    try:
        item_func = func(answer_history,*args,**kargs)
    except:
        item_func = np.nan
    srv_func = np.nanmean(srv_func_list)

    return item_func, srv_func


def FUNC_LIKERT_ITEM_PROBABILITY_WITH_STATISTICS(self,axis_move = 2,not_repeated_since = 5,std_weight = SELF_STD_W,cat_std_weight = CAT_STD_W,launch_count_weight = SELF_COUNT_W,cat_launch_count_weight = CAT_COUNT_W):

    last_launch = self.get_last_launch()
    origin_srv = self.get_origin_survey()
    srv_launch_count = origin_srv.get_launch_count()

    launched_since = srv_launch_count - last_launch
    if launched_since < not_repeated_since:
        return 0

    item_std, surv_std = FUNC_APPLY_TO_ITEM_AND_SURVEY_HISTORY(self,np.std)
    item_count, surv_count = FUNC_APPLY_TO_ITEM_AND_SURVEY_HISTORY(self,len)

    if srv_launch_count > 0:
        item_count_percent = item_count / srv_launch_count
        surv_count_percent = surv_count / srv_launch_count
    else:
        item_count_percent = 0
        surv_count_percent = 0

    prob = np.nansum([axis_move,self.expertvalue,item_std*std_weight,surv_std*cat_std_weight,item_count_percent*launch_count_weight,surv_count_percent*cat_launch_count_weight])

    if prob < 0:
        prob = 0

    return prob




