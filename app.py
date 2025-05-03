# -*- coding: utf-8 -*-
""" Test app to try out different interface options.
"""
import streamlit as st
import json
import re

def ChatbotModule():
    """ The main chatbot module.
    Only when this module is selected will the sidebar show
    - Prompt edit mode
    - Clipboard mode
    - Multi-session mode
    """
    # Provide a toggle to enable editing the prompt
    editor_mode=st.sidebar.toggle(
            label='Prompt Edit Mode',
            value=False,
            help='Enable mode to simplify editing prompt entry.',
            key='editor_mode')
    # Provide a toggle to enable copy to clipboard mode
    copy_mode=st.sidebar.toggle(
            label='Clipboard Mode',
            value=False,
            help='Enable mode to add a copy to clipboard icon on messages.',
            key='clipboard_mode')
    # Provide a toggle to enable multi-session mode
    multi_mode=st.sidebar.toggle(
            label='Multi-Session Mode',
            value=False,
            help='Enable mode to allow multiple chat sessions.',
            key='multi_mode')
    st.markdown('### Chatbot Module')
    st.divider()    
    button_cols=st.columns(2,vertical_alignment='bottom')
    # Load list of models
    model_list=["model1","model2","model3"]
    model=button_cols[0].selectbox(
            'Select Ollama Model',
            model_list,
            key='model_key')
    # Error: st.session_state.model_key cannot be modified after the widget with key model_key is instantiated.
    #st.session_state['model_key']=model
    # New Chat button
    button_cols[1].markdown('Start a new chat session')
    new_chat_btn=button_cols[1].button(
            'New Chat',
            help='Start a new chat',
            use_container_width=True)
    if new_chat_btn:
        if system_key in st.session_state.keys():
            del st.session_state[system_key]
        if messages_key in st.session_state.keys():
            del st.session_state[messages_key]
        if metrics_key in st.session_state.keys():
            del st.session_state[metrics_key]
        if session_log_key in st.session_state.keys():
            del st.session_state[session_log_key]
        if metrics_log_key in st.session_state.keys():
            del st.session_state[metrics_log_key]
        if prompt_key in st.session_state.keys():
            del st.session_state[prompt_key]
        st.rerun()
    if editor_mode:
        slider_cols=st.columns(3,vertical_alignment='center')
        generate_btn=slider_cols[2].button(
                'Submit',
                help='Submit prompt to large language model',
                use_container_width=True)
    else:
        slider_cols=st.columns(2,vertical_alignment='center')
    # Temperature Slider
    slider_cols[0].slider(
            label='Temperature',
            help='Adjust the randomness of the responses',
            value=0.1,
            min_value=0.0,
            max_value=1.0,
            step=0.1,
            key='cb_temperature')
    # Context Size Slider
    slider_cols[1].slider(
            label='Context token limit',
            help='Adjust the number of context tokens',
            value=2048,
            min_value=1024,
            max_value=4096,
            step=1024,
            key='cb_context_size')

def WranglerModule():
    """ The wrangler module.
    Use this module for simple text wrangling.
    """
    st.markdown('### Wrangler Module')
    st.divider()
    if 'text_input' not in st.session_state.keys():
        st.session_state['text_input']=None
        st.session_state['text_output']=None
    with st.expander(label='Enter Text',
            expanded=True,
            icon=':material/person:'):
        st.session_state['text_input']=st.text_area(
                label='Enter text to edit',
                label_visibility='collapsed',
                placeholder='Enter text to edit',
                value=st.session_state['text_input'],
                height=500)
    # Display and handle the text processing buttons
    button_cols=st.columns(4,vertical_alignment='top')
    # First row of buttons
    input_btn=button_cols[0].button('Clear Input',use_container_width=True,help='Clear input text')
    if input_btn: st.session_state['text_input']=None
    output_btn=button_cols[1].button('Clear Output',use_container_width=True,help='Clear processed input')
    if output_btn: st.session_state['text_output']=None
    echo_btn=button_cols[2].button('Echo',use_container_width=True,help='Echo the input text')
    if echo_btn: st.session_state['text_output']=st.session_state['text_input']
    swap_btn=button_cols[3].button('Swap',use_container_width=True,help='Swap the input and output text')
    if swap_btn:
        temp_text=st.session_state['text_input']
        st.session_state['text_input']=st.session_state['text_output']
        st.session_state['text_output']=temp_text
        st.rerun()
    # Second row of buttons
    rev_char_btn=button_cols[0].button('Reverse Characters',use_container_width=True,help='Reverse the characters in the input text')
    if rev_char_btn and st.session_state['text_input']:
        st.session_state['text_output']=st.session_state['text_input'][::-1]
    rev_word_btn=button_cols[1].button('Reverse Words',use_container_width=True,help='Reverse the words in the input text')
    if rev_word_btn and st.session_state['text_input']:
        st.session_state['text_output']=' '.join(st.session_state['text_input'].split()[::-1])
    rev_line_btn=button_cols[2].button('Reverse Lines',use_container_width=True,help='Reverse the lines in the input text')
    if rev_line_btn and st.session_state['text_input']:
        st.session_state['text_output']='\n'.join(st.session_state['text_input'].splitlines()[::-1])
    column_btn=button_cols[3].button('Columnize',use_container_width=True,help='Convert the input text to a column format')
    if column_btn and st.session_state['text_input']:
        st.session_state['text_output']='\n'.join(st.session_state['text_input'].split()[::])
    # Third row of buttons
    rem_line_no_btn=button_cols[0].button('Remove Line Numbers',use_container_width=True,help='Remove leading line numbers from the input text')
    if rem_line_no_btn and st.session_state['text_input']:
        st.session_state['text_output']='\n'.join([line.split(' ')[1] for line in st.session_state['text_input'].splitlines() if line.split(' ')[0].isdigit()])
    rem_line_no_merged_btn=button_cols[1].button('Remove Merged Line Numbers',use_container_width=True,help='Remove line numbers merged into the input text')
    if rem_line_no_merged_btn and st.session_state['text_input']:
        RemoveMergedLineNumbers()
    rem_blank_btn=button_cols[2].button('Remove Blank Lines',use_container_width=True,help='Remove blank lines from the input text')
    if rem_blank_btn and st.session_state['text_input']:
        st.session_state['text_output']='\n'.join([line for line in st.session_state['text_input'].splitlines() if line.strip()])
    rem_return_btn=button_cols[3].button('Remove Returns',use_container_width=True,help='Remove returns from the input text')
    if rem_return_btn and st.session_state['text_input']:
        st.session_state['text_output']=st.session_state['text_input'].replace('\n',' ')
    st.divider()
    # Display and handle the output text viewing options
    st.write('Text Output Options')
    auto_col,text_col,code_col,edit_col=st.columns(4,vertical_alignment='center')
    auto_btn=auto_col.button(
            'Auto',
            help='Auto detect and display the processed text',
            use_container_width=True)
    text_btn=text_col.button(
            'Text',
            help='Display processed text in fixed width font and preseve line breaks',
            use_container_width=True)
    code_btn=code_col.button(
            'Code',
            help='Display processed text with copy to clipboard icon',
            use_container_width=True)
    edit_btn=edit_col.button(
            'Edit',
            help='Display processed text in editable text area',
            use_container_width=True)
    if auto_btn: st.session_state['output_format']='Auto'
    if text_btn: st.session_state['output_format']='Text'
    if code_btn: st.session_state['output_format']='Code'
    if edit_btn: st.session_state['output_format']='Edit'
    if 'output_format' not in st.session_state.keys():
        st.session_state['output_format']='Auto'
    #Show the processed text in the chosen format
    with st.expander(label='Processed Text: '+st.session_state['output_format'],
            expanded=True,
            icon=':material/smart_toy:'):
        match st.session_state['output_format']:
            case 'Auto': st.write(st.session_state['text_output'])
            case 'Text': st.text(st.session_state['text_output'])
            case 'Code': st.code(st.session_state['text_output'],language=None,wrap_lines=True)
            case 'Edit': st.session_state['text_output']=st.text_area(
                        label='Processed text',
                        label_visibility='collapsed',
                        placeholder='Processed text',
                        value=st.session_state['text_output'],
                        height=500)

def RemoveMergedLineNumbers():
    """ Remove line numbers that are merged into the text.
    First try to remove numbers at the beginning of each line.
    If some lines do not starte with a number, then search for a sequence of
    numbers mixed into the text and remove them, but leave any other numbers.
    """
    st.session_state['text_output']=str()
    lines=st.session_state['text_input'].splitlines()
    # Look for a number at the start of each line
    numbered_lines=True
    line_count=0
    for line in lines:
        line_count+=1
        if not re.search(r'^\b\d+\b',line):
            numbered_lines=False
            break
    if numbered_lines and line_count>2:
        for line in lines:
            words=line.split()
            if len(words)>1:
                words=words[1:]
            else:
                words=str()
            if len(words): 
                st.session_state['text_output']+=str(' ').join(words)+'\n'
    else:
    # Look for a sequence of numbers in the text
        RemoveEmbeddedNumberSequence()

def RemoveEmbeddedNumberSequence():
    """ Handle the case where a sequence of numbers is embedded in the text.
    Assume line numbers increment by 1.
    Look for a reasonable starting number, then process the text by removing
    an incrementing sequence of numbers. But leave other numbers in the text.
    """
    # Find all occurrences of integers in the input text
    # The pattern \b\d+\b matches one or more digits (\d+) surrounded by word boundaries (\b)
    # Found integers are converted from string to integers using a list comprehension
    integers=[int(num) for num in re.findall(r'\b\d+\b',st.session_state['text_input'])]
    # If there are no integers then give up
    if len(integers)==0:
        st.warning('No integers found in the input text!',icon=':material/warning:')
        st.session_state['text_output']=st.session_state['text_input']
        return
    # Iterate through the integers and look for a sequence of numbers
    # The sequence is defined as a list of integers that are in order and increment by 1
    found_sequence=False
    first_integer=0
    while not found_sequence:
        for int_0 in integers:
            int_1=int_0+1
            int_2=int_0+2
            if int_1 not in integers: continue
            if int_2 not in integers: continue
            if integers.index(int_0)<integers.index(int_1) and integers.index(int_1)<integers.index(int_2):
                first_integer=int_0
                found_sequence=True
                break
        break
    if not found_sequence:
        st.warning('No sequence of integers found in the input text!',icon=':material/warning:')
        st.session_state['text_output']=st.session_state['text_input']
        return
    # Now we have a sequence of integers, we can remove them from the text
    st.success(f'First line number is {first_integer}',icon=':material/thumb_up:')
    search_integer=first_integer
    for line in st.session_state['text_input'].splitlines():
        for word in line.split():
            try:
                if search_integer==int(word):
                    search_integer+=1
                else:
                    st.session_state['text_output']+=word+' '
            except ValueError:
                st.session_state['text_output']+=word+' '
        st.session_state['text_output']+='\n'

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
    st.markdown('### Debugging Module')
    st.divider()
    button_cols=st.columns(4,vertical_alignment='center')
    session_btn=button_cols[0].button(
            'Session State',
            help='View session state values',
            use_container_width=True)
    if session_btn: ShowSessionState()

def ShowSessionState():
    """ Dump the session state """
    st.write('### Show Session State')
    for k in st.session_state.keys():
        with st.expander(
                    label='st.session_state['+k+']',
                    expanded=True,
                    icon=':material/stylus:'):
            st.write(st.session_state[k])

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
            'Wrangler',
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
        case 'Wrangler': WranglerModule()
        case 'Restore': RestoreSessionLogs()
        case 'Debugging': DebuggingModule()
        case 'Reset': ResetModule()
        case _: st.write(':construction_worker: Something is broken.')
