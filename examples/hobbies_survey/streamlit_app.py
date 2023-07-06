import streamlit as st
from streamlit_utilities import *
import plotly.express as px
import pandas as pd

import hobbies_survey as HS
import definitions as DEFS

from pydyn_surv.classes import survey
import random as rnd


Q_AMT = 25
NO_TENDENCE_LIMIT = 3

if 'no_tendence' not in st.session_state:
    st.session_state['no_tendence'] = 0
if 'q_count' not in st.session_state:
    st.session_state['q_count'] = 0
if 'current_item' not in st.session_state:
    st.session_state['current_item'] = None
if 'current_item_question_text' not in st.session_state:
    st.session_state['current_item_question_text'] = None
if 'current_surveys' not in st.session_state:
    st.session_state['current_surveys'] = []
    
title_view = st.empty()
q_devider_t = st.divider()
question_view = st.empty()
next_button_view = st.empty()
enumeration_view = st.empty()
q_devider_b = st.divider()
# blind_evaluation_view = st.empty()
results_view = st.empty()
# model_evaluation_view = st.empty()


def generate_q():
    # print('Generating new question...')
    st.session_state.current_item, st.session_state.current_item_question_text = get_q()

def answer_q(value):
    # print('Answering question...')
    st.session_state.current_item.answer(value)
    f = open(DEFS.SURVEY_REGISTER,'a')
    item_ = st.session_state.current_item
    survey_ = item_.get_origin_survey()
    f.write('"{}","{}",{},"{}","{}","{}","{}"\n'.format(item_.id,item_.get_categories_names(),value,survey_.name,list(survey_.get_weight()),st.session_state.current_surveys.names(),st.session_state.current_surveys_probs))
    f.close()
    st.session_state.q_count = survey.survey.get_total_launches()
    # print(st.session_state.q_count)
    generate_q()
    # print(st.session_state.current_item.answer_history)
    # st.session_state.current_item, st.session_state.current_item_question_text = get_q()

def get_q():
    srvs = HS.hobbies_survey.get_surveys()
    st.session_state.current_surveys = srvs
    st.session_state.current_surveys_probs = srvs.probabilities()
    # print('     Total launches: {}'.format(survey.survey.get_total_launches()))
    # print('     Surveys avilable: {}'.format(srvs.names()))
    # print('     Probability of each: {}'.format(srvs.probabilities()))
    if len(srvs) == 0:
        Warning('No surveys available for this user.')
        sel = HS.hobbies_survey
        st.session_state.no_tendence += 1
        if st.session_state.no_tendence >= NO_TENDENCE_LIMIT:
            # make_closing()
            st.session_state.q_count = Q_AMT + 1
    else:
        # print('l0 history: {}'.format(srvs[0].get_items().answer_history()))
        sel:survey.survey = rnd.choices(srvs,srvs.probabilities())[0]

    item_,item_question_text, item_answers_text, item_answers_values = sel.launch_random(all_zero_to_one=True)

    return item_, item_question_text

def make_closing():
    question_view.empty()
    next_button_view.empty()
    enumeration_view.empty()
    q_devider_b.empty()
    q_devider_t.empty()

    with results_view.container():
        fig = make_graph()
        if fig is not None:
            st.plotly_chart(fig)
        else:
            emojicols = st.columns([1,1,1])
            emojicols[1].write('# :astonished::confounded::sweat:')
            st.write('#### ¡Lo sentimos! Pero no hemos encontrado un hobby que se ajuste a tus preferencias.')
        st.write('##### {}'.format('Evalúa el desempeño del modelo:'))

        opts = np.arange(0,105,5)
        
        eval_value = st.select_slider(
            'eval',label_visibility='hidden',
            options=opts,format_func = get_eval_label,value = 0,key='eval_slider')
        
        save_eval_button = st.button('Guardar evaluación')
        if save_eval_button:
            with open(DEFS.SURVEY_REGISTER,'a') as f:
                f.write('# EVALUATION: {}\n'.format(eval_value))

            with open(DEFS.SURVEY_REGISTER,'r') as f:
                st.download_button('Descargar resultados',data=f,file_name='resultados.csv',mime='text/csv')

def make_graph():
    all_l2 = np.array(HS.s2).flatten()

    hobbies_table = []

    for srv in all_l2:
        w = srv.get_weight()
        for i in range(len(w)):
            if w[i] > 0:
                hobbies_table.append(['{}: {}'.format(srv.name,srv.categories[i]),round((w[i]/2)*100)])
    
    if len(hobbies_table) == 0:
        return None

    hobbies_table = pd.DataFrame(hobbies_table,columns=['Hobbie','Preferencia'])
    fig = px.pie(hobbies_table, values='Preferencia', names='Hobbie', title='Preferencia por hobbies')

    return fig


title_view.title('Encuesta de hobbies')
enumeration_view.caption('<center> {}/{} </center>'.format(st.session_state.q_count,Q_AMT),True)


if st.session_state.q_count <= Q_AMT:

    if st.session_state.current_item is None:
        generate_q()

    value = likert_question(question_view,st.session_state.current_item_question_text,st.session_state.current_item.launch_count)

    trigger = next_button_view.button('Siguiente')
    if trigger:
        answer_q(value)
        if st.session_state.q_count <= Q_AMT:
            value = likert_question(question_view,st.session_state.current_item_question_text)
            enumeration_view.caption('<center> {}/{} </center>'.format(st.session_state.q_count,Q_AMT),True)
        else:
            make_closing()
    # print_info_button = st.button('info')
    # if print_info_button:
    #     st.session_state.current_item.print_info()
    #     HS.s0[0].print_info()


else:
    make_closing()