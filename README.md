# StreamlitExamples

Streamlit samples and testing

## EchoBot

Example bot from Streamlit tutorial. Uses chatbot interface to echo back anything the user enters.

Demonstrates use of st.chat_input, st.chat_message, and st.chat_message.markdown.

## FakeBot

Another example bot from the Streamlit tutorial. This randomly selects a response from a list.

Demonstrates st.write_stream to display response as it is generated.

Modified to use __main__, added more responses to list, added st.set_page_config.

## NavigationDemo

Demo of page navigation and other components.

Started as st.navigation example code, then kept adding demo of other components.

Note: An error that module Streamlit does not contain an object indicates Streamlit is outdated.

To update Streamlit:

1. conda activate <environment_name>
1. conda update -c conda-forge streamlit -y
1. streamlist version

See: [https://docs.streamlit.io/knowledge-base/using-streamlit/how-upgrade-latest-version-streamlit](https://docs.streamlit.io/knowledge-base/using-streamlit/how-upgrade-latest-version-streamlit)

## TaskTracker

Read/write to json file. Respond to radio buttons.

Original code provided by mistral-small:22b but heavily modified.
