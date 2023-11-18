import streamlit as st
import pandas as pd
import neqsim
from neqsim.thermo.thermoTools import fluidcreator, fluid_df, TPflash, dataFrame

st.title('Create Fluid')

# Sample data for the DataFrame
default_data = {
    'ComponentName':  ["nitrogen", "CO2", "methane", "ethane", "propane", "i-butane", "n-butane", "i-pentane", "n-pentane", "n-hexane", "C7", "C8", "C9", "C10", "C11", "C12", "C13", "C14", "C15", "C16", "C17", "C18", "C19", "C20"],
    'MolarComposition[-]':  [0.53, 3.3, 72.98, 7.68, 4.1, 0.7, 1.42, 0.54, 0.67, 0.85, 1.33, 1.33, 0.78, 0.61, 0.42, 0.33, 0.42, 0.24, 0.3, 0.17, 0.21, 0.15, 0.15, 0.8],
    'MolarMass[kg/mol]': [None, None, None, None, None, None, None, None, None, None, 0.0913, 0.1041, 0.1188, 0.136, 0.150, 0.164, 0.179, 0.188, 0.204, 0.216, 0.236, 0.253, 0.27, 0.391],
    'RelativeDensity[-]': [None, None, None, None, None, None, None, None, None, None, 0.746, 0.768, 0.79, 0.787, 0.793, 0.804, 0.817, 0.83, 0.835, 0.843, 0.837, 0.84, 0.85, 0.877]
}

df = pd.DataFrame(default_data)

st.edited_df = st.data_editor(df, num_rows='dynamic')
st.edited_df.loc[-1] = ['water', 1.0,None,None]

if st.button('Create'):
    st.neqsim_fluid = fluid_df(st.edited_df, lastIsPlusFraction=False).autoSelectModel()
    st.success('Successfully created fluid')
