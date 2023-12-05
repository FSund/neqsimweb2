import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import neqsim
from neqsim.thermo import fluid, TPflash

st.title('Methane Density Calculator')

temperature = st.number_input('Temperature (°C)', value=20.0)
pressure = st.number_input('Pressure (bar)', value=100.0)
calculate_button = st.button('Calculate Density')

if calculate_button:
    # Create a methane fluid
    methane_fluid = fluid('srk')  # or use 'pr' for Peng-Robinson EoS
    methane_fluid.addComponent('methane', 1.0)
    methane_fluid.setTemperature(temperature + 273.15)  # Convert to Kelvin
    methane_fluid.setPressure(pressure)

    # Perform a TP flash calculation
    TPflash(methane_fluid)
    methane_fluid.initProperties()
    # Calculate and display density
    density = methane_fluid.getDensity('kg/m3')
    st.write(f'Average density of fluid: {density:.2f} kg/m³')