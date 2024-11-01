import streamlit as st
import pandas as pd
import neqsim
from neqsim.thermo.thermoTools import fluidcreator, fluid_df, TPflash, dataFrame, hydt, waterdewt
from fluids import default_fluid
import matplotlib.pyplot as plt

st.title('Water Dew Point')
st.divider()
st.text("Set fluid composition:")

if 'activefluid_df' not in st.session_state or st.session_state.activefluid_name != 'default_fluid':
    st.session_state.activefluid_name = 'default_fluid'
    st.session_state.activefluid_df = pd.DataFrame(default_fluid)

if 'tp_data' not in st.session_state:
    st.session_state['tp_data'] = pd.DataFrame({
        'Pressure (bara)': [50.0, 100.0, 150.0, 200.0],   # Default example pressure
        'Temperature (C)': [None, None, None, None]  # Default temperature
    })


hidecomponents = st.checkbox('Show active components')
if hidecomponents:
    st.session_state.activefluid_df =  st.edited_df[st.edited_df['MolarComposition[-]'] > 0]
else:
    st.session_state.activefluid_df = st.session_state.activefluid_df = pd.DataFrame(default_fluid)

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
isplusfluid = st.checkbox('Plus Fluid')

st.text("Fluid composition will be normalized before simulation")
st.divider()

st.edited_dfTP = st.data_editor(
    st.session_state.tp_data['Pressure (bara)'].dropna().reset_index(drop=True),
    num_rows='dynamic',  # Allows dynamic number of rows
    column_config={
        'Pressure (bara)': st.column_config.NumberColumn(
            label="Pressure (bara)",
            min_value=0.0,      # Minimum pressure
            max_value=1000,     # Maximum pressure
            format='%f',        # Decimal format
            help='Enter the pressure in bar absolute.'  # Help text for guidance
        )
    }
)

if st.button('Run'):
    # Check if water's MolarComposition[-] is greater than 0
    water_row = st.edited_df[st.edited_df['ComponentName'] == 'water']  # Adjust 'ComponentName' and 'water' as necessary
    if not water_row.empty and water_row['MolarComposition[-]'].iloc[0] > 0:
        neqsim_fluid = fluid_df(st.edited_df, lastIsPlusFraction=False, add_all_components=False).autoSelectModel()
        results_list = []
        results_list2 = []
        pres_list = []
        fluid_results_list = []
        for pres in st.edited_dfTP.dropna():
            pressure = pres
            pres_list.append(pressure)
            neqsim_fluid.setPressure(pressure, 'bara')
            results_list.append(hydt(neqsim_fluid)-273.15)
            results_list2.append(waterdewt(neqsim_fluid)-273.15)
            fluid_results_list.append(dataFrame(neqsim_fluid))
        st.session_state['tp_data'] = pd.DataFrame({
            'Pressure (bara)': pres_list,   # Default example pressure
            'Hydrate Temperature (C)': results_list,  # Default temperature
            'Aqueous Temperature (C)': results_list2  # Default temperature
        })
        st.session_state['tp_data'] = st.session_state['tp_data'].sort_values('Pressure (bara)')
        st.success('Hydrate calculation finished successfully!')
        combined_results = pd.concat(fluid_results_list, ignore_index=True)
           
        if st.session_state.get('refresh', True):
            st.edited_dfTP2 = st.data_editor(
                st.session_state.tp_data.dropna().reset_index(drop=True),
                num_rows='dynamic',  # Allows dynamic number of rows
                column_config={
                    'Pressure (bara)': st.column_config.NumberColumn(
                        label="Pressure (bara)",
                        min_value=0.0,      # Minimum pressure
                        max_value=1000,     # Maximum pressure
                        format='%f',        # Decimal format
                        help='Enter the pressure in bar absolute.'  # Help text for guidance
                    ),
                    'Temperature (C)': st.column_config.NumberColumn(
                        label="Temperature (C)",
                        min_value=-273.15,  # Minimum temperature in Celsius
                        max_value=1000,     # Maximum temperature in Celsius
                        format='%f',        # Decimal format
                        disabled=True
                    ),
                }
            )
        st.divider()
        plt.figure(figsize=(10, 5))
        plt.plot(st.session_state['tp_data']['Hydrate Temperature (C)'], st.session_state['tp_data']['Pressure (bara)'], marker='o', linestyle='-',label="hydrate temperature")
        plt.plot(st.session_state['tp_data']['Aqueous Temperature (C)'], st.session_state['tp_data']['Pressure (bara)'], marker='x', linestyle='--',label="aqueous dew point")
        
        plt.title('Dew Point Lines')
        plt.ylabel('Pressure (bara)')
        plt.xlabel('Temperature (C)')
        plt.legend(loc="upper left")
        plt.grid(True)
        plt.show()
        st.pyplot(plt)  # Display the plot in Streamlit
        st.divider()
        results_df = st.data_editor(combined_results)
        st.session_state['rerender'] = not st.session_state.get('rerender', False)
    else:
        st.error('Water Molar Composition must be greater than 0. Please adjust your inputs.')

uploaded_file = st.sidebar.file_uploader("Import Fluid")
if uploaded_file is not None:
    st.session_state.activefluid_df = pd.read_csv(uploaded_file)
    check1 = st.sidebar.button("Set fluid")
else:
    st.session_state.activefluid_df = pd.DataFrame(default_fluid)
