from dataclasses import dataclass, fields
import streamlit as st
import pandas as pd
from oilprocess import ProcessInput, ProcessOutput, getprocess 

#oilprocess = getprocess()

# Initialize session state for mappings
if 'mappings' not in st.session_state:
    st.session_state['mappings'] = {}

# Function to remove a mapping
def remove_mapping(key):
    del st.session_state['mappings'][key]

# Read and display CSV
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)

    # Dropdown to select a field for mapping
    unmapped_fields = [f for f in ProcessInput.__annotations__.keys() if f not in st.session_state['mappings']]
    selected_field = st.selectbox("Select a field to map", [''] + unmapped_fields)

    # Dropdown to select a column for the chosen field
    if selected_field:
        selected_column = st.selectbox("Select a column to map to", df.columns)
        if st.button(f"Add mapping for {selected_field}"):
            st.session_state['mappings'][selected_field] = selected_column
            st.success(f"Mapping added: {selected_field} -> {selected_column}")

    # Function to create dataclass instance
    def create_process_input(row, mappings):
        mapped_values = {}
        for field in ProcessInput.__annotations__.keys():
            if field in mappings:
                mapped_values[field] = row[mappings[field]]
            else:
                # Use default value if mapping is skipped
                default_value = 1.0#next(f.default for f in fields(ProcessInput) if f.name == field)
                mapped_values[field] = default_value
        return ProcessInput(**mapped_values)

    # Instantiate ProcessInput
    if st.button("Create ProcessInput Instance"):
        selected_index = 1#st.selectbox("Select Row", df.index)
        selected_row = df.iloc[selected_index]
        process_input = create_process_input(selected_row, st.session_state['mappings'])
        st.write("Dataclass Instance Created:", process_input)

    st.write("Current Mappings:")
    for field, column in st.session_state['mappings'].items():
        col1, col2 = st.columns(2)
        col1.write(f"{field} -> {column}")
        if col2.button(f"Remove {field}", key=field):
            remove_mapping(field)
