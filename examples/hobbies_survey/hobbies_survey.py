from pydyn_surv.classes import survey, item
from pydyn_surv.classes import funcs
import definitions as DEFS
import pandas as pd
import numpy as np
import random as rnd
from typing import List

ITEM_PROB_DEFS = {
    "axis_move":2,
    "std_weight":0,
    "cat_std_weight":0.5,
    "launch_count_weight":-1,
    "cat_launch_count_weight":-8
}
HELP_TEXT = '\
This is a little help for navigating the script:\n\
    h       show this [h]elp\n\
    q       for launching a question [a]nd training the model after\n\
    si      for printing [i]nformation\n\
    ii n    for printing information of the item with id=n\n\
    b       for [b]reak\n'
HELP_TEXT_SUMARY = '[h,q,si,ii n,b]: '


def l0_item_prob(self,not_repeated_since = 15,item_prob_defs = ITEM_PROB_DEFS) -> float:
    return funcs.FUNC_LIKERT_ITEM_PROBABILITY_WITH_STATISTICS(self,not_repeated_since=not_repeated_since,**item_prob_defs)
def l1_item_prob(self,not_repeated_since = 10,item_prob_defs = ITEM_PROB_DEFS) -> float:
    return funcs.FUNC_LIKERT_ITEM_PROBABILITY_WITH_STATISTICS(self,not_repeated_since=not_repeated_since,**item_prob_defs)
def l2_item_prob(self,not_repeated_since = 4,item_prob_defs = ITEM_PROB_DEFS) -> float:
    return funcs.FUNC_LIKERT_ITEM_PROBABILITY_WITH_STATISTICS(self,not_repeated_since=not_repeated_since,**item_prob_defs)


def l0_prob(self:survey.survey) -> float:
    p = 1 - (self.launch_count/self.item_amount)
    if p <= 0:
        p = 1/20
    return p
def l1_prob(self:survey.survey,extra = 4) -> float:
    p = extra - extra*(self.launch_count/self.item_amount)
    if p <= 0:
        p = 1/15
    return p/4
def l2_prob(self:survey.survey,extra = 16) -> float:
    p = extra - extra*(self.launch_count/self.item_amount)
    if p <= 0:
        p = 1/9
    return p/20

def l0_condition(self) -> bool:
    return True
def l1_condition(self:survey.survey) -> bool:
    initial_condition = funcs.CONDITION_ORIGIN_LAUNCH_COUNT_OVER(self,4)
    if initial_condition:
        self_label = self.get_self_label()
        if self_label > 0.5:
            return True
    else:
        return False
def l2_condition(self:survey.survey) -> bool:
    self_label = self.get_self_label()
    if self_label > 0.5:
        return True
    else:
        return False



def get_surveys_from_excel(excel_file:str = 'data/hobbies_surv.xlsx',level:int = 0,surveys_names = DEFS.l0, categories_names = DEFS.l1, origin = None, surv_prob:callable = l0_prob, surv_condition:callable = l0_condition, item_prob:callable = l0_item_prob) -> List[survey.survey]:

    def str_to_list(string):
        lst = string[1:-1].split(',')
        for i in range(len(lst)):
            lst[i] = int(lst[i])
        return lst

    questions_df = pd.read_excel(excel_file,sheet_name=level)
    questions_df['id'] = ['{}.{}'.format(level,i) for i in questions_df.index]
    for column_number in range(level+1):
        questions_df[column_number] = questions_df[column_number].apply(lambda row: str_to_list(row))

    if level == 0:

        survey_name_index = 0
        survey_name = surveys_names
        questions = []
        dimension = len(categories_names)

        for index, question_row in questions_df.iterrows():
            tdict = dict()

            tdict['question'] = question_row['item']
            tdict['answers'] = DEFS.answers
            tdict['answers_values'] = DEFS.answers_values
            tdict['category_vector'] = np.zeros(dimension)
            tdict['expert_extra'] = DEFS.expert_extra
            tdict['category_vector'] = question_row[level]
            tdict['id'] = question_row['id']

            titem = item.item(tdict,probability_function=item_prob)

            questions.append(titem)
            
        survey_ = survey.survey(questions,
                                survey_name,
                                categories=categories_names,
                                origin_category=survey_name,
                                condition_function=surv_condition,
                                probability_function=surv_prob)
        
        return [survey_]
    
    elif level == 1:

        questions_df['origin_category'] = [i.index(1) for i in questions_df[level-1]]

        surveys = []

        for survey_name_index in range(len(surveys_names)):

            questions = []
            survey_name = surveys_names[survey_name_index]
            dimension = len(categories_names[survey_name_index])
            questions_chunck = questions_df[questions_df['origin_category'] == survey_name_index]

            for index, question_row in questions_chunck.iterrows():
                tdict = dict()

                tdict['question'] = question_row['item']
                tdict['answers'] = DEFS.answers
                tdict['answers_values'] = DEFS.answers_values
                tdict['category_vector'] = np.zeros(dimension)
                tdict['expert_extra'] = DEFS.expert_extra
                tdict['category_vector'] = question_row[level]
                tdict['id'] = question_row['id']

                titem = item.item(tdict,probability_function=item_prob)

                questions.append(titem)
            
            tsurvey = survey.survey(questions,
                                    survey_name,
                                    categories=categories_names[survey_name_index],
                                    origin=origin,
                                    origin_category=survey_name,
                                    probability_function=surv_prob,
                                    condition_function=surv_condition)
            surveys.append(tsurvey)
        
        return surveys  
      
    elif level == 2:

        questions_df['origin_survey'] = [i.index(1) for i in questions_df[level-2]]
        questions_df['origin_category'] = [i.index(1) for i in questions_df[level-1]]

        surveys = []

        for surveys_names_index in range(len(surveys_names)):
            # print('On {}, {}'.format(surveys_names_index,surveys_names[surveys_names_index]))
            surveys.append([])
            for survey_name_index in range(len(surveys_names[surveys_names_index])):

                questions = []
                survey_name = surveys_names[surveys_names_index][survey_name_index]
                dimension = len(categories_names[surveys_names_index][survey_name_index])
                questions_chunck = questions_df[(questions_df['origin_survey'] == surveys_names_index) & (questions_df['origin_category'] == survey_name_index)]
                # questions_chunck = t_questions_chunck[questions_df['origin_category'] == survey_name_index]

                for index, question_row in questions_chunck.iterrows():
                    tdict = dict()

                    tdict['question'] = question_row['item']
                    tdict['answers'] = DEFS.answers
                    tdict['answers_values'] = DEFS.answers_values
                    tdict['category_vector'] = np.zeros(dimension)
                    tdict['expert_extra'] = DEFS.expert_extra
                    tdict['category_vector'] = question_row[level]
                    tdict['id'] = question_row['id']

                    titem = item.item(tdict,probability_function=item_prob)

                    questions.append(titem)
                
                tsurvey = survey.survey(questions,
                                        survey_name,
                                        categories=categories_names[surveys_names_index][survey_name_index],
                                        origin=origin[surveys_names_index],
                                        origin_category=survey_name,
                                        probability_function=surv_prob,
                                        condition_function=surv_condition)
                surveys[surveys_names_index].append(tsurvey)
            
        return surveys
    
    else:
        raise ValueError('Level must be 0, 1 or 2')




s0 = get_surveys_from_excel()
s1 = get_surveys_from_excel(level=1,surveys_names=DEFS.l1,categories_names=DEFS.l2,origin=s0,surv_prob=l1_prob,surv_condition=l1_condition,item_prob=l1_item_prob)
s2 = get_surveys_from_excel(level=2,surveys_names=DEFS.l2,categories_names=DEFS.l3,origin=s1,surv_prob=l2_prob,surv_condition=l2_condition,item_prob=l2_item_prob)

# for s in survey.survey.instances:
#     s.print_info(False)

hobbies_survey = s0[0]


def launch_q():
    srvs = hobbies_survey.get_surveys()
    print(srvs.names())
    print(srvs.probabilities())
    if len(srvs) == 0:
        raise ValueError('No surveys available for this user.')
    sel:survey.survey = rnd.choices(srvs,srvs.probabilities())[0]

    itms = sel.get_items()
    sel_itm = rnd.choices(itms,itms.probabilities())[0]

    sel.launch_on_terminal(sel_itm)

    sel.train()
    print('\n{} W = {}\n'.format(sel.name,np.round(sel.get_weight(),2)))

def print_info():
    print('Hobbies survey:\n---------------')
    print('Total answers: {}'.format(survey.survey.get_total_launches()))
    print('\nWeight history:')
    print('---------------')
    for surv in survey.survey.instances:
        print('{} W = {}'.format(surv.name,np.round(surv.get_weight(),2)))
        print('History: {}'.format(surv.get_weight_history()))

def print_i_info(id_):
    items = item.item.get_instance_by_id(id_)
    hobbies_survey.update_all()
    # subseason_survey.update_all()
    for item_ in items:
        print('{}]'.format(item_.id))
        print('-----')
        item_.print_info()


# print(item.item.instances)

if __name__=='__main__':

    help_key = 'h'
    question_key = 'q'
    info_key = 'si'
    info_item_key = 'ii '
    break_key = 'b'

    keep = True
    while keep:
        next_action = input(HELP_TEXT_SUMARY)
        if next_action == help_key:
            print(HELP_TEXT)
        elif next_action == question_key:
            try:
                launch_q()
            except:
                print('No muestras preferencias por ninguna de las categorías disponibles en esta encuesta.')
                keep = False
        elif next_action == info_key:
            print_info()
        elif next_action[:len(info_item_key)] == info_item_key:
            print_i_info(next_action[len(info_item_key):])
        elif next_action == break_key:
            keep = False
