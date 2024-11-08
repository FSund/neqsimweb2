import streamlit as st
import pandas as pd
import neqsim
import uuid
import logging
from neqsim.thermo import fluid_df, phaseenvelope, TPflash, dataFrame
from neqsim import jneqsim
import matplotlib.pyplot as plt
from fluids import detailedHC_data

logger = logging.getLogger(__name__)

st.title('Phase envelope')

st.markdown("""
NeqSim has several options for calculating the phase envelope. 

- The UMR-PRU-EoS is a predictive equation of state that combines the PR EoS 
with an original UNIFAC-type model for the excess Gibbs energy (GE), through the 
universal mixing rules (UMR). The model is called UMR-PRU (Universal Mixing 
Rule Peng Robinson UNIFAC) and it is an accurate model for calculation of 
cricondenbar and hydrocarbon dew points.
""")

kelvin_to_celsius = 273.15

st.header("Input")

# docs: https://htmlpreview.github.io/?https://raw.githubusercontent.com/equinor/neqsimhome/master/javadoc/site/apidocs/neqsim/thermo/system/package-summary.html
# more docs: https://github.com/equinor/neqsim-python/blob/d9f886ec189950f797caa0e0fc30303efb4fef66/src/neqsim/thermo/thermoTools.py#L285
valid_systems = [
    "UMR-PRU-EoS",
    "SRK-EoS",
    "SRK-Peneloux-EoS",
]
if 'model_name' not in st.session_state:
    st.session_state.model_name = None

model_name = st.session_state.model_name

# st.subheader("System")
st.markdown("""
Thermodynamic system and mixing rules
""")
st.session_state.model_name = st.selectbox(
    "System",
    valid_systems, 
    label_visibility="collapsed",
    index=valid_systems.index(model_name) if model_name in valid_systems else 0,
)

# Sample data for the DataFrame

# st.text("Fluid composition")
st.markdown("""
Fluid composition
""")

def clear_composition(edf):
    # Change the key of the data editor to start over.
    st.session_state.df_editor_key = str(uuid.uuid4())

st.button("Clear composition", on_click=clear_composition)

if 'activefluid_df' not in st.session_state or st.session_state.activefluid_name != 'detailedHC_data':
   st.session_state.activefluid_name = 'detailedHC_data'
   st.session_state.activefluid_df = pd.DataFrame(detailedHC_data)

if 'df_editor_key' not in st.session_state:
    st.session_state.df_editor_key = str(uuid.uuid4())

edited_df = st.data_editor(
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
    num_rows='dynamic',
    key=st.session_state.df_editor_key,
)

# st.subheader("Fluid composition")
if 'isplusfluid' not in st.session_state:
    st.session_state.isplusfluid = False

st.checkbox(
    'Last component is "plus" fraction (i.e. C6+)',
    value=st.session_state.isplusfluid,
    on_change=lambda: st.session_state.update({'isplusfluid': not st.session_state.isplusfluid})
)

# usePR = st.checkbox('Peng Robinson EoS', help='use standard Peng Robinson EoS')

st.text("Fluid composition will be normalized before simulation")
st.divider()

composition_ok = edited_df['MolarComposition[-]'].sum() > 0
if st.button('Run', type="primary", disabled=not composition_ok):
    # modelname = "UMR-PRU-EoS"
    neqsim_fluid = fluid_df(
        edited_df, 
        modelName=model_name,
        lastIsPlusFraction=st.session_state.isplusfluid, 
        add_all_components=False
    )
    st.success('Successfully created fluid')
    st.subheader("Results:")
    thermoOps = jneqsim.thermodynamicoperations.ThermodynamicOperations(neqsim_fluid)
    thermoOps.calcPTphaseEnvelope2()
    logger.info(f"Calculated phase envelope using {model_name}")
    fig, ax = plt.subplots()
    dewts = [x - kelvin_to_celsius for x in list(thermoOps.getOperation().get("dewT"))]
    dewps = list(thermoOps.getOperation().get("dewP"))
    bubts = [x - kelvin_to_celsius for x in list(thermoOps.getOperation().get("bubT"))]
    bubps = list(thermoOps.getOperation().get("bubP"))
    plt.plot(dewts,dewps, label="dew point")
    plt.plot(bubts, bubps, label="bubble point")
    plt.title('PT envelope')
    plt.xlabel('Temperature [C]')
    plt.ylabel('Pressure [bara]')
    plt.legend()
    plt.grid(True)
    st.pyplot(fig)
    st.divider()
    cricobar = thermoOps.getOperation().get("cricondenbar")
    cricotherm = thermoOps.getOperation().get("cricondentherm")
    st.write(f"Model name \"{model_name}\"")
    st.write('cricondentherm ', round(cricotherm[1],2), ' bara, ',  round(cricotherm[0]-273.15,2), ' C')
    st.write('cricondenbar ', round(cricobar[1],2), ' bara, ', round(cricobar[0]-273.15,2), ' C')
    dewdatapoints = pd.DataFrame({
        'dew temperatures [C]': dewts,
        'dew pressures [bara]':dewps,
    })
    bubdatapoints = pd.DataFrame({
        'bub temperatures [C]': bubts,
        'bub pressures [bara]':bubps,
    })
    st.divider()
    st.write('dew points')
    st.data_editor(dewdatapoints)
    st.write('bubble points')
    st.data_editor(bubdatapoints)

if not composition_ok:
    # st.markdown("""
    # *The sum of Molar Composition must be greater than 0. Please adjust your inputs.*
    # """)
    st.error('The sum of Molar Composition must be greater than 0. Please adjust your inputs.')
