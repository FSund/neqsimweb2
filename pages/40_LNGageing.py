import streamlit as st
from neqsim.thermo import fluid
from neqsim import jNeqSim
import pandas as pd
from fluids import lng_fluid
from neqsim.thermo.thermoTools import fluid_df

# Streamlit page configuration
st.title('LNG Ageing Simulation')
st.divider()
st.text("Set fluid composition:")

if 'activefluid_df' not in st.session_state:
   st.session_state.activefluid_df = pd.DataFrame(lng_fluid)

hidecomponents = st.checkbox('Show active components')
if hidecomponents:
    st.session_state.activefluid_df =  st.edited_df[st.edited_df['MolarComposition[-]'] > 0]

st.edited_df = st.data_editor(
    st.session_state.activefluid_df,
    column_config={
        "ComponentName": "Component Name",
        "MolarComposition[-]": st.column_config.NumberColumn("Molar Composition [-]", min_value=0, max_value=10000, format="%f"),
        "MolarMass[kg/mol]": st.column_config.NumberColumn(
            "Molar Mass [kg/mol]", min_value=0, max_value=10000, format="%f kg/mol"
        ),
        "RelativeDensity[-]": st.column_config.NumberColumn(
            "Density [gr/cm3]", min_value=1e-10, max_value=10.0, format="%f gr/cm3"
        ),
    },
num_rows='dynamic')

st.text("Fluid composition will be normalized before simulation")
st.divider()

# User inputs
eosmodel = st.selectbox('Equation of State Model', ['SRK', 'PR'], index=1)
pressure_transport = st.number_input('Transport Pressure (bara)', min_value=0.0, value=1.01325)
volume_initial = st.number_input('Initial Volume (m3)', min_value=0.0, value=10000.0)
BOR = st.number_input('Boil-off Rate (%)', min_value=0.0, value=0.15)
refEnergyT = st.number_input('Reference Energy Temperature (C)', value=15.0)
refvolT = st.number_input('Reference Volume Temperature (C)', value=15.0)
time_transport = st.number_input('Transport Time (hours)', min_value=0.0, value=24.0)

# Create fluid from user input
fluid = fluid_df(st.edited_df).autoSelectModel()

# LNG Ageing Simulation Parameters
st.subheader('LNG Ageing Simulation Parameters')
pressure_transport = st.number_input('Transport Pressure (bara)', min_value=0.0, value=1.01325)
volume_initial = st.number_input('Initial Volume (m3)', min_value=0.0, value=10000.0)
BOR = st.number_input('Boil-off Rate (%)', min_value=0.0, value=0.15)
refEnergyT = st.number_input('Reference Energy Temperature (C)', value=15.0)
refvolT = st.number_input('Reference Volume Temperature (C)', value=15.0)
time_transport = st.number_input('Transport Time (hours)', min_value=0.0, value=24.0)

if st.button('Simulate Ageing'):
    fluid.setPressure(pressure_transport, 'bara')
    fluid.setTemperature(-160.0, "C")  # setting a guessed initial temperature
    
    # Creating ship system for LNG ageing
    ship = jNeqSim.fluidMechanics.flowSystem.twoPhaseFlowSystem.shipSystem.LNGship(fluid, volume_initial, BOR / 100.0)
    ship.useStandardVersion("", "2016")
    ship.getStandardISO6976().setEnergyRefT(refEnergyT)
    ship.getStandardISO6976().setVolRefT(refvolT)
    ship.setEndTime(time_transport)
    ship.createSystem()
    ship.solveSteadyState(0)
    ship.solveTransient(0)
    ageingresults = ship.getResults("temp")

    # Display results
    st.write('Ageing Results:')
    st.write(ageingresults)