import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

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
Use right menu to select operations

"""