from pydyn_surv.item import DEFAULT_PARAMETERS_DICT
from pydyn_surv.item import item
from pydyn_surv import ml
import numpy as np
import itertools as it

DIM = 5
POSSIBLE_ANSWERS = np.linspace(-2,2,17)
ANSWER_RANGE = (-2,2)
TDS_LEN = 50

def take_closest(num,collection):
   return min(collection,key=lambda x:abs(x-num))

class user:
    global DIM
    global POSSIBLE_ANSWERS
    global ANSWER_RANGE

    def __init__(self,target_w=np.zeros(DIM),answers_fit=POSSIBLE_ANSWERS):
        self.target_w = target_w
        self.answers_fit = answers_fit
    
    def answer_item(self, item_: item, fit_answer = True, add_noise = True,kargs=dict(),in_range_answer=True):
        a = np.dot(self.target_w,item_.category_vector)
        if add_noise:
            a += np.random.normal(0,0.25)
        if fit_answer:
            a = take_closest(a,self.answers_fit)
        else:
            if in_range_answer:
                if a <= ANSWER_RANGE[0]:
                    a = ANSWER_RANGE[0]
                elif a >= ANSWER_RANGE[1]:
                    a = ANSWER_RANGE[1]
        
        item_.answer(a,not in_range_answer,**kargs)

        
def create_items_dicts(base_dict = DEFAULT_PARAMETERS_DICT, dim = DIM):
    """Creates a vector with dim=dim for each combination of -1,0,1,
    e.g. for dim=3: [[-1,-1,-1],[-1,-1,0],[-1,-1,1],[-1,0,-1],[-1,0,0],[-1,0,1],[-1,1,-1],[-1,1,0],[-1,1,1],[0,-1,-1],[0,-1,0],[0,-1,1],[0,0,-1],[0,0,0],[0,0,1],[0,1,-1],[0,1,0],[0,1,1],[1,-1,-1],[1,-1,0],[1,-1,1],[1,0,-1],[1,0,0],[1,0,1],[1,1,-1],[1,1,0],[1,1,1]]
    Then, for each vector, creates a dictionary with the base_dict and the vector as the 'category_vector', and uses the vector as string for the 'question'.
    Finally, returns a list of all the dictionaries.
    """

    # Create all possible combinations of -1,0,1 for the category_vector
    category_vectors = it.product([-1,0,1], repeat=dim)
    # Create a list of dictionaries, each with the base_dict and the category_vector
    items_dicts = []
    for category_vector in category_vectors:
        item_dict = base_dict.copy()
        item_dict['category_vector'] = np.array(category_vector)
        item_dict['question'] = ', '.join(map(str,category_vector))
        items_dicts.append(item_dict)
    return items_dicts


def custom_train_function(self,tds_len=TDS_LEN,gradient_des:callable = ml.gradient_descent,eta:float = 0.1,iter_:int = 2000,verbose:bool = False):
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
    if len(dataset) > tds_len:
        dataset = dataset[-tds_len:]
    w = self.get_weight()
    trained_w = gradient_des(ml.squared_loss,ml.squared_loss_derivative,dataset,eta,iter_,verbose,w)

    return trained_w
