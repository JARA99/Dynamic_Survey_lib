import numpy as np
from .item import item as item

LAUNCH_FORMAT = ['-----------------------------------------------------------\n {}','    {}) {}','-----------------------------------------------------------']

class survey:

    def __init__(self,items:list = [],name:str = '',init_training_dataset:list = None,w:np.ndarray = None,predictor = None,launch_format = LAUNCH_FORMAT) -> None:
        self.name = name
        self.training_dataset = init_training_dataset
        self.item_amount = len(items)
        self.predicted_item_labels = np.zeros(self.item_amount)
        self.w = w
        self.predictor = predictor
        self.launch_format = launch_format


        if all(isinstance(item_,item) for item_ in items):
            self.items = items

        elif all(isinstance(item_,dict) for item_ in items):
            self.items = []
            for item_ in items:
                temp_item = item(item_)
                self.items.append(temp_item)

    def add_item(self,item_:item) -> None:
        self.items.append(item_)
        self.item_amount += 1
    
    def get_training_dataset(self) -> list:
        training_dataset = []
        for item_ in self.items:
            item_:item
            item_dataset_history = item_.get_dataset_history()
            training_dataset += item_dataset_history
        
        return training_dataset

    def update_training_dataset(self) -> None:
        self.training_dataset = self.get_training_dataset()

    def get_feature_vectors(self) -> None:
        feature_vectors = []
        for item_ in self.items:
            # item_:item
            fv = item_.get_feauture_vector()
            feature_vectors.append(fv)
        
        return feature_vectors

    def get_predicted_labels(self,w:np.ndarray,predictor) -> list:
        predicted_labels = []
        for item_ in self.items:
            item_:item
            x = item_.get_feauture_vector()
            label = predictor(w,x)
            predicted_labels.append(label)
            item_.set_predicted_label(label)
        
        return predicted_labels
    
    def update_labels(self) -> None:
        self.predicted_item_labels = self.get_predicted_labels(self.w,self.predictor)

    def set_w(self,w:np.ndarray) -> None:
        self.w = w
    
    def set_predictor(self,predictor) -> None:
        self.predictor = predictor

    def print_items(self) -> None:
        for item_ in self.items:
            item_:item
            print('{}] {}'.format(item_.id, item_.question_text))
    
    def print_item_info(self,index) -> None:
        self.items[index].print_values()
    

    def launch_item(self,index) -> None:
        item_:item
        item_ = self.items[index]
        print(self.launch_format[0].format(item_.question_text))
        for answ_index in range(len(item_.answers_text)):
            print(self.launch_format[1].format(answ_index + 1,item_.answers_text[answ_index]))
        # print(self.launch_format[2])

        r = input('                                                R: ')
        print(self.launch_format[2])
        r = int(r)

        # try:
        ans_val = item_.answers_values[r-1]
        item_.answer(ans_val)
        # except:
        #     print('\n\n! --> Not a valid answer, please retry.\n')
        #     self.launch_item(index)

    def print_info(self) -> None:
        # self.name = name
        # self.training_dataset = init_training_dataset
        # self.item_amount = len(items)
        # self.predicted_item_labels = np.zeros(self.item_amount)
        # self.w = w
        # self.predictor = predictor
        # self.launch_format = launch_format
        print('Survey name: {}'.format(self.name))
        print('Training dataset:')
        print(*('   {} -> {}\n'.format(x,y) for x,y in self.training_dataset),sep='')
        print('Item amount: {}'.format(self.item_amount))
        print('Predicted item labels: {}'.format(self.predicted_item_labels))
        print('Weight: {}'.format(self.w))
        print('Predictor: {}'.format(self.predictor))
        print('ITEMS:\n------')
        self.print_items()

    def update_all(self) -> None:
        self.update_training_dataset()
        self.update_labels()


