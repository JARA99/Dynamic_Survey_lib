from pydyn_surv import survey, item
from pydyn_surv import ml
from pydyn_surv import funcs
import pandas as pd
import numpy as np
import random as rnd

CATEGORIES = ['Invierno','Primavera','Verano','Otoño']
HELP_TEXT = '\
This is a little help for navigating the script:\n\
    h       show this [h]elp\n\
    q       for launching a question [a]nd training the model after\n\
    i       for printing [i]nformation\n\
    ii n    for printing information of the item with id=n\n\
    b       for [b]reak\n'
HELP_TEXT_SUMARY = '[h,q,i,ii n,b]: '

ETA = 0.1
ETA_ST = 1
ITER = 2000
VERBOSE = False

PREDICTOR = ml.reg_predictor
GRADIENT_DEC = ml.gradient_descent

ANSWERS = ['Muy en desacuerdo','En desacuerdo','Ni de acuerdo ni en desacuerdo','De acuerdo','Muy de acuerdo']
ANSWER_VALUES = [-2,-1,0,1,2]

def get_questions_from_excel(excel_file:str = 'Questionarie.xlsx',dimension:int = 4) -> list:

    def str_to_list(string):
        lst = string.split(',')
        for i in range(len(lst)):
            lst[i] = int(lst[i])
        return lst

    questions_df = pd.read_excel(excel_file,sheet_name='Preguntas',converters={'Categorías':str})
    answers_df = pd.read_excel(excel_file,sheet_name='Respuestas',index_col='Grupo de respuestas')
    # print(answers_df)

    questions_df['Categorías'] = questions_df['Categorías'].apply(lambda row: str_to_list(row))

    questions = []

    for index, question_row in questions_df.iterrows():
        tdict = dict()

        tdict['question'] = question_row['Pregunta']
        tdict['answers'] = list(answers_df.loc[question_row['Grupo de respuestas']])
        tdict['answers_values'] = ANSWER_VALUES
        tdict['category_vector'] = np.zeros(dimension)
        tdict['expert_extra'] = question_row['Punteo extra']

        for cat in question_row['Categorías']:
            coord = abs(cat) - 1
            if cat > 0:
                tdict['category_vector'][coord] = 1
            else:
                tdict['category_vector'][coord] = -1

        # tdict['category_unit_vector'] = tdict['category_vector']/np.linalg.norm(tdict['category_vector'])
        # tdict['category_vector'] = tdict['category_unit_vector']

        titem = item.item(tdict,index)

        questions.append(titem)
    
    return questions

qs = get_questions_from_excel()
# print(qs)

seasons_survey = survey.survey(qs,'Estaciones del año',predictor=PREDICTOR,categories=CATEGORIES,origin_category=['Estaciones'])
# subseason_survey = survey.survey(qs[12:],'Subestaciones del año',predictor=PREDICTOR,categories=CATEGORIES,origin_category=CATEGORIES)

seasons_survey.set_probability_function_of_items(funcs.FUNC_LIKERT_ITEM_PROBABILITY_WITH_STATISTICS)
# subseason_survey.set_probability_function_of_items(funcs.FUNC_LIKERT_ITEM_PROBABILITY_WITH_STATISTICS)

# subseason_survey.add_origin(seasons_survey)
# seasons_survey.add_offspring(subseason_survey)

# print('Season offspring:',[i.name for i in seasons_survey.offspring])
# print('Subseason offspring:',[i.name for i in subseason_survey.offspring])
# print('Season origin:',[i.name for i in seasons_survey.origin])
# print('Subseason origin:',[i.name for i in subseason_survey.origin])

# subseason_survey.set_condition_function(funcs.CONDITION_ORIGIN_LAUNCH_COUNT_OVER)
# subseason_survey.set_condition_function(funcs.FUNC_FALSE)

def launch_q():
    srvs = seasons_survey.get_surveys(count = 3)
    sel:survey.survey = rnd.choices(srvs,srvs.probabilities(all_zero_to_one = True))[0]

    itms = sel.get_items()
    sel_itm = rnd.choices(itms,itms.probabilities(all_zero_to_one = True))[0]

    sel.launch_on_terminal(sel_itm)

    sel.train()
    print('\n{} W = {}\n'.format(sel.name,np.round(sel.get_weight(),2)))

def print_info():
    print('Seasons survey:\n-----------------\n')
    seasons_survey.update_all()
    seasons_survey.print_info()
    print('\n')
    # print('Subseasons survey:\n-----------------\n')
    # subseason_survey.update_all()
    # subseason_survey.print_info()
    # print('\n')

def print_i_info(id_):
    items = item.item.get_instance_by_id(id_)
    seasons_survey.update_all()
    # subseason_survey.update_all()
    for item_ in items:
        print('{}]'.format(item_.id))
        print('-----')
        item_.print_info()

help_key = 'h'
question_key = 'q'
info_key = 'i'
info_item_key = 'ii '
break_key = 'b'

# print(item.item.instances)

keep = True
while keep:
    next_action = input(HELP_TEXT_SUMARY)
    if next_action == help_key:
        print(HELP_TEXT)
    elif next_action == question_key:
        launch_q()
    elif next_action == info_key:
        print_info()
    elif next_action[:len(info_item_key)] == info_item_key:
        print_i_info(int(next_action[len(info_item_key):]))
    elif next_action == break_key:
        keep = False
