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
if 'current_item' not in st.session_state:
    print('reseting current item')
    st.session_state['current_item'] = None
if 'current_item_question_text' not in st.session_state:
    st.session_state['current_item_question_text'] = None
if 'current_surveys' not in st.session_state:
    st.session_state['current_surveys'] = []
    
title_view = st.empty()
st.divider()
question_view = st.empty()
next_button_view = st.empty()
st.divider()
blind_evaluation_view = st.empty()
results_view = st.empty()
model_evaluation_view = st.empty()


def generate_q():
    print('Generating new question...')
    st.session_state.current_item, st.session_state.current_item_question_text = get_q()

def answer_q(value):
    print('Answering question...')
    st.session_state.current_item.answer(value)
    f = open(DEFS.SURVEY_REGISTER,'a')
    item_ = st.session_state.current_item
    survey_ = item_.get_origin_survey()
    f.write('"{}","{}",{},"{}","{}","{}","{}"\n'.format(item_.id,item_.get_categories_names(),value,survey_.name,list(survey_.get_weight()),st.session_state.current_surveys.names(),st.session_state.current_surveys.probabilities()))
    f.close()
    st.session_state.q_count += 1
    generate_q()
    # print(st.session_state.current_item.answer_history)
    # st.session_state.current_item, st.session_state.current_item_question_text = get_q()

def get_q():
    srvs = HS.hobbies_survey.get_surveys()
    st.session_state.current_surveys = srvs
    # print('     Total launches: {}'.format(survey.survey.get_total_launches()))
    # print('     Surveys avilable: {}'.format(srvs.names()))
    # print('     Probability of each: {}'.format(srvs.probabilities()))
    if len(srvs) == 0:
        Warning('No surveys available for this user.')
        sel = HS.hobbies_survey
        st.session_state.no_tendence += 1
        if st.session_state.no_tendence > 5:
            pass #TODO: end survey
    else:
        # print('l0 history: {}'.format(srvs[0].get_items().answer_history()))
        sel:survey.survey = rnd.choices(srvs,srvs.probabilities())[0]

    item_,item_question_text, item_answers_text, item_answers_values = sel.launch_random(all_zero_to_one=True)

    return item_, item_question_text

def make_closing():
    question_view.empty()
    next_button_view.empty()
    with results_view.container():
        with open('survey_register.csv','r') as f:
            st.download_button('Descargar resultados',data=f,file_name='resultados.csv',mime='text/csv')



title_view.title('Encuesta de hobbies')

if st.session_state.q_count <= Q_AMT:

    if st.session_state.current_item is None:
        generate_q()

    value = likert_question(question_view,st.session_state.current_item_question_text)

    trigger = next_button_view.button('Siguiente')
    if trigger:
        answer_q(value)
        if st.session_state.q_count <= Q_AMT:
            value = likert_question(question_view,st.session_state.current_item_question_text)
        else:
            make_closing()
    # print_info_button = st.button('info')
    # if print_info_button:
    #     st.session_state.current_item.print_info()
    #     HS.s0[0].print_info()


else:
    make_closing()