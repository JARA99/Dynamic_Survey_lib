import numpy as np
from . import ml
import math
# from .item import item
# from .survey import survey

SELF_STD_W,SELF_COUNT_W,CAT_STD_W,CAT_COUNT_W = 0.5,-0.5,0.25,-0.25
PREDICTOR = ml.reg_predictor

def FUNC_FALSE(*args,**kargs):
    """Returns False. Useful for the 'condition' and 'probability' methods on `pydyn_surv.survey.survey` and `pydyn_surv.item.item` objects.
    """
    return False

def FUNC_TRUE(*args,**kargs):
    """Returns True. Useful for the 'condition' and 'probability' methods on `pydyn_surv.survey.survey` and `pydyn_surv.item.item` objects.
    """
    return True

def TRAIN_FUNCTION(self,gradient_des:callable = ml.gradient_descent,eta:float = 0.1,iter_:int = 2000,verbose:bool = False):
    """Trains the item using the gradient descent method.
    Parameters
    ----------
    gradient_des: callable
        The gradient descent function to be used.
    eta: float
        The learning rate.
    iter_: int
        The number of iterations.
    verbose: bool
        If True, prints the iteration number and the loss at each iteration.
    Returns
    -------
    trained_w: np.ndarray
        The trained weight vector.
    """
    dataset = self.get_training_dataset()
    w = self.get_weight()
    trained_w = gradient_des(ml.squared_loss,ml.squared_loss_derivative,dataset,eta,iter_,verbose,w)

    return trained_w

def FUNC_LIKERT_ITEM_PROBABILITY(self,axis_move = 2):
    """Returns the probability for an item to be launched based on the predicted label and the axis move only.
    Parameters
    ----------
    axis_move: int
        The axis move.
    Returns
    -------
    prob: float
        The probability for the item to be launched.
    """
    if not self.get_predicted_label() is np.nan:
        if not np.isnan(self.expertvalue):
            prob = (self.get_predicted_label() + axis_move) * (1 + self.expertvalue)
        else:
            prob = self.get_predicted_label() + axis_move
        if prob < 0:
            prob = 0

        return prob
    else:
        if not np.isnan(self.expertvalue):
            prob = axis_move*(1+self.expertvalue)
        else:
            prob = axis_move
        if prob < 0:
            prob = 0
        
        return prob

def FUNC_APPLY_TO_ITEM_AND_CATEGORY_HISTORY(self,func:callable,*args,**kargs):
    """Applies a function to the item history and the category history and returns a list for each one.
    Parameters
    ----------
    func: callable
        The function to be applied.
    *args: list
        The arguments for the function.
    **kargs: dict
        The keyword arguments for the function.
    Returns
    -------
    item_func: list
        The list of the function applied to the item history.
    cat_func: list
        The list of the function applied to the category history.
    """

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


def FUNC_LIKERT_ITEM_PROBABILITY_WITH_STATISTICS(self,axis_move = 2,not_repeated_since = 5,std_weight = SELF_STD_W,cat_std_weight = CAT_STD_W,launch_count_weight = SELF_COUNT_W,cat_launch_count_weight = CAT_COUNT_W,predicted_label_weight = None):
    """Returns the probability for an item to be launched based on the predicted label, the axis move and the statistics of the item and category history.
    Parameters
    ----------
    axis_move: int
        The axis move.
    not_repeated_since: int
        The number of launches since the last launch of the item.
    std_weight: float
        The weight of the standard deviation of the item history in the probability.
    cat_std_weight: float
        The weight of the standard deviation of the category history in the probability.
    launch_count_weight: float
        The weight of the launch count of the item in the probability.
    cat_launch_count_weight: float
        The weight of the launch count of the category in the probability.
    predicted_label_weight: float
        The weight of the predicted label in the probability.
    Returns
    -------
    prob: float
        The probability for the item to be launched.
    """
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
    
    if predicted_label_weight is None:
        predicted_label_weight = origin_srv.get_launch_count()/origin_srv.item_amount
        if predicted_label_weight > 1:
            predicted_label_weight = 1 + math.log(predicted_label_weight)

    prob_elements = [axis_move,self.get_predicted_label()*predicted_label_weight,item_std*std_weight,cat_std*cat_std_weight,item_count_percent*launch_count_weight,cat_count_percent*cat_launch_count_weight]

    if np.isnan(prob_elements).all():
        prob = 0
    else:
        if not np.isnan(self.expertvalue):
            prob = (1 + self.expertvalue)*np.nansum(prob_elements)
        else:
            prob = np.nansum(prob_elements)

    if prob < 0:
        prob = 0

    return prob


def FUNC_STD(l:list,return_when_empty = 0):
    """Returns the standard deviation of a list.
    Parameters
    ----------
    l: list
        The list to calculate the standard deviation.
    return_when_empty: float
        The value to return when the list is empty.
    Returns
    -------
    std: float
        The standard deviation of the list.
    """
    if len(l) == 0:
        return return_when_empty
    return np.std(l)

def CONDITION_ORIGIN_LAUNCH_COUNT_OVER(self,count = 4,all_origins = False):
    """Returns True if the launch count of the origin is over the count.
    Parameters
    ----------
    count: int
        The count to compare.
    all_origins: bool
        If True, all the origins must have a launch count over the count.
    Returns
    -------
    bool
        True if the launch count of the origin is over the count.
    """
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
    """Returns True if the launch count of the origin is below the count.
    Parameters
    ----------
    count: int
        The count to compare.
    all_origins: bool
        If True, all the origins must have a launch count below the count.
    Returns
    -------
    bool
        True if the launch count of the origin is below the count.
    """
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


