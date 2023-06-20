class pydyn_surv_list(list):
    def __init__(self,l:list = []):
        super().__init__(l)

    def probabilities(self,*args,**kargs) -> list:
        return [i.probability(*args,**kargs) for i in self]
    
    def ids(self) -> list:
        return [i.id for i in self]
    
    def questions(self) -> list:
        return [i.question_text for i in self]
    
    def names(self) -> list:
        return [i.name for i in self]