from pydyn_surv.classes import survey, item
from pydyn_surv.LinearClassifier import basic_linear_classifier as blc
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

ANSWERS = ['Muy en desacuerdo','En desacuerdo','Ni de acuerdo ni en desacuerdo','De acuerdo','Muy de acuerdo']
ANSWER_VALUES = [-2,-1,0,1,2]

def get_questions_from_excel(excel_file:str = 'Questionarie.xlsx') -> list:

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
        tdict['category_vector'] = question_row['Categorías']
        tdict['expert_extra'] = question_row['Punteo extra']

        titem = item.item(tdict)

        questions.append(titem)
    
    return questions

qs = get_questions_from_excel()

# print(qs)

seasons_survey = survey.survey(qs[:12],'Estaciones del año',predictor=PREDICTOR,categories=CATEGORIES,origin_category=['seasons'])

subseason_survey = survey.survey(qs[12:],'Subestaciones del año',predictor=PREDICTOR,categories=CATEGORIES,origin_category=['Invierno'],origin=seasons_survey)

print(seasons_survey.get_items()[1].answers_text)
print(seasons_survey.get_items()[1].answers_values)
print([i.categoryvector for i in seasons_survey.items])
# print(seasons_survey)
# print(subseason_survey)
# print(seasons_survey == subseason_survey)
# print(seasons_survey.get_items().ids())

# print([i.name for i in seasons_survey.offspring])
# print([i.name for i in subseason_survey.offspring])
# # seasons_survey.add_offspring(seasons_survey)

# seasons_survey.offspring = [subseason_survey]
# # seasons_survey.offspring.append('hola')
# print(seasons_survey.offspring == subseason_survey.offspring)

# print([i.name for i in seasons_survey.offspring])
# print([i.name for i in subseason_survey.offspring])

# print([i.name for i in seasons_survey.launch_survey()])
# # print(seasons_survey.get_items())
# print(seasons_survey.get_items().questions())
# print(seasons_survey.get_items().probabilities())


def subseason_condition(self):
    for origin in self.origin:
        if origin.get_launch_count() > 4:
            return True
    return False

subseason_survey.set_condition_function(subseason_condition)

keep = True
while keep:
    srvs = seasons_survey.get_surveys()
    print(srvs.names())
    sel = rnd.choices(srvs,srvs.probabilities())[0]

    itms = sel.get_items()
    sel_itm = rnd.choices(itms,itms.probabilities())[0]

    sel.launch_item(sel_itm)



