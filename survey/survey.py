import numpy as np
from .item import item as item

class survey:

    def __init__(self,items:list = [],name:str = '',init_training_dataset:list = None,w:np.ndarray = None,predictor = None) -> None:
        self.name = name
        self.training_dataset = init_training_dataset
        self.item_amount = len(items)
        self.item_labels = np.zeros(self.item_amount)
        self.w = w
        self.predictor = predictor
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
            # item_:item
            dataset_pair = item.get_dataset_pair()
            if dataset_pair != None:
                training_dataset.append()
        
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

    def get_labels_predict(self,w:np.ndarray,predictor) -> list:
        predicted_labels = []
        for item_ in self.items:
            item_:item
            x = item_.get_feauture_vector()
            label = predictor(w,x)
            predicted_labels.append(label)
            item_.set_predicted_label(label)
        
        return predicted_labels
    
    def update_labels(self) -> None:
        self.item_labels = self.get_labels_predict(self.w,self.predictor)

    def set_w(self,w:np.ndarray) -> None:
        self.w = w
    
    def set_predictor(self,predictor) -> None:
        self.predictor = predictor

    def update_all(self) -> None:
        self.update_training_dataset()


