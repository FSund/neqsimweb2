import streamlit as st
import pandas as pd
import neqsim
from neqsim.thermo.thermoTools import fluidcreator, fluid_df, hydt, dataFrame
from fluids import default_fluid

st.title('Gas Hydrate Calculation')
st.divider()

st.text("Set fluid composition:")

df = pd.DataFrame(default_fluid)
st.edited_df = st.data_editor(
    df,
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
    neqsim_fluid = fluid_df(st.edited_df, lastIsPlusFraction=False, add_all_components=False).autoSelectModel()
    neqsim_fluid.setPressure(pressure, 'bara')
    hydt(neqsim_fluid)
    st.success('Hydrate calculation finished successfully!')
    st.text("Hydrate temperature " +str(round(neqsim_fluid.getTemperature('C'), 2)) + " [C]")
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
        openapitext = st.question(input)
        st.write(openapitext)
    except:
        st.write('OpenAI key needed for data analysis')