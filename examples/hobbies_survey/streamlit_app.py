import streamlit as st
from streamlit_utilities import *

import hobbies_survey as HS
import definitions as DEFS

from pydyn_surv.classes import survey
import random as rnd

Q_AMT = 25
no_tendence = 0
q_count = 0
answer_state = 1


def get_q():
    srvs = HS.hobbies_survey.get_surveys()
    print('Total launches: {}'.format(survey.survey.get_total_launches()))
    print(srvs.names())
    print(srvs.probabilities())
    if len(srvs) == 0:
        Warning('No surveys available for this user.')
        sel = HS.hobbies_survey
        global no_tendence
        no_tendence += 1
        if no_tendence > 5:
            pass #TODO: end survey
    else:
        print(srvs[0].get_items().answer_history())
        sel:survey.survey = rnd.choices(srvs,srvs.probabilities())[0]

    item_,item_question_text, item_answers_text, item_answers_values = sel.launch_random(all_zero_to_one=True)

    return item_, item_question_text


title_view = st.empty()
# st.divider()
question_view = st.empty()
# next_button_view = st.empty()
# st.divider()
blind_evaluation_view = st.form(key='blind_evaluation_form')
results_view = st.empty()
model_evaluation_view = st.form(key='model_evaluation_form')



title_view.title('Encuesta de hobbies')


def create_a_question():
    global answer_state
    global q_count
    answer_state = 0
    current_q,current_q_text = get_q()
    form = st.form(key='form_{}'.format(q_count))

    value = likert_question(form,current_q_text)
    form_filled = form.form_submit_button('Siguiente')
    if form_filled:
        print(value)
        print(current_q.question_text)
        answer_q(current_q,value)
        q_count += 1
        # answer_state = 0


def answer_q(q,value):
    q.answer(value)
    global answer_state
    # answer_state = 1

if answer_state == 1:
    q_count = create_a_question()
# else:
#     next_button_view.button('nueva',on_click=create_a_question(question_view,next_button_view))



