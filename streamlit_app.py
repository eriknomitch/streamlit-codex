import os
import openai

from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import pathlib

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

st.title('Query to Code')

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'Language',
    ('python', 'javascript')
)

st.write(pathlib.Path.home())

def make_prompt(query):
    # return f"""Given this query, what would be the top result from StackOverflow for it?
    return f"""Given this query, give example code that explains the answer to the query in the most concise way possible. Add comments to explain the code.

Query: {query}
Code: ```python"""

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
        engine="code-davinci-001",
        prompt=prompt,
        max_tokens=500,
        stop=["```", "### Short Query:"],
        temperature=0
    )

    choice_0 = completion.choices[0].text;

    return choice_0

txt = st.text_area('Code Query', '', height=50)

def run_output(query):
    if len(query) == 0:
        return None

    completion = process_query(query)

    if completion is None:
        return None

    return format_for_output(completion)

st.write(run_output(txt))

