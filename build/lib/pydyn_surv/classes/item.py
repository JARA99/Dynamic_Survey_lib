import numpy as np
from . import funcs

DEFAULT_PARAMETERS_DICT = {
    'question':'',
    'answers':[],
    'answers_values':[-2,-1,0,1,2],
    'category_vector':[],
    'answer_range':(-2,2),
    'expert_extra':0,
    'id':None,
    'origin_survey':None,
}

class item:
    """ Class that represents an item (question) in the survey, and stores some useful data like the user answer history.

    Returns
    -------
    pydyn_surv.item.item
        Instance of the class pydyn_surv.item.item
    """

    instances = []
    def set_all_probability_function(func) -> None:
        """Sets the probability function for all the items.

        Parameters
        ----------
        func : function
            Probability function to be setted.
        """
        for item_ in item.instances:
            item_.set_probability_function(func)

    def __init__(self,parameters_dict:dict = DEFAULT_PARAMETERS_DICT,id_ = None,origin_survey = None, probability_function = funcs.FUNC_LIKERT_ITEM_PROBABILITY):
        """Creates an instance of an pydyn_surv.item.

        Parameters
        ----------
        parameters_dict : dict, optional
            Dictionary containing the atributtes for this instance, by default DEFAULT_PARAMETERS_DICT
        
        Returns
        -------
        pydyn_surv.item.item
            An item instance with the initialization parameters.
        """

        item.instances.append(self)

        try:
            self.question_text = parameters_dict['question']
        except:
            self.question_text = DEFAULT_PARAMETERS_DICT['question']
        
        try:
            self.answers_text = parameters_dict['answers']
        except:
            self.answers_text = DEFAULT_PARAMETERS_DICT['answers']
        
        try:
            self.answers_values = parameters_dict['answers_values']
        except:
            self.answers_values = DEFAULT_PARAMETERS_DICT['answers_values']

        try:
            self.category_vector = parameters_dict['category_vector']
        except:
            self.category_vector = DEFAULT_PARAMETERS_DICT['category_vector']

        try:
            self.answer_range = parameters_dict['answer_range']
        except:
            self.answer_range = DEFAULT_PARAMETERS_DICT['answer_range']
        
        try:
            self.expertvalue = parameters_dict['expert_extra']
        except:
            self.expertvalue = DEFAULT_PARAMETERS_DICT['expert_extra']

        try:
            self.id = parameters_dict['id']
        except:
            self.id = DEFAULT_PARAMETERS_DICT['id']

        try:
            self.origin_survey = parameters_dict['origin_survey']
        except:
            self.origin_survey = DEFAULT_PARAMETERS_DICT['origin_survey']

        if id_ is not None:
            self.id = id_
        if origin_survey is not None:
            self.origin_survey = origin_survey

        self.launch_count = 0
        self.answer_history = []
        self.last_launch = None

        self.category_vector_abs = []
        for cat in self.category_vector:
            self.category_vector_abs.append(abs(cat))
        
        self.category_vector = np.array(self.category_vector)
        self.category_vector_abs = np.array(self.category_vector_abs)

        self.mean_label = np.nan
        self.predicted_label = np.nan

        self.set_probability_function(probability_function)
        
    def set_origin_survey(self,survey) -> None:
        """Sets the origin survey for the item.

        Parameters
        ----------
        survey : pydyn_surv.classes.survey
            The origin survey for the item.
        """
        self.origin_survey = survey

    def get_feauture_vector(self) -> np.ndarray:
        """Returns the feature vector for the item, ie. the category vector.

        Returns
        -------
        np.ndarray
            The feauture vector.
        """
        return self.category_vector

    def set_predicted_label(self,label:float) -> None:
        """Sets the predicted label to the input given.

        Parameters
        ----------
        label : float
            The predicted label for the item.
        """
        self.predicted_label = label

    def get_predicted_label(self) -> float:
        """Gets the predicted label for the item.

        Returns
        -------
        float
            The predicted label for the item.
        """
        return self.predicted_label

    def update_mean_label(self) -> None:
        """Calculates the mean label for the item and assign it to the instance atribute.	
        """
        try:
            self.mean_label = np.mean(self.answer_history)
        except:
            self.mean_label = np.nan
    
    def get_mean_label(self,update:bool = True) -> float:
        """Gets the mean label for the item. If the update parameter is set to True, the mean label is calculated before returning it (default behaviour).

        Parameters
        ----------
        update : bool, optional
            If True, the mean label is calculated before returning it, by default True.
        Returns
        -------
        float
            The mean label for the item.

        """
        if update:
            self.update_mean_label()
        
        return self.mean_label
    
    def set_last_launch(self,n_launch:int) -> None:
        """Sets the last launch for the item.

        Parameters
        ----------
        n_launch : int
            The last launch for the item.
        """
        self.last_launch = n_launch

    def answer(self,answer:float,force:bool = False) -> None:
        """If the answer is in the answer range, it is recorded in the answer history and the launch count is increased by one. If the answer is out of range, it is not recorded unless the force parameter is set to True.

        Parameters
        ----------
        answer : float
            The answer given by the user.
        force : bool, optional
        """
        if self.answer_range[0] <= answer <= self.answer_range[1]:
            self.answer_history.append(answer)
            self.launch_count += 1
            
        else:
            if force:
                Warning('The answer is out of range, but it was recorded anyway.')
                self.answer_history.append(answer)
                self.launch_count += 1
            else:
                Exception('The answer was not recorded because it is out of range. You can force the answer to be recorded by setting the force parameter to True.')


    def get_dataset_pair(self) -> tuple:
        """Gets the dataset pair for training the model using the mean label. The dataset pair contains the pair (category vector, mean label).

        Returns:
            tuple: (category_vector, mean_label)
        """
        return (self.category_vector,self.mean_label)
    
    def get_dataset_history(self) -> list:
        """Gets the dataset histoy for training the model. The dataset history contains the pairs (category vector, answer) from the historic answers.

        Returns
        -------
        list
            The dataset history.
        """
        dataset_history = [(self.category_vector,answer) for answer in self.answer_history]

        return dataset_history

    def probability(self,*args,**kargs) -> float:
        """Returns the probability of the item being launched. This method is a wrapper for the _probability method, which is the one that actually calculates the probability.	
        """
        return self._probability(self,*args,**kargs)
    
    def set_probability_function(self,probability_function:callable) -> None:    
        """Sets the probability function for the item. The probability function must be a callable that returns a float value. It may or may not depend on the item instance, but it must be able to handle the item instance as an argument.

        Parameters
        ----------
        probability_function : callable
            The probability function.
        """
        self._probability = probability_function

    def get_launch_count(self) -> int:
        """Gets the launch count for the item.

        Returns
        -------
        int
            The launch count for the item.
        """
        return self.launch_count
    
    def get_answer_history(self) -> list:
        """Gets the answer history for the item.

        Returns
        -------
        list
            The answer history for the item.
        """
        return self.answer_history
    
    def get_last_launch(self) -> int:
        """Gets the last launch for the item.

        Returns
        -------
        int
            The last launch for the item.
        """
        return self.last_launch
    
    def get_origin_survey(self) -> pydyn_surv.classes.survey:
        """Gets the origin survey for the item.

        Returns
        -------
        pydyn_surv.classes.survey
            The origin survey for the item.
        """
        return self.origin_survey

    def print_values(self):
        """Prints the instance attributes stored values into the terminal.
        """
        print('Question text: ',self.question_text)
        print('Answers text: ',self.answers_text)
        print('Answers values: ',self.answers_values)
        print('Category vector: ',self.category_vector)
        print('Answer range: ',self.answer_range)
        print('Expert value: ',self.expertvalue)
        print('Launch count: ',self.launch_count)
        print('Answer history: ',self.answer_history)
        print('Category vector abs: ',self.category_vector_abs)
        print('Mean label: ',self.mean_label)
        print('Predicted label: ',self.predicted_label)
        print('ID: ',self.id)
        print('')
    