import streamlit as st
from streamlit_utilities import *
import plotly.express as px
import pandas as pd

# import hobbies_survey as HS
from hobbies_survey import get_surveys_from_excel, l1_prob, l1_condition, l1_item_prob, l2_prob, l2_condition, l2_item_prob
import definitions as DEFS

from pydyn_surv.classes import survey
import random as rnd

from github import Github
from github import Auth

# ----------------------------------------------------------------------------------------------------------------------
# CONFIGURATIONS:
# ----------------------------------------------------------------------------------------------------------------------
st.set_page_config(initial_sidebar_state="collapsed") 
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# CONSTANTS:
# ----------------------------------------------------------------------------------------------------------------------
Q_AMT = 30
NO_TENDENCE_LIMIT = 3
GITHUB_REPO = 'streamlit-pygithub-storage'
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
auth = Auth.Token(GITHUB_TOKEN)
g = Github(auth=auth)
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# SESSION STATE:
# ----------------------------------------------------------------------------------------------------------------------
if 's0' not in st.session_state:
    st.session_state.s0 = get_surveys_from_excel()
s0 = st.session_state.s0

if 's1' not in st.session_state:
    st.session_state.s1 = get_surveys_from_excel(level=1,surveys_names=DEFS.l1,categories_names=DEFS.l2,origin=s0,surv_prob=l1_prob,surv_condition=l1_condition,item_prob=l1_item_prob)
s1 = st.session_state.s1

if 's2' not in st.session_state:
    st.session_state.s2 = get_surveys_from_excel(level=2,surveys_names=DEFS.l2,categories_names=DEFS.l3,origin=s1,surv_prob=l2_prob,surv_condition=l2_condition,item_prob=l2_item_prob)
s2 = st.session_state.s2

hobbies_survey = s0[0]

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
if 'current_surveys_probs' not in st.session_state:
    st.session_state['current_surveys_probs'] = []
if 'save_file' not in st.session_state:
    st.session_state['save_file'] = '# NEW ENTRY\n'
if 'save_button_disabled' not in st.session_state:
    st.session_state['save_button_disabled'] = True
# ----------------------------------------------------------------------------------------------------------------------  

# ----------------------------------------------------------------------------------------------------------------------
# PAGE LAYOUT:
# ----------------------------------------------------------------------------------------------------------------------
title_view = st.empty()
instructions_view = st.expander('Instrucciones')
instructions_view.write('A continuación se le presentarán una serie de afirmaciones, por favor indique en qué medida estas representan su personalidad, gustos y preferencias. Si la afirmación lo representa, seleccione algún porcentaje en la escala de **:green["De acuerdo"]** (hacia la derecha), de lo contrario seleccione un porcentaje en la escala de **:green["En desacuerdo"]** (hacia la izquierda).\n\nAl finalizar se le presentará un resumen de las conclusiones del modelo y una evaluación del mismo.')
q_devider_t = st.divider()
question_view = st.empty()
next_button_view = st.empty()
enumeration_view = st.empty()
q_devider_b = st.divider()
# blind_evaluation_view = st.empty()
results_view = st.empty()
# model_evaluation_view = st.empty()
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# FUNCTIONS:
# ----------------------------------------------------------------------------------------------------------------------
def generate_q():
    # print('Generating new question...')
    st.session_state.current_item, st.session_state.current_item_question_text = get_q()

def answer_q(value):
    # print('Answering question...')
    st.session_state.current_item.answer(value)
    # f = open(DEFS.SURVEY_REGISTER,'a')
    item_ = st.session_state.current_item
    survey_ = item_.get_origin_survey()
    st.session_state.save_file += ('"{}","{}",{},"{}","{}","{}","{}"\n'.format(item_.id,item_.get_categories_names(),value,survey_.name,list(survey_.get_weight()),st.session_state.current_surveys.names(),st.session_state.current_surveys_probs))
    # f.close()
    st.session_state.q_count += 1 # survey.survey.get_total_launches()
    # print(st.session_state.q_count)
    generate_q()
    # print(st.session_state.current_item.answer_history)
    # st.session_state.current_item, st.session_state.current_item_question_text = get_q()

def get_q():
    srvs = hobbies_survey.get_surveys()
    st.session_state.current_surveys = srvs
    st.session_state.current_surveys_probs = srvs.probabilities()
    if len(srvs) == 0:
        Warning('No surveys available for this user.')
        sel = hobbies_survey
        st.session_state.no_tendence += 1
        if st.session_state.no_tendence >= NO_TENDENCE_LIMIT:
            # make_closing()
            st.session_state.q_count = Q_AMT
    else:
        # print('l0 history: {}'.format(srvs[0].get_items().answer_history()))
        sel:survey.survey = rnd.choices(srvs,srvs.probabilities())[0]

    item_,item_question_text, item_answers_text, item_answers_values = sel.launch_random(all_zero_to_one=True)

    return item_, item_question_text

def eval_done():
    st.session_state.save_button_disabled = False

def make_closing():
    question_view.empty()
    next_button_view.empty()
    enumeration_view.empty()
    q_devider_b.empty()
    q_devider_t.empty()

    with results_view.container():
        l0_fig, l1_fig, l2_fig = make_graph()
        if l0_fig is not None:
            st.plotly_chart(l0_fig)
            if l1_fig is not None:
                st.plotly_chart(l1_fig)
                if l2_fig is not None:
                    st.plotly_chart(l2_fig)
        else:
            emojicols = st.columns([1,1,1])
            emojicols[1].write('# :astonished::confounded::sweat:')
            st.write('#### ¡Lo sentimos! Pero no hemos encontrado un hobby que se ajuste a tus preferencias.')
        st.write('##### {}'.format('Evalúa el desempeño del modelo:'))

        opts = np.arange(0,105,5)
        
        eval_value = st.select_slider(
            'eval',label_visibility='hidden',
            options=opts,format_func = get_eval_label,value = 50,key='eval_slider',on_change=eval_done)
        
        comment_text = st.text_input('Comentario (opcional):','',50,key='comment_text',on_change=eval_done)

        closing_instructions = st.caption('Por favor presiona el botón **:green["Guardar y enviar"]** para que tus resultados y evaluación sean tomados en cuenta de forma **anónima**. Si lo deseas puedes volver a tomar el cuestionario ya que el objetivo del estudio no es recaudar datos de hobbies sino evaluar el modelo.')

        save_eval_button = st.button('Guardar y enviar',disabled=st.session_state.save_button_disabled)
        button_instrucc = st.caption('Realiza un cambio en la evaluación o comentario para habilitar el botón de guardado. Una vez guardado el botón se deshabilitará y no podrás volver a enviar tu evaluación, pero puedes volver a tomar el cuestionario y enviar una nueva.')
        if save_eval_button:
            st.session_state.save_file += ('# EVALUATION: {}\n'.format(eval_value))
            st.session_state.save_file += ('# COMMENT: {}\n'.format(comment_text))
            gh_write(st.session_state.save_file)
            st.session_state.save_file = '# NEW ENTRY\n'
            st.session_state.save_button_disabled = True
            # st.write('Evaluación guardada. Por favor descarga tus resultados y envíalos a: [{0}](mailto:{0}?subject=[EPS%Response])'.format(DEFS.EMAIL))
            # st.download_button('Descargar resultados',data=st.session_state.save_file,file_name='resultados.csv',mime='text/csv')

def make_graph():
    all_l0 = np.array(s0).flatten()
    all_l1 = np.array(s1).flatten()
    all_l2 = np.array(s2).flatten()


    # l0
    # --------------------------------------------------------------------------------------------------------------------
    l0_hobbies_table = []
    for srv in all_l0:
        w = srv.get_weight()
        for i in range(len(w)):
            if w[i] > 0:
                l0_hobbies_table.append(['Preferencias generales: {}'.format(srv.categories[i]),round((w[i]/2)*100)])
    
    if len(l0_hobbies_table) == 0:
        l0_fig = None
    else:
        l0_hobbies_table = pd.DataFrame(l0_hobbies_table,columns=['Hobbie','Preferencia'])
        l0_fig = px.pie(l0_hobbies_table, values='Preferencia', names='Hobbie', title='Preferencias generales')

    # l1
    # --------------------------------------------------------------------------------------------------------------------
    l1_hobbies_table = []
    for srv in all_l1:
        w = srv.get_weight()
        for i in range(len(w)):
            if w[i] > 0:
                l1_hobbies_table.append(['{}: {}'.format(srv.name,srv.categories[i]),round((w[i]/2)*100)])
    
    if len(l1_hobbies_table) == 0:
        l1_fig = None
    else:
        l1_hobbies_table = pd.DataFrame(l1_hobbies_table,columns=['Hobbie','Preferencia'])
        l1_fig = px.pie(l1_hobbies_table, values='Preferencia', names='Hobbie', title='Preferencia por grupos')

    # l2
    # --------------------------------------------------------------------------------------------------------------------
    l2_hobbies_table = []
    for srv in all_l2:
        w = srv.get_weight()
        for i in range(len(w)):
            if w[i] > 0:
                l2_hobbies_table.append(['{}: {}'.format(srv.name,srv.categories[i]),round((w[i]/2)*100)])
    
    if len(l2_hobbies_table) == 0:
        l2_fig = None
    else:
        l2_hobbies_table = pd.DataFrame(l2_hobbies_table,columns=['Hobbie','Preferencia'])
        l2_fig = px.pie(l2_hobbies_table, values='Preferencia', names='Hobbie', title='Preferencia específicas')

    return l0_fig, l1_fig, l2_fig

def gh_write(text,file_path='EPS2023/records.csv'):
    r, rf,ft = gh_get_file(file_path)
    t = ft + text
    r.update_file(rf.path,'streamlit commit',t,rf.sha,branch='main')
    

def gh_get_file(file_path='EPS2023/records.csv'):
    repo = g.get_user().get_repo(GITHUB_REPO)
    repo_file = repo.get_contents(file_path)
    file_text = repo_file.decoded_content.decode()
    return repo, repo_file, file_text
# --------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------
# PAGE LOGIC:
# --------------------------------------------------------------------------------------------------------------------
title_view.title('Encuesta de hobbies')
enumeration_view.caption('<center> {}/{} </center>'.format(st.session_state.q_count,Q_AMT),True)


if st.session_state.q_count < Q_AMT:

    if st.session_state.current_item is None:
        generate_q()

    value = likert_question(question_view,st.session_state.current_item_question_text,st.session_state.current_item.launch_count)

    trigger = next_button_view.button('Siguiente')
    if trigger:
        answer_q(value)
        if st.session_state.q_count < Q_AMT:
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

st.sidebar.write('#### Debug info:')
st.sidebar.write('No tendance: {}'.format(st.session_state.no_tendence))
st.sidebar.write('Q count: {}'.format(st.session_state.q_count))
st.sidebar.write('Current item: {}'.format(st.session_state.current_item))
st.sidebar.write('Current item question text: {}'.format(st.session_state.current_item_question_text))
st.sidebar.write('Current surveys: {}'.format(st.session_state.current_surveys))
st.sidebar.write('Current surveys probabilities: {}'.format(st.session_state.current_surveys_probs))
st.sidebar.write('S0 history: {}'.format(s0[0].get_items().answer_history()))
# --------------------------------------------------------------------------------------------------------------------