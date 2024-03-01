import streamlit as st
from neqsim.thermo import fluid
from neqsim import jNeqSim
import pandas as pd
from fluids import lng_fluid
from neqsim.thermo.thermoTools import fluid_df
from io import BytesIO

# Streamlit page configuration
st.title('LNG Ageing Simulation')
st.divider()
st.text("Set fluid composition:")

if 'activefluid_df' not in st.session_state  or 'activefluid_name' not in st.session_state or st.session_state.activefluid_name != 'lng_fluid':
   st.session_state.activefluid_name = 'lng_fluid'
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

# LNG Ageing Simulation Parameters
st.subheader('LNG Ageing Simulation Parameters')
pressure_transport = st.number_input('Transport Pressure (bara)', min_value=0.0, value=1.01325)
volume_initial = st.number_input('Initial Volume (m3)', min_value=0.0, value=120000.0)
BOR = st.number_input('Boil-off Rate (%)', min_value=0.0, value=0.15)
time_transport = st.number_input('Transport Time (hours)', min_value=0.0, value=24.0)
standard_version = st.selectbox(
    'ISO6976 standard version:',
    ('2004', '2016'),
    index=1  # Default to the second option, which is '2016'
)
energy_ref_temp = st.selectbox(
    'ISO6976 energy reference temperature:',
    (0, 15, 15.55, 20),
    index=1  # Default to the second option, which is '2016'
)
volume_ref_temp = st.selectbox(
    'ISO6976 volume reference temperature:',
    (0, 15, 15.55, 20),
    index=1  # Default to the second option, which is '2016'
)
if st.button('Simulate Ageing'):
    # Create fluid from user input
    fluid = fluid_df(st.edited_df).autoSelectModel()
    fluid.setPressure(pressure_transport, 'bara')
    fluid.setTemperature(-160.0, "C")  # setting a guessed initial temperature
    
    # Creating ship system for LNG ageing
    ship = jNeqSim.fluidMechanics.flowSystem.twoPhaseFlowSystem.shipSystem.LNGship(fluid, volume_initial, BOR / 100.0)
    ship.useStandardVersion("", standard_version)
    ship.getStandardISO6976().setEnergyRefT(energy_ref_temp)
    ship.getStandardISO6976().setVolRefT(volume_ref_temp)
    ship.setEndTime(time_transport)
    ship.createSystem()
    ship.solveSteadyState(0)
    ship.solveTransient(0)
    ageingresults = ship.getResults("temp")

    ageingresults = ship.getResults("temp")
    # Assuming ageingresults is already obtained from the simulation
    results = ageingresults[1:]  # Data rows
    columns = ageingresults[0]   # Column headers

    # Clean the column names to ensure uniqueness and handle empty or None values
    cleaned_columns = []
    seen = set()
    for i, col in enumerate(columns):
        new_col = col if col not in (None, '') else f"Unnamed_{i}"
        if new_col in seen:
            new_col = f"{new_col}_{i}"
        seen.add(new_col)
        cleaned_columns.append(new_col)

    # Creating DataFrame from results with cleaned column names
    resultsDF = pd.DataFrame([[float(str(j).replace(',', '')) for j in i] for i in results], columns=cleaned_columns)
    resultsDF.columns = ['time', 'temperature','GCV','WI','density','volume','C1','C2','C3','iC4','nC4','iC5','nC5','C6','N2','energy', 'GCV_mass', 'gC1','gC2','gC3','giC4','gnC4','giC5','gnC5','gC6','gN2']

    # Display the DataFrame
    print(resultsDF.head())  # or use st.dataframe(resultsDF) in Streamlit

    # Displaying the results DataFrame in Streamlit
    st.subheader('Ageing Simulation Results')
    st.dataframe(resultsDF)

    # Function to convert DataFrame to Excel and offer download
    def convert_df_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        processed_data = output.getvalue()
        return processed_data

    # Download button for the results in Excel format
    # if st.button('Download Results as Excel'):
    excel_data = convert_df_to_excel(resultsDF)
    st.download_button(label='📥 Download Excel',
                    data=excel_data,
                    file_name='lng_ageing_results.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
