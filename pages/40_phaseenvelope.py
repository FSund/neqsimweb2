import streamlit as st
import pandas as pd
import neqsim
from neqsim.thermo import fluid_df, phaseenvelope, TPflash, dataFrame
from neqsim import jNeqSim
import matplotlib.pyplot as plt

st.title('Phase Envelope')

st.divider()

st.text("Set fluid composition:")

# Sample data for the DataFrame
default_data = {
    'ComponentName':  ["CO2", "methane", "ethane", "propane", "i-butane", "n-butane"],
    'MolarComposition[-]':  [0.01, 0.2, 0.1, 0.01, 0.01, 0.01],
}

df = pd.DataFrame(default_data)

st.edited_df = st.data_editor(df, num_rows='dynamic')

st.text("Fluid composition will be normalized before simulation")

st.divider()

if st.button('Run'):
    neqsim_fluid = fluid_df(st.edited_df).setModel("UMR-PRU-EoS")
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
