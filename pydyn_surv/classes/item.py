import numpy as np

DEFAULT_PARAMETERS_DICT = {
    'question':'',
    'answers':[],
    'answers_values':[-2,-1,0,1,2],
    'principal_cat_list':[],
    'secondary_cat_list':[],
    'principal_value':1,
    'secondary_value':0.5,
    'answer_range':(-2,2),
    'expert_extra':0
}

class item:
    """ Class that represents an item (question) in the survey, and stores some useful data like the user answer history.

    Returns
    -------
    pydyn_surv.item.item
        Instance of the class pydyn_surv.item.item
    """

    _total_item_count:int = 0
    _total_launch_count:int = 0
    _category_launch_count:np.ndarray = np.array([])
    _category_answer_history:list = []

    categories:list = []
    dimension:int = 0

    statistics_weights = np.array([0.5,-0.5,0.25,-0.25])
    expert_weight = 1
    
    def reset_category_history() -> None:
        """Resets the history of answers for all the categories.
        """
        item._category_launch_count = np.zeros(item.dimension)
        for i in range(item.dimension):
            item._category_answer_history.append([])

    def set_categories(categories:list) -> None:
        """Sets the names of all the categories that can be selected.

        Parameters
        ----------
        categories : list
            A list containing the categories.
        """
        item.categories = categories
        item.dimension = len(categories)
        item.reset_category_history()

    def add_category(category:str,init_count:int = 0) -> None:
        """Adds a category to the list of categories.

        Parameters
        ----------
        category : str
            The name of the category.
        init_count : int, optional
            The amount of times a question within this category has been answered, by default 0.
        """
        item.categories.append(category)
        item.dimension += 1
        item._category_launch_count = np.concatenate(item._category_launch_count,[init_count])
        item._category_answer_history.append([])
    
    def set_statistics_weights(self_std_w:float = 0.5,self_count_w:float = -0.5,cat_std_w:float = 0.25,cat_count_w:float = -0.25) -> None:
        """Sets the weights given for the statistics

        Parameters
        ----------
        self_std_w : float, optional
            The weight for the standard deviation of the item, by default 0.5
        self_count_w : float, optional
            The weight for the amount of thime the item has been answered divided by the total of answers of the user, by default -0.5
        cat_std_w : float, optional
            The weight for the standard deviation of the category (or categories) of the item, by default 0.25
        cat_count_w : float, optional
            The weight for the amount of times a question from the category (or categories) have been answered, by default -0.25
        """
        item.statistics_weights = np.array([self_std_w,self_count_w,cat_std_w,cat_count_w])

    def set_expert_weight(expert_w:float = 1):
        """Sets the weight of the expert punctuation

        Parameters
        ----------
        expert_w : float, optional
            The expert weight amount, by default 1
        """
        item.expert_weight = expert_w


    # def __init__(self,q_text:dict,principal_cat:list,secondary_cat:list,extra_points:float,answer_range:tuple = (-2,2),principal_value:float = 1,secondary_value:float = 0.5) -> None:
    def __init__(self,parameters_dict:dict = DEFAULT_PARAMETERS_DICT):
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
        self.id = item._total_item_count
        item._total_item_count += 1


        try:
            self.question_text = parameters_dict['question']
        except:
            self.question_text = ''
        
        try:
            self.answers_text = parameters_dict['answers']
        except:
            self.answers_text = []
        
        try:
            self.answers_values = parameters_dict['answers_values']
        except:
            self.answers_values = [-2,-1,0,1,2]

        try:
            self.principal_cat_list = parameters_dict['principal_cat_list']
        except:
            self.principal_cat_list = []
        
        try:
            self.secondary_cat_list = parameters_dict['secondary_cat_list']
        except:
            self.secondary_cat_list = []
        
        try:
            principal_value = parameters_dict['principal_value']
        except:
            principal_value = 1

        try:
            secondary_value = parameters_dict['secondary_value']
        except:
            secondary_value = 0.5
        
        try:
            self.answer_range = parameters_dict['answer_range']
        except:
            self.answer_range = (-2,2)
        
        try:
            extra_points = parameters_dict['expert_extra']
        except:
            extra_points = 0

        self.label = None
        self.predicted_label = None
        self.launch_count = 0
        self.answer_history = []
        self.dataset_history = []

        self.principal_abs_cat_list = []
        for cat in self.principal_cat_list:
            self.principal_abs_cat_list.append(abs(cat))

        self.feature_vector = None
        
        self.categoryvector = []
        self.categoryvector_abs = []
        # for i in secondary_cat:
        #     self.categoryvector[i] = secondary_value
        
        for i,j in zip(self.principal_abs_cat_list,self.principal_cat_list):
            self.categoryvector.append(principal_value*(j/i))
            self.categoryvector_abs.append(principal_value)
        
        self.categoryvector = np.array(self.categoryvector)
        self.categoryvector_abs = np.array(self.categoryvector_abs)

        self.expertvalue = extra_points

        self.statisticsvector = [0,0,0,0]
        '''A vector containing the percentage of times question or category is launched and its standard deviation in the order: [std_self,count_self,std_category,count_category]'''
        
    def get_feauture_vector(self) -> np.ndarray:
        """Returns the feature vector for the item, including its statistics vector and expert values.

        Returns
        -------
        np.ndarray
            The feauture vector.
        """
        return np.concatenate([self.categoryvector,self.statisticsvector,[self.expertvalue]])
    
    def update_label(self) -> None:
        """Updates the calculated label of the item based on the mean of the answers of it.
        """
        if self.launch_count > 0:
            self.label = self._get_label(np.mean(self.answer_history))
        else:
            self.label = None

    def set_predicted_label(self,label:float) -> None:
        """Sets the predicted label to the input given.

        Parameters
        ----------
        label : float
            The predicted label for the item.
        """
        self.predicted_label = label

    def _get_statistics(self) -> np.ndarray:
        """Get the standard deviation and count based on the register.

        Returns
        -------
        np.ndarray
            Returns the statistics vector.
        """
        if self.launch_count > 1:
            stdeviation_self = np.std(self.answer_history)
            count_self = self.launch_count/item._total_launch_count
        else:
            stdeviation_self = 0
            if self._total_launch_count != 0:
                count_self = self.launch_count/item._total_launch_count
            else:
                count_self = 0

        stdeviation_category = []
        count_category = []
        for i in self.principal_abs_cat_list:
            i -= 1
            if len(self._category_answer_history[i]) > 1:
                stdeviation_category.append(np.std(self._category_answer_history[i]))

                if item._total_launch_count != 0:
                    count_category.append(self._category_launch_count[i]/item._total_launch_count)


        if len(stdeviation_category) > 0:
            stdeviation_category = np.mean(stdeviation_category)
        else:
            stdeviation_category = 0
        
        if len(count_category) > 0:
            count_category = np.mean(count_category)
        else:
            count_category = 0

        return np.array([stdeviation_self,count_self,stdeviation_category,count_category])

    def update_statistics(self) -> None:
        """Calculates the statistic vector and assign it to the instance atribute.
        """
        self.statisticsvector = self._get_statistics()

    def answer(self,answer:float) -> None:
        """Stores a answer for a given item, in the item history and the category history.

        Parameters
        ----------
        answer : float
            The answer given by the user.
        """
        if self.answer_range[0] <= answer <= self.answer_range[1]:
            self.answer_history.append(answer)
            self.launch_count += 1
            item._total_launch_count += 1
            item._category_launch_count += self.categoryvector_abs

            self.dataset_history.append((self.categoryvector,answer))

            # for i,j in zip(self.principal_abs_cat_list,self.principal_cat_list):
            #     item._category_answer_history[i-1].append(answer*(j/i))

            for i in range(self.dimension):
                sign = self.principal_cat_list[i]/self.principal_abs_cat_list[i]
                item._category_answer_history[i].append(answer*sign)
            
        else:
            Warning('The answer was not recorded because it is out of range.')


    def _get_label(self,answer:float) -> float:
        """Generates a label based on the answer and the statistics.

        Parameters
        ----------
        answer : float
            The answer for calculating the label

        Returns
        -------
        float
            The label for the given answer (if the statistic weight vector is full of zeros the label is equal to the answer).
        """
        stat_label = self.statistics_weights.dot(self.statisticsvector)
        expert_label = self.expert_weight * self.expertvalue
        label = answer + stat_label + expert_label
        # print(answer,stat_label,expert_label)
        return label
    
    def print_values(self):
        """Prints the instance attributes stored values into the terminal.
        """
        print('\nTOTAL:\n------')
        print('Total item count: {}'.format(item._total_item_count))
        print('Total launch count: {}'.format(item._total_launch_count))
        print('Statistics weights: {}'.format(item.statistics_weights))
        print('Expert weight: {}'.format(item.expert_weight))
        print('\nCATEGORY:\n---------')
        print('Categories: {}'.format(item.categories))
        print('Dimension: {}'.format(item.dimension))
        print('Category launch count: {}'.format(item._category_launch_count))
        print('Category answer history: {}'.format(item._category_answer_history))
        print('\nITEM:\n-----')
        print('id: {}'.format(self.id))
        print('Question: {}'.format(self.question_text))
        print('Answers: {}'.format(self.answers_text))
        print('Launch count:{}'.format(self.launch_count))
        print('Answer history: {}'.format(self.answer_history))
        print('Answer range: {}'.format(self.answer_range))
        print('Calcualted label: {}'.format(self.label))
        print('Predicted label: {}'.format(self.predicted_label))
        print('Principal_category_list: {}'.format(self.principal_cat_list))
        print('Principal_abs_category_list: {}'.format(self.principal_abs_cat_list))
        print('Category vector: {}'.format(self.categoryvector))
        print('Category vector abs: {}'.format(self.categoryvector_abs))
        print('Statistics vector: {}'.format(self.statisticsvector))
        print('Expert value: {}'.format(self.expertvalue))

    def get_dataset_pair(self) -> tuple:
        """Returns a pair with the full feature vector (categoryvector, statisticsvector, expertvector) and the label from the answer mean plus the statistics and expert fixed weights dot its vectors.

        Returns:
            tuple: (full feature_vector,calculated label)
        """
        if self.launch_count > 0:
            self.update_all()

            return (self.feature_vector,self.label)

        else:
            return None
    
    def get_dataset_history(self) -> list:
        """Gets the dataset histoy for training the model. The dataset history contains the pairs (category vector, answer) from the historic answers.

        Returns
        -------
        list
            The dataset history.
        """
        return self.dataset_history
    
    def update_feature_vector(self) -> None:
        """Updates the feture vector for the item.
        """
        self.feature_vector = self.get_feauture_vector()

    def update_all(self) -> None:
        """Executes all the "update" functions.
        """
        self.update_statistics()
        self.update_feature_vector()
        self.update_label()
