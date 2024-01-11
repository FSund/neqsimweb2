import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import openai
from openai import OpenAI



def make_request(question_input: str):
    try:
        #API_KEY = st.secrets["apipas"]
        #OpenAI.api_key = API_KEY
        OpenAI.api_key = openai_api_key
        client = OpenAI(api_key=openai_api_key)
    except:
        st.write('no OPENAI key given..')
    try:
        completion = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=question_input,
        max_tokens=500,
        temperature=0
        )
        return completion.choices[0].text
    except:
        return ""

st.set_page_config(page_title="NeqSim", page_icon='images/neqsimlogocircleflat.png')

st.image('images/neqsimlogocircleflat.png', width=150)

st.write("# Welcome to NeqSim! 👋")

"""
NeqSim is a library for calculation of fluid behavior, phase equilibrium and process simulation. This this project is a collectiomn of Streamlit models using neqsim for simulation.The method documentation for the models found in this application can be found in [Introduction to Gas Processing using NeqSim in Colab](https://colab.research.google.com/github/EvenSol/NeqSim-Colab/blob/master/notebooks/examples_of_NeqSim_in_Colab.ipynb).

## NeqSim project in GitHub
The NeqSim library is written in the Java programming language. The source code and libraries are hosted in GitHub.

* [NeqSim Java](https://github.com/equinor/neqsim)

## NeqSim discussion
Questions related to use and development are asked on the [NeqSim github discussions](https://github.com/equinor/neqsim/discussions) page.

## How to use this application
Use left menu to select operations


## NeqSim Chatbot
NeqSim Streamlit is integrated with OpenAI, and will provide information related to the simulations. To use this option an OpenAI key  must be entered in the left menu.
"""

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
st.make_request = make_request