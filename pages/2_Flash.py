import streamlit as st
import pandas as pd
import neqsim
from neqsim.thermo.thermoTools import fluidcreator, fluid_df, TPflash, dataFrame

st.title('Flash')

# Inputs for temperature and pressure
temp = st.number_input("Temperature (C)", min_value=0.0, value=20.0)  # Default 20.0 C
pressure = st.number_input("Pressure (bara)", min_value=0.0, value=1.0)  # Default 1 bara

if st.button('Run'):
    neqsim_fluid = fluid_df(st.edited_df, lastIsPlusFraction=False).autoSelectModel()
    neqsim_fluid.setPressure(pressure, 'bara')
    neqsim_fluid.setTemperature(temp, 'C')
    TPflash(neqsim_fluid)
    st.success('Flash finished successfully!')
    # Display the DataFrame using st.table
    st.subheader("Results Table:")
    results_df = st.data_editor(dataFrame(neqsim_fluid))