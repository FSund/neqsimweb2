import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import logging

logger = logging.getLogger(__name__)

st.set_page_config(page_title="NeqSim", page_icon='images/neqsimlogocircleflat.png')

st.image('images/neqsimlogocircleflat.png', width=150)

st.write("# Welcome to the NeqSim Simulation Platform! 👋")

"""
## About NeqSim
NeqSim (Non-equilibrium Simulator) is a library for the simulation of fluid behavior, phase equilibrium, and process systems.

## Getting Started
Use the left-hand menu to select the desired simulation or process. Enter any required inputs, and NeqSim will handle the calculations.
"""
