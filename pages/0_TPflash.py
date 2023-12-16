import streamlit as st
import pandas as pd
import neqsim
from neqsim.thermo.thermoTools import fluidcreator, fluid_df, TPflash, dataFrame

pd.set_option('display.float_format', '{:.2E}'.format)

st.title('TP flash')
st.divider()

st.text("Set fluid composition:")

# Sample data for the DataFrame
default_data = {
    'ComponentName':  ["water", "MEG", "TEG", "nitrogen", "CO2", "methane", "ethane", "propane", "i-butane", "n-butane", "i-pentane", "n-pentane", "n-hexane", "C7", "C8", "C9", "C10", "C11", "C12", "C13", "C14", "C15", "C16", "C17", "C18", "C19", "C20"],
    'MolarComposition[-]':  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'MolarMass[kg/mol]': [None, None, None, None, None, None, None, None, None, None, None, None, None, 0.0913, 0.1041, 0.1188, 0.136, 0.150, 0.164, 0.179, 0.188, 0.204, 0.216, 0.236, 0.253, 0.27, 0.391],
    'RelativeDensity[-]': [None, None, None, None, None, None, None, None, None, None, None, None, None, 0.746, 0.768, 0.79, 0.787, 0.793, 0.804, 0.817, 0.83, 0.835, 0.843, 0.837, 0.84, 0.85, 0.877]
}

df = pd.DataFrame(default_data)
st.edited_df = st.data_editor(
    df,
    column_config={
        "ComponentName": "ComponentName",  # change the title
        "MolarComposition[-]": st.column_config.NumberColumn(
            "MolarComposition[-]", min_value=0, max_value=1.0, format="%f"
        ),
        "MolarMass[kg/mol]'": st.column_config.NumberColumn(
            "MolarMass[kg/mol]", min_value=1, max_value=10000, format="%f kg/mol"
        ),
        "Density[gr/cm3]": st.column_config.NumberColumn(
            "Density[gr/cm3]", min_value=1e-10, max_value=10.0, format="%f gr/cm3"
        ),
    },
num_rows='dynamic')

#st.write(df.style.format("{:.2}"))
#st.edited_df = st.data_editor(df, num_rows='dynamic')

st.text("Fluid composition will be normalized before simulation")

st.divider()

temp = st.number_input("Temperature (C)", min_value=-273.15, value=20.0)  # Default 20.0 C
pressure = st.number_input("Pressure (bara)", min_value=0.0, value=1.0)  # Default 1 bara

if st.button('Run'):
    neqsim_fluid = fluid_df(st.edited_df, lastIsPlusFraction=False, add_all_components=False).autoSelectModel()
    neqsim_fluid.setPressure(pressure, 'bara')
    neqsim_fluid.setTemperature(temp, 'C')
    TPflash(neqsim_fluid)
    st.success('Flash finished successfully!')
    st.subheader("Results:")
    results_df = st.data_editor(dataFrame(neqsim_fluid))
    st.divider()
    #compnames = ','.join(neqsim_fluid.getComponentNames())
    input = "give sources for equilibrium data for ", str(neqsim_fluid.getComponentNames()[0])
    openapitext = st.question(input)
    st.write(openapitext)

