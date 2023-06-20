import numpy as np

class pydyn_surv_list(list):
    def __init__(self,l:list = []):
        super().__init__(l)

    def probabilities(self,all_nanzero_to_one = False,*args,**kargs) -> list:
        probs = [i.probability(*args,**kargs) for i in self]
        # print(probs)
        if (not any(probs) or np.isnan(probs).all()) and all_nanzero_to_one:
            probs = [1 for i in probs]
            # print(probs)
        return probs
    
    def ids(self) -> list:
        return [i.id for i in self]
    
    def questions(self) -> list:
        return [i.question_text for i in self]
    
    def names(self) -> list:
        return [i.name for i in self]