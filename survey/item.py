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

    _total_item_count:int = 0
    _total_launch_count:int = 0
    _category_launch_count:np.ndarray = np.array([])
    _category_answer_history:list = []

    categories:list = []
    dimension:int = 0

    statistics_weights = np.array([0.5,-0.8,0.05,-0.2])
    expert_weight = 1
    
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
    
    def set_statistics_weights(self_std_w:float = 0.5,self_count_w:float = -0.8,cat_std_w:float = 0.05,cat_count_w:float = -0.2) -> None:
        item.statistics_weights = np.array([self_std_w,self_count_w,cat_std_w,cat_count_w])


    # def __init__(self,q_text:dict,principal_cat:list,secondary_cat:list,extra_points:float,answer_range:tuple = (-2,2),principal_value:float = 1,secondary_value:float = 0.5) -> None:
    def __init__(self,parameters_dict:dict = DEFAULT_PARAMETERS_DICT) -> None:
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

        self.principal_abs_cat_list = []
        for cat in self.principal_cat_list:
            self.principal_abs_cat_list.append(abs(cat))

        self.feature_vector = None
        
        self.categoryvector = np.zeros(self.dimension)
        self.categoryvector_abs = np.zeros(self.dimension)
        # for i in secondary_cat:
        #     self.categoryvector[i] = secondary_value
        
        for i,j in zip(self.principal_abs_cat_list,self.principal_cat_list):
            self.categoryvector[i-1] = principal_value*(j/i)
            self.categoryvector_abs[i-1] = principal_value

        self.expertvalue = extra_points

        self.statisticsvector = [0,0,0,0]
        '''A vector containing the percentage of times question or category is launched and its standard deviation in the order: [std_self,count_self,std_category,count_category]'''
        
    def get_feauture_vector(self) -> np.ndarray:
        return np.concatenate([self.categoryvector,self.statisticsvector,[self.expertvalue]])
    
    def update_label(self) -> None:
        self.label = self._get_label(np.mean(self.answer_history))

    def set_predicted_label(self,label) -> None:
        self.predicted_label = label

    def _get_statistics(self) -> np.ndarray:
        if self.launch_count > 1:
            stdeviation_self = np.std(self.answer_history)
            count_self = self.launch_count/item._total_launch_count
        else:
            stdeviation_self = 0
            count_self = self.launch_count/item._total_launch_count

        stdeviation_category = []
        count_category = []
        for i in self.principal_abs_cat_list:
            i -= 1
            stdeviation_category.append(np.std(self._category_answer_history[i]))
            count_category.append(self._category_launch_count[i]/item._total_launch_count)
        stdeviation_category = np.mean(stdeviation_category)
        count_category = np.mean(count_category)

        # print(stdeviation_self,count_self,stdeviation_category,count_category)

        return np.array([stdeviation_self,count_self,stdeviation_category,count_category])

    def update_statistics(self) -> None:
        self.statisticsvector = self._get_statistics()

    def answer(self,answer) -> None:
        if self.answer_range[0] <= answer <= self.answer_range[1]:
            self.answer_history.append(answer)
            self.launch_count += 1
            item._total_launch_count += 1
            item._category_launch_count += self.categoryvector_abs

            for i,j in zip(self.principal_abs_cat_list,self.principal_cat_list):
                item._category_answer_history[i-1].append(answer*(j/i))
            
        else:
            Warning('The answer was not recorded because it is out of range.')


    def _get_label(self,answer):
        stat_label = self.statistics_weights.dot(self.statisticsvector)
        expert_label = self.expert_weight * self.expertvalue
        label = answer + stat_label + expert_label
        # print(answer,stat_label,expert_label)
        return label
    
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
        print('Question: {}'.format(self.question_text))
        print('Answers: {}'.format(self.answers_text))
        print('Launch count:{}'.format(self.launch_count))
        print('Answer history: {}'.format(self.answer_history))
        print('Answer range: {}'.format(self.answer_range))
        print('Label: {}'.format(self.label))
        print('Principal_category_list: {}'.format(self.principal_cat_list))
        print('Principal_abs_category_list: {}'.format(self.principal_abs_cat_list))
        print('Category vector: {}'.format(self.categoryvector))
        print('Category vector abs: {}'.format(self.categoryvector_abs))
        print('Statistics vector: {}'.format(self.statisticsvector))
        print('Expert value: {}'.format(self.expertvalue))

    def get_dataset_pair(self) -> tuple:
        if self.launch_count > 0:
            self.update_all()

            return (self.feature_vector,self.label)

        else:
            return None
    
    def update_feature_vector(self) -> None:
        self.feature_vector = self.get_feauture_vector()

    def update_all(self) -> None:
        self.update_statistics()
        self.update_feature_vector()
        self.update_label()
