import streamlit as st
import pandas as pd
import neqsim
from neqsim.thermo import fluid_df, phaseenvelope, TPflash, dataFrame
from neqsim import jNeqSim
import matplotlib.pyplot as plt

st.title('Phase Envelope')

st.text("Set fluid composition:")
# Sample data for the DataFrame
default_data = {
    'ComponentName':  ["nitrogen", "CO2", "methane", "ethane", "propane", "i-butane", "n-butane", "i-pentane", "n-pentane", "n-hexane", "benzene", "c-hexane", "n-heptane", "c-C7", "toluene","n-octane", "m-Xylene","c-C8","n-nonane","nC10","nC11","nC12", "C7", "C8", "C9", "C10", "C11", "C12", "C13", "C14", "C15", "C16", "C17", "C18", "C19", "C20"],
    'MolarComposition[-]':  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'MolarMass[kg/mol]': [None, None, None, None, None, None, None, None, None, None, None, None, None,None, None, None, None,None, None, None,None, None, 0.0913, 0.1041, 0.1188, 0.136, 0.150, 0.164, 0.179, 0.188, 0.204, 0.216, 0.236, 0.253, 0.27, 0.391],
    'RelativeDensity[-]': [None, None, None, None, None, None, None, None, None, None, None, None, None,None, None, None, None,None, None, None,None, None, 0.746, 0.768, 0.79, 0.787, 0.793, 0.804, 0.817, 0.83, 0.835, 0.843, 0.837, 0.84, 0.85, 0.877]
}

df = pd.DataFrame(default_data)
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

if st.button('Run'):
    neqsim_fluid = fluid_df(st.edited_df, lastIsPlusFraction=isplusfluid, add_all_components=False).setModel("UMR-PRU-EoS")
    st.success('Successfully created fluid')
    st.subheader("Results:")
    thermoOps = jNeqSim.thermodynamicOperations.ThermodynamicOperations(neqsim_fluid)
    thermoOps.calcPTphaseEnvelope()
    fig, ax = plt.subplots()
    dewts = [x-273.15 for x in list(thermoOps.getOperation().get("dewT"))]
    dewps = list(thermoOps.getOperation().get("dewP"))
    bubts = [x-273.15 for x in list(thermoOps.getOperation().get("bubT"))]
    bubps = list(thermoOps.getOperation().get("bubP"))
    plt.plot(dewts,dewps, label="dew point")
    plt.plot(bubts, bubps, label="bubble point")
    plt.title('PT envelope')
    plt.xlabel('Temperature [C]')
    plt.ylabel('Pressure [bar]')
    plt.legend()
    st.pyplot(fig)
    st.divider()
    cricobar = thermoOps.getOperation().get("cricondenbar")[1]
    st.write('cricondenbar ', cricobar, ' bara')
    dewdatapoints = pd.DataFrame(
    {'dew temperatures': dewts,
     'dew pressures':dewps,
    }
    )
    bubdatapoints = pd.DataFrame(
    {'bub temperatures': bubts,
     'bub pressures':bubps,
    }
    )
    st.divider()
    st.write('dew points')
    st.data_editor(dewdatapoints)
    st.write('bubble points')
    st.data_editor(bubdatapoints)
