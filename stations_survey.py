from survey import survey, item
from LinearClassifier import basic_linear_classifier as blc
import pandas as pd
import numpy as np
import random as rnd


CATEGORIES = ['Invierno','Primavera','Verano','Otoño']
HELP_TEXT = '\
This is a little help for navigating the script:\n\
    h show this [h]elp\n\
    q for launching a [q]uestion\n\
    i for printing [i]nformation\n\
    t for [t]raining the model\n\
    b for [b]reak\n'
HELP_TEXT_SUMARY = '[h,q,i,t,b]: '
ETA = 0.1
ETA_ST = 1
ITER = 2000
VERBOSE = False

def get_questions_from_excel(excel_file:str = 'tests/Questionarie.xlsx') -> list:

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
        tdict['principal_cat_list'] = question_row['Categorías']
        tdict['expert_extra'] = question_row['Punteo extra']

        questions.append(tdict)
    
    return questions

questions = get_questions_from_excel()
item.item.set_categories(CATEGORIES)
seasons_survey = survey.survey(questions,'Cuestionario sobre estaciones del año')

dim = len(CATEGORIES) + 4 + 1 #Categories plus 4 statistic features plus an expert feature.
w = np.zeros(dim)

seasons_survey.set_predictor(blc.reg_predictor)
seasons_survey.set_w(w)

questions_indexes = list(np.arange(seasons_survey.item_amount))
print(questions_indexes)

print(HELP_TEXT)

while True:
    instrucction = input(HELP_TEXT_SUMARY)

    if instrucction == 'h':
        print(HELP_TEXT)
    elif instrucction == 'q':
        seasons_survey.update_all()
        weights = seasons_survey.predicted_item_labels
        if any(weights) != 0:
            # print(weights)
            min_weight = min(weights)
            if min_weight < 0:
                item_index = rnd.choices(questions_indexes,weights=list(np.array(weights) + abs(min_weight)),k=1)
            else:
                item_index = rnd.choices(questions_indexes,weights=weights,k=1)
            # print('random with weights = {}'.format(item_index))
            seasons_survey.launch_item(item_index[0])
        else:
            item_index = rnd.choice(questions_indexes)
            # print('random without weights = {}'.format(item_index))
            seasons_survey.launch_item(item_index)
    elif instrucction == 'i':
        seasons_survey.update_all()
        seasons_survey.print_info()
    elif instrucction == 't':
        seasons_survey.update_all()
        w = blc.gradient_descent(blc.squared_loss,blc.squared_loss_derivative,seasons_survey.training_dataset,ETA,ITER,VERBOSE,w)
        seasons_survey.set_w(w)
    elif instrucction == 'b':
        break
    else:
        print(HELP_TEXT)

        


