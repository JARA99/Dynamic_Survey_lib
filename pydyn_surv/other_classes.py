import numpy as np

class pydyn_surv_list(list):
    def __init__(self,l:list = []):
        """A list of pydyn_surv objects with some useful methods.
        Methods
        -------
        * **probabilities:**
            Returns a list of probabilities of each item in the list.

        * **ids:**
            Returns a list of ids of each item in the list (only works if the list is made of pydyn_surv.item.item objects).
        
        * **questions:**
            Returns a list of questions of each item in the list (only works if the list is made of pydyn_surv.item.item objects).
        
        * **names:**
            Returns a list of names of each item in the list (only works if the list is made of pydyn_surv.survey.survey objects).
        
        * **answer_history:**
            Returns a list of answer_history of each item in the list (only works if the list is made of pydyn_surv.item.item objects).
        Returns
        -------
        pydyn_surv_list: pydyn_surv.other_classes.pydyn_surv_list
            A pydyn_surv_list object.
        """
        super().__init__(l)

    def probabilities(self,all_zero_to_one = False,nan_to_zero = True,*args,**kargs) -> list:
        """Returns a list of probabilities of each item in the list.
        Parameters
        ----------
        all_zero_to_one: bool
            If True, all probabilities are set to 1 if all of them are 0.
        nan_to_zero: bool
            If True, all probabilities that are np.nan are set to 0.
        *args, **kargs:
            Arguments and keyword arguments to be passed to the probability method of each item.
        Returns
        -------
        probs: list
            A list of probabilities of each item in the list.
        """
        probs = [i.probability(*args,**kargs) for i in self]
        # print(probs)

        if nan_to_zero:
            probs = [0 if item == np.nan else item for item in probs]

        if not any(probs) and all_zero_to_one:
            probs = [1 for i in probs]
            # print(probs)
        return probs
    
    def ids(self) -> list:
        """Returns a list of ids of each item in the list (only works if the list is made of pydyn_surv.item.item objects).
        Returns
        -------
        ids: list
            A list of ids of each item in the list.
        """
        return [i.id for i in self]
    
    def questions(self) -> list:
        """Returns a list of questions of each item in the list (only works if the list is made of pydyn_surv.item.item objects).
        Returns
        -------
        questions: list
            A list of questions of each item in the list.
        """
        return [i.question_text for i in self]
    
    def names(self) -> list:
        """Returns a list of names of each item in the list (only works if the list is made of pydyn_surv.survey.survey objects).
        Returns
        -------
        names: list
            A list of names of each item in the list.
        """
        return [i.name for i in self]
    
    def answer_history(self) -> list:
        """Returns a list of answer_history of each item in the list (only works if the list is made of pydyn_surv.item.item objects).
        Returns
        -------
        answer_history: list
            A list of answer_history of each item in the list.
        """
        return [i.answer_history for i in self]