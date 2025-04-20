The following code was removed from Chatbot.py

def DemonstrationModule():
    """ Demo and test Streamlit components
    """
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

@st.dialog('Demonstration Dialog')
def DemonstrationDialog():
    st.write('Press :red[Close]')
    if st.button('Close'):
        st.rerun()

