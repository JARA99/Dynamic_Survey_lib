import numpy as np
from statistics import variance as var

class item:

    _total_item_count:int = 0
    _total_launch_count:int = 0
    _category_launch_count:np.ndarray = np.array([])
    _category_answer_history:list = []

    categories:list = []
    dimension:int = 0
    
    def reset_category_history() -> None:
        item._category_launch_count = np.zeros(item.dimension)
        for i in range(item.dimension):
            item._category_answer_history.append([])

    def set_categories(categories:list) -> None:
        item.categories = categories
        item.dimension = len(categories)
        item.reset_category_history()

    def add_category(category:str,init_count:int = 0) -> None:
        item.categories.append(category)
        item.dimension += 1
        item._category_launch_count = np.concatenate(item._category_launch_count,[init_count])
        item._category_answer_history.append([])

    def __init__(self,q_text:dict,principal_cat:list,secondary_cat:list,extra_points:float,answer_range:tuple = (-2,2),principal_value:float = 1,secondary_value:float = 0.5) -> None:
        item._total_item_count += 1
        self.id = item._total_item_count
        self.text = q_text
        self.launch_count = 0
        self.answer_history = []
        self.answer_range = answer_range
        self.label = None
        self.principal_cat_list = principal_cat
        # self.secondary_cat_list = secondary_cat
        
        self.categoryvector = np.zeros(self.dimension)
        # for i in secondary_cat:
        #     self.categoryvector[i] = secondary_value
        
        for i in principal_cat:
            self.categoryvector[i] = principal_value

        self.expertvector = [extra_points]

        self.statisticsvector = [0,0,0,0]
        '''A vector containing the percentage of times question or category is launched and variance in the order: [var_self,count_self,var_category,count_category]'''
        
    def get_feauture_vector(self) -> np.ndarray:
        return np.concatenate([self.categoryvector,self.expertvector,self.statisticsvector])

    def calculate_statistics(self) -> None:
        variance_self = var(self.answer_history)
        count_self = self.launch_count/item._total_launch_count

        variance_category = []
        count_category = []
        for i in self.principal_cat_list:
            variance_category.append(var(self._category_answer_history[i]))
            count_category.append(self._category_launch_count[i]/item._total_launch_count)
        variance_category = np.mean(variance_category)
        count_category = np.mean(count_category)

        # print(variance_self,count_self,variance_category,count_category)

        self.statisticsvector = np.array([variance_self,count_self,variance_category,count_category])
        # print(self.statisticsvector)


    def answer(self,answer) -> None:
        if self.answer_range[0] <= answer <= self.answer_range[1]:
            self.answer_history.append(answer)
            self.launch_count += 1
            item._total_launch_count += 1
            item._category_launch_count += self.categoryvector

            for i in self.principal_cat_list:
                item._category_answer_history[i].append(answer)


    def _get_label(self,answer,statistics_weight):
        label = answer + statistics_weight.dot(self.statisticsvector)
    
    def print_values(self):
        print('\nTOTAL:\n------')
        print('Total item count: {}'.format(item._total_item_count))
        print('Total launch count: {}'.format(item._total_launch_count))
        print('\nCATEGORY:\n---------')
        print('Categories: {}'.format(item.categories))
        print('Dimension: {}'.format(item.dimension))
        print('Category launch count: {}'.format(item._category_launch_count))
        print('Category answer history: {}'.format(item._category_answer_history))
        print('\nITEM:\n-----')
        print('id: {}'.format(self.id))
        print('Question: {}'.format(self.text))
        print('Launch count:{}'.format(self.launch_count))
        print('Answer history: {}'.format(self.answer_history))
        print('Answer range: {}'.format(self.answer_range))
        print('Label: {}'.format(self.label))
        print('Principal_category_list: {}'.format(self.label))
        print('Category vector: {}'.format(self.categoryvector))
        print('Statistics vector: {}'.format(self.statisticsvector))
        print('Expert vector: {}'.format(self.expertvector))
