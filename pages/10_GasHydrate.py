import streamlit as st
import pandas as pd
import neqsim
import time
from neqsim.thermo.thermoTools import fluidcreator, fluid_df, hydt, dataFrame
from fluids import default_fluid

st.title('Gas Hydrate Calculation')
st.divider()
st.text("Set fluid composition:")

if 'activefluid_df' not in st.session_state:
   st.session_state.activefluid_df = pd.DataFrame(default_fluid)

hidecomponents = st.checkbox('Show active components')

if hidecomponents:
    st.session_state.activefluid_df =  st.edited_df[st.edited_df['MolarComposition[-]'] > 0]

st.edited_df = st.data_editor(
    st.session_state.activefluid_df,
    column_config={
        "ComponentName": "Component Name",
        "MolarComposition[-]": st.column_config.NumberColumn(
        ),
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

if st.button('Run'):
    # Check if water's MolarComposition[-] is greater than 0
    water_row = st.edited_df[st.edited_df['ComponentName'] == 'water']  # Adjust 'ComponentName' and 'water' as necessary
    if not water_row.empty and water_row['MolarComposition[-]'].iloc[0] > 0:
        neqsim_fluid = fluid_df(st.edited_df, lastIsPlusFraction=False, add_all_components=False).autoSelectModel()
        neqsim_fluid.setPressure(pressure, 'bara')
        hydt(neqsim_fluid)  # Assuming 'hydt' is your method for hydrate calculation
        st.success('Hydrate calculation finished successfully!')
        st.text("Hydrate temperature " + str(round(neqsim_fluid.getTemperature('C'), 2)) + " [C]")
        st.subheader("Results:")
        results_df = st.data_editor(dataFrame(neqsim_fluid))
        st.divider()
        list1 = neqsim_fluid.getComponentNames()
        l1 = list(list1)
        string_list = [str(element) for element in l1]
        delimiter = ", "
        result_string = delimiter.join(string_list)
        try:
            input = "What scientific experimental hydrate equilibrium data are available for mixtures of " + result_string
            openapitext = st.make_request(input)
            st.write(openapitext)
        except:
            st.write('OpenAI key needed for data analysis')
    else:
        st.error('Water Molar Composition must be greater than 0. Please adjust your inputs.')

uploaded_file = st.sidebar.file_uploader("Import Fluid")
if uploaded_file is not None:
    st.session_state.activefluid_df = pd.read_csv(uploaded_file)
    check1 = st.sidebar.button("Set fluid")
else:
    st.session_state.activefluid_df = pd.DataFrame(default_fluid)
