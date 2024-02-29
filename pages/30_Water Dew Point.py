import streamlit as st
import pandas as pd
import neqsim
from neqsim.thermo.thermoTools import hydt,fluidcreator, fluid_df, TPflash, dataFrame
from fluids import default_fluid

st.title('Water Dew Point')
st.divider()
st.text("Set fluid composition:")

if 'activefluid_df' not in st.session_state:
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

pressure = st.number_input("Pressure (bara)", min_value=0.0, value=1.0)  # Default 1 bara

input_data = st.empty()
input_df = pd.DataFrame({'Pressure (bar)': [10], 'Water dew point (C)': 0.0, 'Hydrate temperature (C)': 0.0, 'Ice temperature (C)': 0.0})


# Button to trigger calculations
if st.button('Calc'):
    neqsim_fluid = fluid_df(st.edited_df, lastIsPlusFraction=isplusfluid, add_all_components=False).autoSelectModel()
    neqsim_fluid.setTemperature(0.0, 'C')
    TPflash(neqsim_fluid)
    for i in range(len(st.hydrate_df)):
        neqsim_fluid.setPressure(pressure)
        results = neqsim.thermo.dewt(neqsim_fluid)-273.15
        print(results)
        st.hydrate_df.at[i, 'Water dew point (C)'] = results
        hydresults = neqsim.thermo.hydt(neqsim_fluid)-273.15
        st.hydrate_df.at[i, 'Hydrate temperature (C)'] = hydresults
        neqsim.thermo.freeze(neqsim_fluid)
        freezet = neqsim_fluid.getTemperature('C')
        st.hydrate_df.at[i, 'Ice temperature (C)'] = freezet


st.hydrate_df
