import streamlit as st
import numpy as np

def get_label(float_number):
    if float_number == 0.0:
        return 'Neutral'
    elif float_number == -2.0:
        return 'Totalmente en desacuerdo'
    elif float_number == 2.0:
        return 'Totalmente de acuerdo'
    elif float_number < 0:
        return '{}% en desacuerdo'.format(round(abs(float_number/2)*100))
    elif float_number > 0:
        return '{}% de acuerdo'.format(round(abs(float_number/2)*100))
    else:
        return ''

def get_eval_label(float_number):
    if float_number == 50:
        return 'Neutral'
    elif float_number == 0:
        return 'Nada certero'
    elif float_number == 100:
        return 'Totalmente certero'
    else:
        return '{}% de certeza'.format(float_number)
    
def likert_question(view=st,question:str = '',l_count:int = 0):

    with view.container():

        opts = np.arange(-2.,2.1,0.1)
        opts = np.round(opts,2)

        st.write('##### {}'.format(question),)

        value = st.select_slider(
            question,label_visibility='hidden',
            options=opts,format_func = get_label,value = 0.0,key='{}_{}'.format(question,l_count))

        return value