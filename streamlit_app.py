import os
import openai

from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES

import pathlib

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

generated_code = ""
code_query = ""

examples = {
    "golang": [
        "iterate over array",
        "create dict with keys 0 to 10",
        "read JSON file as dict"
    ],
    "python": [
        "yaml file to dict",
        "get time delta as json"
    ],
    "javscript": [
        "iterate over object"
    ],
    "typescript": [
        "define interface",
    ],
}

# -----------------------------

st.title('Query to Code')

'''
_Made by [@eriknomitch](https://twitter.com/eriknomitch)_

You're using my OpenAI API key so don't abuse the service. Contact me if you need to use it for something else.
'''

# Add a selectbox to the sidebar:
language = st.sidebar.selectbox(
    'Language',
    ('golang', 'python', 'javascript', 'typescript')
)

# st.text(language)

# st.write(pathlib.Path.home())

def make_prompt(query):
    # return f"""Given this query, what would be the top result from StackOverflow for it?
    return f"""Given this query, give example code that explains the answer to the query in the most concise way possible. The example code should import any libraries used in it.

Query: {query}
Code (with comments): ```{language}
"""

def format_for_output(completion):
    return f"```go\n{completion}```"

def process_query(query):
    if len(query) == 0:
        return None

    prompt = make_prompt(query)

    completion = openai.Completion.create(
        engine="code-davinci-002",
        prompt=prompt,
        max_tokens=500,
        stop=["```"],
        temperature=0
    )

    choice_0 = completion.choices[0].text;

    return choice_0

def run_output(query):
    global generated_code

    query = query.strip()

    if len(query) == 0:
        return None

    completion = process_query(query)

    if completion is None:
        return None

    generated_code = completion.strip()

    return generated_code

def run_example(example):
    global code_query

    #run_output(example)

with st.expander("Examples"):
    # '''

    # > get time delta as JSON
    # '''
    '''
    _Tip:_ Try using a query that you'd usually Google for.

    '''

    for example in examples[language]:
        #st.button(example, on_click=lambda: run_example(example))
        st.text(example)

code_query = st.text_area('Code Query', value=code_query, height=50, key='code_query', placeholder=f"Enter a query that describes {language} code...")

if code_query != "":
    run_output(code_query)

# Spawn a new Ace editor
# content = st_ace(value=generated_code, readonly=True, language="python", theme="monokai")

if generated_code != "":
    st.markdown(format_for_output(generated_code))

# Display editor's content as you type
#content

# components.iframe("https://replit.com/@replit/Python", width=1000, height=800)


