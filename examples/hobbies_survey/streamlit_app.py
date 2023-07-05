import streamlit as st
from streamlit_utilities import *

import hobbies_survey as HS
import definitions as DEFS

from pydyn_surv.classes import survey
import random as rnd

Q_AMT = 25
if 'no_tendence' not in st.session_state:
    st.session_state['no_tendence'] = 0
if 'q_count' not in st.session_state:
    st.session_state['q_count'] = 0
if 'answer_state' not in st.session_state:
    st.session_state['answer_state'] = 1


def get_q():
    srvs = HS.hobbies_survey.get_surveys()
    print('Total launches: {}'.format(survey.survey.get_total_launches()))
    print(srvs.names())
    print(srvs.probabilities())
    if len(srvs) == 0:
        Warning('No surveys available for this user.')
        sel = HS.hobbies_survey
        st.session_state.no_tendence += 1
        if st.session_state.no_tendence > 5:
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
    st.session_state.answer_state = 0
    current_q,current_q_text = get_q()
    form = st.form(key='form_{}'.format(st.session_state.q_count))

    value = likert_question(form,current_q_text)
    form_filled = form.form_submit_button('Siguiente')
    # while not form_filled:
    #     print('waiting for form to be filled')
    # answer_q(current_q,value)
    # if form_filled:
    #     print(value)
    #     print(current_q.question_text)
    #     current_q.answer(value)
    #     st.session_state.q_count += 1
    #     st.session_state.answer_state = 1
        # st.session_state.answer_state = 0



def answer_q(q,value):
    # q.answer(value)
    # st.session_state.answer_state = 1
    print(value)
    print(q.question_text)
    q.answer(value)
    st.session_state.q_count += 1
    st.session_state.answer_state = 1

if st.session_state.answer_state == 1:
    create_a_question()
# else:
#     next_button_view.button('nueva',on_click=create_a_question(question_view,next_button_view))

# questions_views = []

# for q in Q_AMT:
#     temp = st.empty()
#     questions_views.append(temp)



