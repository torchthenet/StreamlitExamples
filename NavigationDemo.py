# -*- coding: utf-8 -*-
""" Demonstrate and test different Streamlit features
"""
#https://docs.streamlit.io/develop/api-reference/navigation/st.navigation
import streamlit as st

def create_account():
    st.header('Create Account')

def manage_account():
    st.header('Manage Account')
    tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])
    with tab1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

def learn():
    st.header('Learn')
    button_cols=st.columns(2,vertical_alignment='center')
    show_session_state_btn=button_cols[0].button(
            'Session State',
            help="Show session state values",
            use_container_width=True)
    reset_module_btn=button_cols[1].button(
            'Reset',
            help="Reset session state values",
            use_container_width=True)
    if show_session_state_btn:
        ShowSessionState()
    if reset_module_btn:
        ResetModule()

def ShowSessionState():
    """ Dump the session state 
    """
    st.write('### Show Session State')
    for k in st.session_state.keys():
        with st.expander(
                    label='st.session_state['+k+']',
                    expanded=False,
                    icon=':material/stylus:'):
            st.write(st.session_state[k])

def ResetModule():
    """ This does the same as a browser refresh
    """
    st.write('### Reset Module')
    for k in st.session_state.keys():
        del st.session_state[k]
    st.write('Application State Was Reset :material/reset_settings:')

def demo():
    """ Demo and test Streamlit components
    """
    st.header('Demo')
    # https://docs.streamlit.io/develop/api-reference/status
    button_cols=st.columns(5,vertical_alignment='center')
    success_btn=button_cols[0].button(
            'Success',
            help="Demonstrate the success callout",
            use_container_width=True)
    info_btn=button_cols[1].button(
            'Info',
            help="Demonstrate the info callout",
            use_container_width=True)
    warn_btn=button_cols[2].button(
            'Warn',
            help="Demonstrate the warn callout",
            use_container_width=True)
    err_btn=button_cols[3].button(
            'Error',
            help="Demonstrate the error callout",
            use_container_width=True)
    exception_btn=button_cols[4].button(
            'Exception',
            help="Demonstrate the exception callout",
            use_container_width=True)
    if success_btn:
        st.success('A :blue[success] message!',icon=':material/thumb_up:')
    if info_btn:
        st.info('An :green[info] message!',icon=':material/info:')
    if warn_btn:
        st.warning('A :orange[warn] message!',icon=':material/warning:')
    if err_btn:
        st.error('An :red[error] message!',icon=':material/report:')
    if exception_btn:
        st.exception('This is an exception message!')
    # https://docs.streamlit.io/develop/api-reference/layout
    button_cols=st.columns(5,vertical_alignment='center')
    modal_btn=button_cols[0].button(
            'Modal Dialog',
            help="Demonstrate a modal dialog",
            use_container_width=True)
    popover_btn=button_cols[1].button(
            'Popover',
            help="Demonstrate a popover",
            use_container_width=True)
    toast_btn=button_cols[2].button(
            'Toast',
            help="Demonstrate a toast",
            use_container_width=True)
    if modal_btn:
        DemonstrationDialog()
    if popover_btn:
        with st.popover('Demonstrate Popover',help='This is a popover'):
            st.write(':blue[Popover] message')
    if toast_btn:
        st.toast('This is a :red[toast]!',icon=':material/bolt:')
    # https://docs.streamlit.io/develop/api-reference/widgets/st.segmented_control
    option_map = {
        0: ":material/add:",
        1: ":material/zoom_in:",
        2: ":material/zoom_out:",
        3: ":material/zoom_out_map:",
    }
    selection = st.segmented_control(
        "Tool",
        options=option_map.keys(),
        format_func=lambda option: option_map[option],
        selection_mode="single",
    )
    # TODO: demonstrate invoking a function from selection
    st.write(
        "Your selected option: "
        f"{None if selection is None else option_map[selection]}"
    )
    # Work on file and directory selection
    button_cols=st.columns(5,vertical_alignment='center')
    select_file_btn=button_cols[0].button(
            'Select File',
            help='Select a file',
            use_container_width=True)
    select_dir_btn=button_cols[1].button(
            'Select Directory',
            help='Select a directory',
            use_container_width=True)
    if 'uploaded_files' not in st.session_state:
        st.session_state['uploaded_files']='No files selected yet'
    if select_file_btn:
        select_file()
    if select_dir_btn:
        pass

@st.dialog('File Selection Dialog')
def select_file():
    """ Select a single, existing file from the local filesystem.
    This uses the Streamlit st.file_uploader feature.
    There is no way to clear the list of selected files.
    Putting this in a modal dialog allows the list to be cleared.
    The filename list is saved in st.session_state.
    While st.file_uploader returns a list of file-like objects, this list is
    released when the dialog exits.
    Saving the list in a session_state variable doesn't work.
    The solution is to make a deep copy of the list.
    """
    files = st.file_uploader("Choose JSON files",
                             type='json',
                             accept_multiple_files=True,
                             help='Pick one or more .json files to upload')
    if len(files):
        st.session_state['uploaded_files']=list()
        for file in files:
            st.session_state['uploaded_files'].append(file)
        for file in st.session_state['uploaded_files']:
            st.write('Filename: ', file.name)
    st.write('Press :red[CLOSE] to exit')
    if st.button('CLOSE'): st.rerun()

def select_dir():
    """ Select a single, existing directory from the local filesystem.
    There isn't a Streamlit feature to do this.
    Options are to use TclTk, or win32, or PowerShell?
    """
    pass

@st.dialog('Demonstration Dialog')
def DemonstrationDialog():
    st.write('Press :red[Close]')
    if st.button('Close'):
        st.rerun()

# can't use shortcodes so copy and paste the images from
# https://share.streamlit.io/streamlit/emoji-shortcodes
# 1 = ":one:", 2 = ":two:", ...
# debug = ":beetle:", reset = ":sparkles:"
# Or use Google Material font (limited to b&w)
pages = {
    "Your account": [
        st.Page(create_account, title="Create your account",icon=":material/favorite:"),
        st.Page(manage_account, title="Manage your account"),
    ],
    "Resources": [
        st.Page(learn, title="Learn about us"),
        st.Page(demo, title="Demonstrations"),
    ],
}

# See https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config
# Choose page icon from one of the following:
#  https://share.streamlit.io/streamlit/emoji-shortcodes
#  https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded 
st.set_page_config(
        page_title='Navigation',
        page_icon=':material/smart_toy:',
        layout='wide',
        initial_sidebar_state='expanded',
        menu_items={
                'Get Help': None,
                'Report a bug': None,
                'About': '# Demo App',
                } )
pg = st.navigation(pages)
pg.run()

# vim: set expandtab tabstop=4 shiftwidth=4 autoindent: