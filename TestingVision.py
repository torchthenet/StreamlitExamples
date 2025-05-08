# -*- coding: utf-8 -*-
""" Test app to figure out vision models.
"""
import streamlit as st
import ollama
import json

def ChatbotModule():
    model_list=ollama.list()['models']
    for model in model_list:
        model_name=model['model']
        model_dict=ollama.show(model_name)
        model_capabilities=model_dict['capabilities']
        if 'vision' in model_capabilities:
            st.write('### Vision Model: ', model_name)
            st.divider()
            st.write('Model Capabilities: ', model_capabilities)
    pass

def RestoreSessionLogs():
    """ Restore the session and metrics lists from user provided log files.
    There is no check to see if the files are valid. """
    st.markdown('### Restore Session Logs')
    st.divider()
    st.markdown('Upload the session log file (ChatbotSession_*.log) and the metrics log file (ChatbotSession_*_metrics.log)')
    st.markdown('The session log file contains the chat history and the metrics log file contains the metrics for each response.')
    # Upload the session log file
    st.markdown('\n\nSession log file:')
    session_log_file=st.file_uploader(
            label='Upload a session log file',
            type='log',
            label_visibility='collapsed')
    # Upload the metrics log file
    st.markdown('Metrics log file:')
    metrics_log_file=st.file_uploader(
            label='Upload a metrics log file',
            type='log',
            label_visibility='collapsed')
    if session_log_file and metrics_log_file:
        # Read the session log file and restore the messages list
        st.session_state['cb_messages']=json.load(session_log_file)
        # Read the metrics log file and restore the metrics list
        st.session_state['cb_metrics']=json.load(metrics_log_file)
        st.write('Session restored.')

def DebuggingModule():
    """ Provide buttons to access debug views """
    st.write('## Debugging Module')
    st.divider()
    button_cols=st.columns(4,vertical_alignment='center')
    session_btn=button_cols[0].button(
            'Session State',
            help='View session state values',
            use_container_width=True)
    show_model_btn=button_cols[1].button(
            'Show Models',
            help='View current model information',
            use_container_width=True)
    list_models_btn=button_cols[2].button(
            'List Models',
            help='View available models',
            use_container_width=True)
    running_btn=button_cols[3].button(
            'Running Models',
            help='View running models',
            use_container_width=True)
    if session_btn: ShowSessionState()
    if show_model_btn: ShowAllModels()
    if list_models_btn: ListModels()
    if running_btn: ShowRunningModels()

def ShowSessionState():
    """ Dump the session state """
    st.write('### Show Session State')
    for k in st.session_state.keys():
        with st.expander(
                    label='st.session_state['+k+']',
                    expanded=True,
                    icon=':material/stylus:'):
            st.write(st.session_state[k])

def ShowAllModels():
    """ Show current model """
    st.write('### Show Current Models')
    model_list=ollama.list()['models']
    for model in model_list:
        model_name=model['model']
        with st.expander(
                    label=model_name,
                    expanded=False,
                    icon=':material/stylus:'):
            st.write(ollama.show(model['model']))

def ListModels():
    """ Show all available models """
    st.write('### List Available Models')
    model_list=ollama.list()
    st.write(model_list)
    return

def ShowRunningModels():
    """ Display models currently active in ollama """
    st.write('### Show Running Models')
    running_list=ollama.ps()
    st.write(running_list)

def ResetModule():
    """ This does the same as a browser refresh but preserves the log and sys_models. """
    st.write('### Reset Module')
    st.divider()
    for k in st.session_state.keys():
        if k == 'log':
            st.session_state['log'].info('Application reset - session_state cleared')
        elif k[:4] == 'sys_':
            pass
        else:
            del st.session_state[k]
    st.write('Application State Was Reset :material/reset_settings:')

if __name__=='__main__':
    # The Chatbot application.
    st.set_page_config(
            page_title='Chatbot',
            page_icon=':material/smart_toy:',
            layout='wide',
            initial_sidebar_state='expanded',
            menu_items={
                    'Get Help': None,
                    'Report a bug': None,
                    'About': '# Simple Chatbot for Ollama'
                    } )
    st.sidebar.header('Ollama Chatbot')
    module_list=(
            'Chatbot',
            'Restore',
            'Debugging',
            'Reset')
    module=st.sidebar.selectbox(
            'Select a module',
            module_list,
            key='module')
    # Run the selected module
    match module:
        case 'Chatbot': ChatbotModule()
        case 'Restore': RestoreSessionLogs()
        case 'Debugging': DebuggingModule()
        case 'Reset': ResetModule()
        case _: st.write(':construction_worker: Something is broken.')
