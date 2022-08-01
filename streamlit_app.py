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

# -----------------------------

st.title('Query to Code')

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'Language',
    ('python', 'javascript')
)

# st.write(pathlib.Path.home())

def make_prompt(query):
    # return f"""Given this query, what would be the top result from StackOverflow for it?
    return f"""Given this query, give example code that explains the answer to the query in the most concise way possible. The example code should import any libraries used in it.

Query: {query}
Code (with comments): ```python"""

# def make_prompt(query):
#     return f"""# Python Short Queries to Code

# ## Dict to JSON String

# ### Short Query: python dict to json string
# ### Example Code:
# ```python
# import json

# # Make a dict
# d = dict(a=1, b=2)

# # Convert to JSON string
# j = json.dumps(d)

# # Print the JSON string
# print(j)
# ```

# ### Short Query: ${query}
# ### Example Code:"""

def format_for_output(completion):
    return f"```python\n{completion}```"

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

txt = st.text_area('Code Query', '', height=50)

def run_output(query):
    global generated_code

    if len(query) == 0:
        return None

    completion = process_query(query)

    generated_code = completion.strip()

    if completion is None:
        return None

    return format_for_output(completion)

st.write(run_output(txt))

# # Spawn a new Ace editor
# content = st_ace(value=generated_code, readonly=True, language="python")

# # Display editor's content as you type
# content

# components.iframe("https://replit.com/@replit/Python", width=1000, height=800)


