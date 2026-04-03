# StreamlitExamples Development Notes

Streamlit samples and testing

Initial development on Windows. Using torchthenet account on github.

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
1. streamlit version

See: [https://docs.streamlit.io/knowledge-base/using-streamlit/how-upgrade-latest-version-streamlit](https://docs.streamlit.io/knowledge-base/using-streamlit/how-upgrade-latest-version-streamlit)

## TaskTracker

Read/write to json file. Respond to radio buttons.

Original code provided by mistral-small:22b but heavily modified.

## 2026-04-03 Set Up MacOS

Pulled project from github. Needed to add ssh key to account.

This project is significantly behind the current streamlit and ollama versions.
See if Claude Code can catch it back up.

### Step 1 - get streamlit and ollama working independently

python3 -m venv venv
source venv/bin/activate
pip install {package}
pip freeze > requirements.txt
pip install -r requirements.txt

Note: ensure .gitignore has the line venv/

test@mbp-pw5p StreamlitExamples % pip show ollama
WARNING: Package(s) not found: ollama
test@mbp-pw5p StreamlitExamples % source venv/bin/activate
(venv) test@mbp-pw5p StreamlitExamples % pip show ollama
Name: ollama
Version: 0.6.1
Summary: The official Python client for Ollama.
Home-page: <https://ollama.com>
Author:
Author-email: <hello@ollama.com>
License-Expression: MIT
Location: /Users/test/Documents/torchthenet/StreamlitExamples/venv/lib/python3.14/site-packages
Requires: httpx, pydantic
Required-by:
(venv) test@mbp-pw5p StreamlitExamples % pip show streamlit
Name: streamlit
Version: 1.56.0
Summary: A faster way to build and share data apps
Home-page: <https://streamlit.io>
Author:
Author-email: Snowflake Inc <hello@streamlit.io>
License-Expression: Apache-2.0
Location: /Users/test/Documents/torchthenet/StreamlitExamples/venv/lib/python3.14/site-packages
Requires: altair, blinker, cachetools, click, gitpython, numpy, packaging, pandas, pillow, protobuf, pyarrow, pydeck, requests, tenacity, toml, tornado, typing-extensions
Required-by:
(venv) test@mbp-pw5p StreamlitExamples %

Executed: streamlit hello

Opens Opera and displays hello world example.

### Step 2 - try to run claude offline using ollama launch claude

Test with qwen3.5? omnicoder? ministral-3?

Should look at the ollama library pages for the models and see. Or just test.

#### claude cli with ollama_qwen3.5_27b

ollama launch claude --model qwen3.5:27b -- --name ollama_qwen3.5_27b

Launches at office while offline. Woot!

Running on MBP 14 with ~25% CPU. Hard to tell how sluggish since only results display.

Test the apps to see which one to start updating.

* EchoBot.py - runs without errors
* FakeBot.py - runs without errors
* NavigationDemo.py - runs without throwing errors but not sure all functionality is there
* TaskTracker.py - runs without errors
* TestingUI.py - runs without errors (but not sure all functionality is there). Pylance does report two errors.
* TestingVision.py - runs without errors. The only app that uses Ollama.

All apps appear to work on MacOs without changes or upgrading code for new Streamlit or Ollama versions.

Execute apps using:

source venv/bin/activate
streamlit run {app.py}

Try resolving two formatting errors in TestingUI.py with offline Claude Clode.

First fix takes a while but eventually completes without internet. About 35 min?
Stalls on editing file. Can see the edit was made but Claude CLI still working.

Second fix took about 7 minutes.

After both fixes Claude launched the app which opens in Opera.
Claude may not be able to debug but still seems to recognize app launched without errors.
Manual check appears to demonstrate app works so issues are resolved.

Committed all changes to git, but will need to wait to push and sync repo.

#### claude cli with ollama_ministral-3_14b

ollama launch claude --model ministral-3:14b -- --name ollama_ministral-3_14b

Running 100% GPU with 15G size at 32k context.

The @TaskTracker.py app is very rudimetary. To execute the app activate the venv and then execute 'streamlit run TaskTracker.py'. Let's add some functionality. The user should have a way to add and delete tasks from the list. What do you suggest?

Runs 3 explore agents.
Takes ~52 minutes.
Resulting code throws error. Pasted back into prompt.
It also doesn't log task start/stop time anymore.
