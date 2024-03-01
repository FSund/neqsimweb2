import streamlit as st
import pandas as pd
import neqsim
from neqsim.thermo.thermoTools import fluidcreator, fluid_df, TPflash, dataFrame
from fluids import default_fluid

st.title('Water Dew Point')
st.divider()
st.text("Set fluid composition:")

if 'activefluid_df' not in st.session_state or st.session_state.activefluid_name != 'default_fluid':
    st.session_state.activefluid_name = 'default_fluid'
    activefluid_df = pd.DataFrame(default_fluid)

hidecomponents = st.checkbox('Show active components')

if hidecomponents:
    activefluid_df =  st.edited_df[st.edited_df['MolarComposition[-]'] > 0]

st.edited_df = st.data_editor(
    activefluid_df,
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
isplusfluid = st.checkbox('Plus Fluid')

st.text("Fluid composition will be normalized before simulation")
st.divider()

input_data = st.empty()
input_df = pd.DataFrame({'Pressure (bar)': [10], 'Water dew point (C)': 0.0})
st.hydrate_df = st.data_editor(
    input_df,num_rows='dynamic')


# Button to trigger calculations
if st.button('Calc'):
    neqsim_fluid = fluid_df(st.edited_df, lastIsPlusFraction=isplusfluid, add_all_components=False).autoSelectModel()
    neqsim_fluid.setTemperature(0.0, 'C')
    TPflash(neqsim_fluid)
    for i in range(len(st.hydrate_df)):
        pressure = st.hydrate_df.at[i, 'Pressure (bar)']
        neqsim_fluid.setPressure(pressure)
        results = neqsim.thermo.dewt(neqsim_fluid)-273.15
        print(results)
        st.hydrate_df.at[i, 'Water dew point (C)'] = results

st.hydrate_df
