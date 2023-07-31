import numpy as np
from .item import item as item
from . import funcs
from .other_classes import pydyn_surv_list
from random import choices as rnd_choices

LAUNCH_FORMAT = [
    '-----------------------------------------------------------\n {}',
    '    {}) {}',
    '-----------------------------------------------------------']
"""
List containing the strings with the format to display an intem in the terminal. The first string is the format for the item's statement, the second is the format for the item's answer number and the third is the format for the closing.
"""


class survey:

    instances = []
    instances_dict = dict()
    
    def get_total_launches(*args) -> int:
        """Returns the total amount of launches across all surveys.

        Returns
        -------
        int
            The total amount of launches across all surveys.
        """
        total = 0
        for survey_ in survey.instances:
            total += survey_.launch_count
        return total

    def __init__(self,items:list = [],name:str = '',init_training_dataset:list = None,w:np.ndarray = None,predictor = funcs.PREDICTOR,launch_format = LAUNCH_FORMAT,categories:list = [],origin:list = [],offspring:list = [],origin_category = None, condition_function:callable = funcs.FUNC_TRUE, probability_function:callable = funcs.FUNC_TRUE, train_function:callable = funcs.TRAIN_FUNCTION) -> None:
        """Creates a survey instance.
        
        Parameters
        ----------
        items : list, optional
            The list of items that the survey will contain, by default []. The items can be added later with the methods `set_items` and `add_item`. The items could be pydyn_surv.item.item instances or dicts with the parameters to create them.

        name : str, optional    
            The name of the survey, by default ''. It is also used to set the origin category name in case it is not set with the parameter `origin_category`.
        init_training_dataset : list, optional
            The initial trainin dataset in case, by default None.
        w : np.ndarray, optional
            The initial weight vector, by default None. If it is not set, it will be set to a vector of zeros with the same dimension as the items.
        predictor : callable, optional
            The predictor function, by default `pydyn_surv.funcs.PREDICTOR`. It can be changed later with the method `set_predictor`.
        launch_format : list, optional
            The format to display the items in the terminal, by default `pydyn_surv.survey.LAUNCH_FORMAT`.
        categories : list, optional
            The list of categories that the survey will contain, by default []. The categories can be added later with the methods `set_categories` and `add_category`.
        origin : list, optional
            The list of surveys that are the origin of the survey, by default []. The origin can be changed later with the method `set_origin`.
        offspring : list, optional
            The list of surveys that are the offspring of the survey, by default []. The offspring can be changed later with the method `set_offspring`.
        origin_category : str, optional
            The name of the origin category, by default None. If it is not set, it will be set to the name of the survey.
        condition_function : callable, optional
            The condition function, by default `pydyn_surv.funcs.FUNC_TRUE`. It can be changed later with the method `set_condition_function`.
        probability_function : callable, optional
            The probability function, by default `pydyn_surv.funcs.FUNC_TRUE`. It can be changed later with the method `set_probability_function`.
        train_function : callable, optional
            The train function, by default `pydyn_surv.funcs.TRAIN_FUNCTION`. It can be changed later with the method `set_train_function`.

        Returns
        -------
        pydyn_surv.survey.survey
            The survey instance.
        """
        survey.instances.append(self)
        self.name = name
        self.training_dataset = []
        self.init_training_dataset = init_training_dataset
        self.predictor = predictor
        self.launch_format = launch_format
        self.item_by_id = {}

        self.launch_count:int = 0
        self.category_launch_count:np.ndarray = np.array([])
        self.category_answer_history:list = []
        self.dimension:int = 0

        self.set_categories(categories)
        self.set_items(items)
        self.predicted_item_labels = np.full(self.item_amount,np.nan)
        self.calculated_item_labels = np.full(self.item_amount,np.nan)

        self.w_history = []

        if w is None:
            t_w = np.full(self.dimension,0)
            self.set_w(t_w)
        else:
            self.set_w(w)

        self.set_condition_function(condition_function)
        self.set_probability_function(probability_function)
        self.set_train_function(train_function)

        if not origin_category is None:
            self.set_origin_category(origin_category)
        else:
            self.set_origin_category(name)

        self.label = np.nan

        self.set_origin(origin)
        self.set_offspring(offspring)

        self.last_condition_state = None

        # print(self.name)
        survey.instances_dict[self.name] = self

    def set_origin(self,origin:list) -> None:
        """Sets the origin for the survey.

        Parameters
        ----------
        origin : list
            A list containing the origin surveys, which must be of type survey.
        """
        if origin is None:
            origin = pydyn_surv_list()
        if not isinstance(origin,pydyn_surv_list):
            if not isinstance(origin,list):
                origin = pydyn_surv_list([origin])
            else:
                origin = pydyn_surv_list(origin)
        
        if self in origin:
            origin.remove(self)
            print(Warning('Warning: The survey cannot be its own origin. It has been removed from the origin list.'))
            

        self.origin = origin

        for srv in self.origin:
            if self not in srv.offspring:
                # print('Adding offspring to the origin survey.')	
                srv.add_offspring(self)
    
    def set_offspring(self,offspring:list) -> None:
        """Sets the offspring for the survey.

        Parameters
        ----------
        offspring : list
            A list containing the offspring surveys, which must be of type survey.
        """
        if not isinstance(offspring,pydyn_surv_list):
            if not isinstance(offspring,list):
                offspring = pydyn_surv_list([offspring])
            else:
                offspring = pydyn_surv_list(offspring)
        
        if self in offspring:
            offspring.remove(self)
            print(Warning('Warning: The survey cannot be its own offspring. It has been removed from the offspring list.'))

        self.offspring = offspring

        for srv in self.offspring:
            if self not in srv.origin:
                srv.add_origin(self)
    
    def add_origin(self,origin) -> None:
        """Adds an origin survey to the survey.

        Parameters
        ----------
        origin : pydyn_surv.survey.survey
            The origin survey to be added.
        """
        if origin == self:
            raise ValueError('A survey cannot be its own origin. You can create a copy of the survey and set it as the origin.')

        if origin not in self.origin:
            self.origin.append(origin)
        if self not in origin.offspring:
            # print('Adding offspring to the origin survey.')
            origin.add_offspring(self)
        
    
    def add_offspring(self,offspring) -> None:
        """Adds an offspring survey to the survey.

        Parameters
        ----------
        offspring : pydyn_surv.survey.survey
            The offspring survey to be added.
        """
        if offspring == self:
            raise ValueError('A survey cannot be its own offspring. You can create a copy of the survey and set it as the offspring.')

        if offspring not in self.offspring:
            self.offspring.append(offspring)
        if self not in offspring.origin:
            # print('Adding origin to the offspring survey.')
            offspring.add_origin(self)

    def set_origin_category(self,category) -> None:
        """Sets the origin category for the survey.

        Parameters
        ----------
        category : list|str
            The origin category for the survey.
        """
        if not isinstance(category,list):
            self.origin_category = [category]
        else:
            self.origin_category = category

    def set_items(self,items:list) -> None:
        """Sets the items for the survey.

        Parameters
        ----------
        items : list
            A list containing the items, which can be of type item or dict.
        """

        if all(isinstance(item_,item) for item_ in items):
            self.items = pydyn_surv_list(items)
            for i in range(len(self.items)): 
                if self.items[i].id is None:
                    self.items[i].id = i
                if self.items[i].id in self.item_by_id.keys():
                    raise ValueError('More than one item with the same id.')
                else:
                    self.item_by_id[self.items[i].id] = self.items[i]
                
                self.items[i].set_origin_survey(self)
                
            self.item_amount = len(self.items)

        elif all(isinstance(item_,dict) for item_ in items):
            self.items = pydyn_surv_list([])
            for i in range(len(items)):
                temp_item = item(items[i],i,self)
                self.items.append(temp_item)
                self.item_by_id[temp_item.id] = self.items[-1]
            self.item_amount = len(self.items)
        else:
            raise TypeError('All items must be of type item or dict.')

    def add_item(self,item_:item) -> None:
        """Adds an item to the survey.

        Parameters
        ----------
        item_ : item
            The item to be added.
        """
        if item_.id is None:
            item_.id = self.item_amount
        elif item_.id in self.item_by_id.keys():
            raise ValueError('An item with the same id already exists.')
        
        self.items.append(item_)
        self.item_by_id[item_.id] = self.items[-1]
        self.item_amount += 1

    def reset_category_history(self) -> None:
        """Resets the history of answers for all the categories.
        """
        self.category_launch_count = np.zeros(self.dimension)
        for i in range(self.dimension):
            self.category_answer_history.append([])

    def set_categories(self,categories:list) -> None:
        """Sets the names of all the categories that can be selected.

        Parameters
        ----------
        categories : list
            A list containing the categories.
        """
        self.categories = categories
        self.dimension = len(categories)
        self.reset_category_history()

    def add_category(self,category:str,init_count:int = 0) -> None:
        """Adds a category to the list of categories.

        Parameters
        ----------
        category : str
            The name of the category.
        init_count : int, optional
            The amount of times a question within this category has been answered, by default 0.
        """
        self.categories.append(category)
        self.dimension += 1
        self.category_launch_count = np.concatenate(item.category_launch_count,[init_count])
        self.category_answer_history.append([])
    
    def get_training_dataset(self) -> list:
        """Returns the training dataset of the survey.
        Returns
        -------
        training_dataset : list
            A list containing the training dataset. Each element is a tuple containing the feature vector and the label.
        """
        if isinstance(self.init_training_dataset,list):
            training_dataset = self.init_training_dataset
        else:
            training_dataset = []

        for item_ in self.items:
            item_:item
            item_dataset_history = item_.get_dataset_history()
            training_dataset += item_dataset_history
        
        return training_dataset
    
    def get_weight(self) -> np.ndarray:
        """Returns the current weight vector of the survey.
        Returns
        -------
        w : np.ndarray
            The current weight vector of the survey.
        """
        return self.w

    def update_training_dataset(self) -> None:
        """Updates the training dataset of the survey.
        """
        self.training_dataset = self.get_training_dataset()

    def get_feature_vectors(self) -> list:
        """Returns the feature vectors of the items in the survey.
        Returns
        -------
        feature_vectors : list
            A list containing the feature vectors of the items in the survey.
        """
        feature_vectors = []
        for item_ in self.items:
            # item_:item
            fv = item_.get_feauture_vector()
            feature_vectors.append(fv)
        
        return feature_vectors

    def get_predicted_labels(self,w:np.ndarray,predictor) -> list:
        """Returns the predicted labels of the items in the survey.
        Parameters
        ----------
        w : np.ndarray
            The weight vector.
        predictor : function
            The predictor function.
        Returns
        -------
        predicted_labels : list
            A list containing the predicted labels of the items in the survey.
        """
        predicted_labels = []
        for item_ in self.items:
            item_:item
            x = item_.get_feauture_vector()
            label = predictor(w,x)
            predicted_labels.append(label)
            item_.set_predicted_label(label)
        
        return predicted_labels

    def get_calculated_labels(self) -> list:
        """Returns the calculated labels of the items in the survey.
        Returns
        -------
        calculated_labels : list
            A list containing the calculated labels of the items in the survey.
        """
        calculated_labels = []
        for item_ in self.items:
            item_:item
            item_.update_mean_label()
            label = item_.get_mean_label()
            calculated_labels.append(label)
        
        return calculated_labels
    
    def update_predicted_labels(self) -> None:
        """Updates the predicted labels of the items in the survey via `get_predicted_labels` method with the survey's weight vector and predictor function.
        """
        self.predicted_item_labels = self.get_predicted_labels(self.w,self.predictor)
    
    def update_calculated_labels(self) -> None:
        """Updates the calculated labels of the items in the survey via `get_calculated_labels` method.
        """
        self.calculated_item_labels = self.get_calculated_labels()
    
    def update_all_labels(self) -> None:
        """Updates the predicted and calculated labels of the items in the survey.
        """
        self.update_calculated_labels()
        self.update_predicted_labels()

    def set_w(self,w:np.ndarray) -> None:
        """Sets the weight vector of the survey.
        Parameters
        ----------
        w : np.ndarray
            The weight vector.
        """
        self.w = w
        self.w_history.append(w)
        # print('Weight setted to: {}'.format(self.w))
    
    def set_predictor(self,predictor) -> None:
        """Sets the predictor function of the survey.
        Parameters
        ----------
        predictor : function
            The predictor function.
        """
        self.predictor = predictor

    def print_items(self) -> None:
        """Prints the items in the survey.
        """
        for item_ in self.items:
            item_:item
            print('{}] {}'.format(item_.id, item_.question_text))
    
    def print_item_info(self,item_:item) -> None:
        """Prints the information of an item in the survey.
        Parameters
        ----------
        item_ : item
            The item to print the information of.
        """
        if item_ in self.items:
            item_.print_values()
        else:
            raise ValueError('Item {} is not in survey {}.'.format(item_.id,self.name))
    
    def launch_random(self,random_func:callable=rnd_choices,all_zero_to_one=False) -> tuple:
        """Returns a random item in the survey.
        Parameters
        ----------
        random_func : callable, optional
            The function to use to randomly select an item, by default `random.choices`.
        all_zero_to_one : bool, optional
            If `True`, if the probabilities of all the items are equal to zero, it turns them to one, by default False.
        Returns
        -------
        item_ : pydyn_surv.item.item
            The randomly selected item.
        item_.question_text : str
            The question text of the randomly selected item.
        item_.answers_text : list
            The answers text of the randomly selected item.
        item_.answers_values : list
            The answers values of the randomly selected item.
        """
        # self.update_all()
        items_ = self.get_items()
        item_ = random_func(items_,items_.probabilities(all_zero_to_one=all_zero_to_one))[0]

        return item_,item_.question_text, item_.answers_text, item_.answers_values

    def launch_on_terminal(self,item_:item,force_answer:bool = False) -> None:
        """Launches an item on the terminal.
        Parameters
        ----------
        item_ : item
            The item to launch.
        force_answer : bool, optional
            If `True`, it forces the answering without checking the input, by default False.
        """
        # self.update_all()
        if item_ not in self.items:
            raise ValueError('Item {} is not in survey {}.'.format(item_.id,self.name))

        print(self.launch_format[0].format(item_.question_text))
        for answ_index in range(len(item_.answers_text)):
            print(self.launch_format[1].format(answ_index + 1,item_.answers_text[answ_index]))
        # print(self.launch_format[2])

        r = input('                                                R: ')
        print(self.launch_format[2])

        # try:
        r = int(r)
        ans_val = item_.answers_values[r-1]
        item_.answer(ans_val,force_answer)
        # item_.set_last_launch(self.launch_count)

        # self.launch_count += 1
        # self.category_launch_count += item_.category_vector_abs
        
        # for i in range(self.dimension):
        #     if item_.category_vector[i]:
        #         sign = item_.category_vector[i]/item_.category_vector_abs[i]
        #         self.category_answer_history[i].append(ans_val*sign)
            

        # except:
        #     print('\n\n! --> Not a valid answer, please retry.\n')
        #     self.launch_item(item_,force_answer)

    def get_launch_count(self) -> int:
        """Gets the launch count of the survey.
        
        Returns
        -------
        int
            The launch count for the survey.
        """
        return self.launch_count
    
    def get_category_launch_count(self) -> np.ndarray:
        """Gets the launch count of each category.
        
        Returns
        -------
        np.ndarray
            The launch count for each category.
        """
        return self.category_launch_count
    
    def get_category_answer_history(self) -> list:
        """Gets the answer history of each category.
        
        Returns
        -------
        list
            The answer history for each category.
        """
        return self.category_answer_history

    def print_info(self,print_items:bool = False) -> None:
        """Prints the information of the survey.
        Parameters
        ----------
        print_items : bool, optional
            If `True`, it prints the items in the survey, by default False.
        """
        # self.name = name
        # self.training_dataset = init_training_dataset
        # self.item_amount = len(items)
        # self.predicted_item_labels = np.zeros(self.item_amount)
        # self.w = w
        # self.predictor = predictor
        # self.launch_format = launch_format
        print('\nSURVEY INFO:\n------------')
        print('Survey name: {}'.format(self.name))
        print('Categories: {}'.format(self.categories))
        print('Training dataset:')
        print(*('   {} -> {}\n'.format(x,y) for x,y in self.training_dataset),sep='')
        print('Item amount: {}'.format(self.item_amount))
        print('Predicted item labels: {}'.format(self.predicted_item_labels))
        print('Probabilities: {}'.format(self.get_items().probabilities()))
        print('Calculated item labels: {}'.format(self.calculated_item_labels))
        print('Weight: {}'.format(self.w))
        print('Predictor: {}'.format(self.predictor))
        print('Origin: {}'.format([o.name for o in self.origin]))
        print('Origin category: {}'.format(self.origin_category))
        print('Offspring: {}'.format([o.name for o in self.offspring]))
        print('Weight history: {}'.format(self.w_history))
        if print_items:
            print('\nITEMS:\n------')
            self.print_items()

    def update_all(self,exclude_calculated_labels:bool = False) -> None:
        """Updates all the information of the survey.
        Parameters
        ----------
        exclude_calculated_labels : bool, optional
            If `True`, it excludes the calculated labels from the update, by default False.
        """
        self.update_training_dataset()
        if exclude_calculated_labels:
            self.update_predicted_labels()
        else:
            self.update_all_labels()

    def get_self_label(self):
        """Gets the predicted label of a survey based on the origin category and the origin.
        Returns
        -------
        label : float
            The label of the survey.
        """

        labels = []

        # if not isinstance(self.origin_category,list):
        #     for origin in self.origin:
        #         cat_index = origin.categories.index(self.origin_category)
        #         feature_vector = np.zeros(origin.dimension)
        #         feature_vector[cat_index] = 1

        #         label = origin.predictor(origin.w,feature_vector)
        #         labels.append(label)
        # else:
        for origin in self.origin:
            feature_vector = np.zeros(origin.dimension)
            for cat in self.origin_category:
                cat_index = origin.categories.index(cat)
                feature_vector[cat_index] = 1

            label = origin.predictor(origin.w,feature_vector)
            labels.append(label)
        
        try:
            self.label = np.nanmean(labels)
        except:
            Warning('No label for survey {}.'.format(self.name))
            self.label = np.nan

        return self.label

    def condition(self,*args,**kwargs) -> bool:
        """Returns True if the condition for launching the survey is met, False otherwise. This method is a wrapper for the _condition method, which is setted by the set_condition_function method. It also stores the last condition state in the last_condition_state attribute.
        Parameters
        ----------
        *args : list
            The arguments for the condition function.
        **kwargs : dict
            The keyword arguments for the condition function.
        Returns
        -------
        condition : bool
            True if the condition for launching the survey is met, False otherwise.
        """
        self.last_condition_state = self._condition(self,*args,**kwargs)
        return self.last_condition_state
    
    def set_condition_function(self,condition_function:callable) -> None:
        """Sets the condition function for the survey. The condition function must be a callable that returns a boolean value. It may or may not depend on the survey instance, but it must be able to handle the survey instance as an argument.
        Parameters
        ----------
        condition_function : callable
            The condition function.
        """
        self._condition = condition_function

    def probability(self,*args,**kargs) -> float:
        """Returns the probability of the survey being launched. This method is a wrapper for the _probability method, which is the one that actually calculates the probability.
        Parameters
        ----------
        *args : list
            The arguments for the probability function.
        **kwargs : dict
            The keyword arguments for the probability function.
        """
        return self._probability(self,*args,**kargs)
    
    def set_probability_function(self,probability_function:callable) -> None:    
        """Sets the probability function for the survey. The probability function must be a callable that returns a float value. It may or may not depend on the survey instance, but it must be able to handle the survey instance as an argument.

        Parameters
        ----------
        probability_function : callable
            The probability function.
        """
        self._probability = probability_function
    
    def set_probability_function_of_items(self,probability_function:callable) -> None:
        """Sets the probability function for the items of the survey. The probability function must be a callable that returns a float value. It may or may not depend on the survey instance, but it must be able to handle the survey instance as an argument.
        
        Parameters
        ----------
        probability_function : callable
            The probability function.
        """
        for item_ in self.items:
            item_.set_probability_function(probability_function)

    def train(self,*args,**kwargs) -> np.ndarray:
        """Trains the survey. This method is a wrapper for the _train method, which is the one that actually trains the survey.`
        Parameters
        ----------
        *args : list
            The arguments for the train function.
        **kwargs : dict
            The keyword arguments for the train function.
        """
        self.update_all()
        trained_w = self._train(self,*args,**kwargs)
        self.set_w(trained_w)
    
    def set_train_function(self,train_function:callable) -> None:
        """Sets the train function for the survey. The train function must be a callable that returns a width. It must be able to handle the survey instance as an argument.

        Parameters
        ----------
        train_function : callable
            The train function.
        """
        self._train = train_function

    def get_surveys(self,force:bool = False, force_offspring = False,*args,**kwargs) -> pydyn_surv_list:
        """Returns a list with the surveys avaiable to be launched from the current survey, e.i. the current survey and the offspring surveys that meet the condition for launching. If the force argument is set to True, it returns the offspring surveys that meet the condition even if the condition is not met for the current survey.
        Parameters
        ----------
        force : bool, optional
            If `True`, it returns the offspring surveys that meet the condition even if the condition is not met for the current survey, by default False.
        force_offspring : bool, optional
            Represents the force state for the offspring surveys, since this is a recursive method, by default False.
        *args : list
            The arguments for the condition function.
        **kwargs : dict
            The keyword arguments for the condition function.
        Returns
        -------
        surveys : pydyn_surv_list
            The list of surveys avaiable to be launched from the current survey.
        """
        if self.condition(*args,**kwargs) or force:
            if any(self.get_items().probabilities()):
                surveys = pydyn_surv_list([self])
            else:
                surveys = pydyn_surv_list([])
                
            for surv in self.offspring:
                # print(surv.name)
                offspring_survs = surv.get_surveys(force_offspring,force_offspring,*args,**kwargs)
                surveys += offspring_survs
        else:
            surveys = pydyn_surv_list([])
        
        return surveys


    # def get_items and def get_items_probabilities: to be implemented

    def get_items(self) -> pydyn_surv_list:
        """Returns a list with the items of the survey.
        Returns
        -------
        items : pydyn_surv_list
            The list of items of the survey.
        """
        return self.items


    def get_weight_history(self) -> list:
        """Returns a list with the weight history of the survey.
        Returns
        -------
        w_history : list
            The list of weight history of the survey.
        """
        
        return self.w_history
