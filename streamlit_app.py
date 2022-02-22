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

st.title('Codex')

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'Language',
    ('python', 'javascript')
)

st.write(pathlib.Path.home())

def make_prompt(query):
    return f"""# Python Short Queries to Code

## Dict to JSON String

### Short Query: python dict to json string
### Example Code:
```python
import json

# Make a dict
d = dict(a=1, b=2)

# Convert to JSON string
j = json.dumps(d)

# Print the JSON string
print(j)
```

### Short Query: ${query}
### Example Code:"""

def process_query(query):
    if len(query) == 0:
        return None

    prompt = make_prompt(query)

    completion = openai.Completion.create(
      engine="code-davinci-001",
      prompt=prompt,
      max_tokens=500,
    )

    choice_0 = completion.choices[0].text;

    return choice_0

txt = st.text_area('Code Query', '', height=50)

st.write('Sentiment:', process_query(txt))

