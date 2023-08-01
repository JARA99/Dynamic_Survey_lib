from pydyn_surv.item import DEFAULT_PARAMETERS_DICT
from pydyn_surv.item import item
from pydyn_surv.survey import survey
from pydyn_surv import ml
import numpy as np
import itertools as it
import matplotlib.pyplot as plt

DIM = 5
POSSIBLE_ANSWERS = np.linspace(-2,2,5)
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
            a += np.random.normal(0,1)
        if fit_answer:
            a = take_closest(a,self.answers_fit)
        else:
            if in_range_answer:
                if a <= ANSWER_RANGE[0]:
                    a = ANSWER_RANGE[0]
                elif a >= ANSWER_RANGE[1]:
                    a = ANSWER_RANGE[1]
        
        item_.answer(a,not in_range_answer,**kargs)

class complex_user(user):
    def __init__(self, target_w=np.zeros(DIM), answers_fit=POSSIBLE_ANSWERS):
        super().__init__(target_w, answers_fit)
    
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

        movement = np.random.normal(0,0.1,DIM)

        
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

def get_survey_entropy(s:survey):
    """Returns the entropy of the survey.
    Parameters
    ----------
    surv: Survey
        The survey to be analyzed.
    Returns
    -------
    entropy: float
        The entropy of the survey.
    """
    items_probs_w = np.array(s.get_items().probabilities(True))
    total_w = np.sum(items_probs_w)
    items_probs = items_probs_w/total_w
    items_probs = items_probs[items_probs != 0]

    entropies = [x*np.log(x) for x in items_probs]
    entropy = -np.sum(entropies)

    return entropy

def get_survey_rsquared(s:survey):
    """Returns the r squared of the survey.
    Parameters
    ----------
    surv: Survey
        The survey to be analyzed.
    Returns
    -------
    r_squared: float
        The r squared of the survey.
    """
    tds = s.get_training_dataset()
    tds_x = [pair[0] for pair in tds]
    tds_y = np.array([pair[1] for pair in tds])
    trained_w = s.get_weight()

    trained_y = np.array([np.dot(trained_w,x) for x in tds_x])
    y_mean = np.mean(tds_y)

    ss_res = np.sum((tds_y-trained_y)**2)
    ss_tot = np.sum((tds_y-y_mean)**2)

    if ss_tot == 0:
        r_squared = np.nan
    else:
        r_squared = 1 - (ss_res/ss_tot)

    return r_squared



def plot_bars(user_name,counts,subfix='_wh_cf',title_extra='',save_path='output/current_run/count_bars/'):

    # Make a grouped bar chart showing ocurrences of -1,0 and 1 in each grouped column, each column is a weight coordinate:
    # 1st column is w0, 2nd column is w1 and 3rd column is w2

    # set width of bar
    barWidth = 0.25
    fig, ax = plt.subplots(figsize =(12, 8))
    # set height of bar
    bars1 = counts[0]
    bars2 = counts[1]
    bars3 = counts[2]

    # Set position of bar on X axis
    r1 = np.arange(len(bars1))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]

    # Make the plot
    ax.bar(r1, bars1, color='C3', width=barWidth, edgecolor='white', label='-1')
    ax.bar(r2, bars2, color='C1', width=barWidth, edgecolor='white', label='0')
    ax.bar(r3, bars3, color='C2', width=barWidth, edgecolor='white', label='1')

    # Add xticks on the middle of the group bars
    ax.set_xlabel('Ocurrencias')
    ax.set_ylabel('Categoría')
    ax.set_title('Ocurrencias de cada categoría en cada coordenada de peso\nUsuario {}{}'.format(user_name,title_extra))
    ax.set_xticks([r + barWidth for r in range(len(bars1))], ['C{}'.format(i+1) for i in range(len(bars1))])

    # Create legend & Show graphic
    ax.legend()
    fig.savefig('{}{}{}.png'.format(save_path,user_name,subfix))

    # plt.close(fig)


# def w_evolution(w:np.ndarray):
#     r_w = []
#     for coord in w:
#         start_cord = coord + np.random.normal(0,0.2,1)[0]

#         if start_cord < -1:
#             move = - (start_cord + 1.5) * 0.005
#             r_w.append(start_cord + move)
#         elif -1 <= start_cord < -0.2:
#             move = - (start_cord + 0.4) * 0.005
#             r_w.append(start_cord + move)
#         elif -0.2 <= start_cord <= 0.2:
#             move = np.random.normal(0,0.05,1)[0]
#             r_w.append(start_cord + move)
#         elif 0.2 < start_cord <= 1:
#             move = - (start_cord - 0.4) * 0.005
#             r_w.append(start_cord + move)
#         elif start_cord > 1:
#             move = - (start_cord - 1.5) * 0.005
#             r_w.append(start_cord + move)

#     extra_move = np.random.normal(0,0.001,len(w))
    
#     return np.array(r_w+extra_move)

def w_evolution(w:np.ndarray):
    r_w = w.copy()
    for i in range(len(r_w)):
        if i%2 == 0:
            r_w[i] += np.random.normal(-0.0001,0.005,1)[0]
        else:
            r_w[i] += np.random.normal(0.0001,0.005,1)[0]
    return r_w



