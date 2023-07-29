import numpy as np

class pydyn_surv_list(list):
    def __init__(self,l:list = []):
        super().__init__(l)

    def probabilities(self,all_zero_to_one = False,nan_to_zero = True,*args,**kargs) -> list:
        probs = [i.probability(*args,**kargs) for i in self]
        # print(probs)

        if nan_to_zero:
            probs = [0 if item == np.nan else item for item in probs]

        if not any(probs) and all_zero_to_one:
            probs = [1 for i in probs]
            # print(probs)
        return probs
    
    def ids(self) -> list:
        return [i.id for i in self]
    
    def questions(self) -> list:
        return [i.question_text for i in self]
    
    def names(self) -> list:
        return [i.name for i in self]
    
    def answer_history(self) -> list:
        return [i.answer_history for i in self]