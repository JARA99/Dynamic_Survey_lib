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
    a for launching a question [a]nd training the model after\n\
    i for printing [i]nformation\n\
    ii for printing information of the 0 item\n\
    t for [t]raining the model\n\
    b for [b]reak\n'
HELP_TEXT_SUMARY = '[h,q,a,i,ii,t,b]: '
ETA = 0.1
ETA_ST = 1
ITER = 2000
VERBOSE = False

PREDICTOR = blc.reg_predictor
GRADIENT_DEC = blc.gradient_descent

SELF_STD_W,SELF_COUNT_W,CAT_STD_W,CAT_COUNT_W = 0.5,-0.5,0.25,-0.25

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
item.item.set_statistics_weights(SELF_STD_W,SELF_COUNT_W,CAT_STD_W,CAT_COUNT_W)

seasons_survey = survey.survey(questions,'Cuestionario sobre estaciones del año')

dim = len(CATEGORIES) #Categories plus 4 statistic features plus an expert feature.
dim_ext = dim + 4 + 1 #Categories plus 4 statistic features plus an expert feature.
w = np.zeros(dim_ext)
w[-1] = 1
w[dim:dim+4] = SELF_STD_W, SELF_COUNT_W, CAT_STD_W, CAT_COUNT_W

seasons_survey.set_predictor(PREDICTOR)
seasons_survey.set_w(w)

questions_indexes = list(np.arange(seasons_survey.item_amount))
# print(questions_indexes)

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
    elif instrucction == 'a':
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
        seasons_survey.update_all()
        w = GRADIENT_DEC(blc.squared_loss,blc.squared_loss_derivative,seasons_survey.training_dataset,ETA,ITER,VERBOSE,w)
        seasons_survey.set_w(w)
    elif instrucction == 'i':
        seasons_survey.update_all()
        seasons_survey.print_info()
    elif instrucction == 't':
        seasons_survey.update_all()
        w = GRADIENT_DEC(blc.squared_loss,blc.squared_loss_derivative,seasons_survey.training_dataset,ETA,ITER,VERBOSE,w)
        seasons_survey.set_w(w)
    elif instrucction == 'b':
        break
    elif instrucction == 'ii':
        seasons_survey.print_item_info(0)
    else:
        print(HELP_TEXT)

        


