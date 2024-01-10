import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from oilprocess import ProcessInput

# App title
st.title('Time Series Data Plotter')

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Function to create dataclass instance
def create_process_input(row, mappings):
    mapped_values = {field: row[mappings[field]] for field in mappings}
    return ProcessInput(**mapped_values)

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    st.write(df)

    # Select the time column
    time_col = st.selectbox('Select the time column', df.columns)
    df[time_col] = pd.to_datetime(df[time_col])

    # Select columns to plot
    plot_cols = st.multiselect('Which columns to plot?', df.columns, df.columns[0])

    if len(plot_cols) >= 1:
        # Plotting
        fig, ax = plt.subplots()
        for col in plot_cols:
            if col != time_col:
                ax.plot(df[time_col], df[col], label=col)
        ax.legend()
        st.pyplot(fig)
    
    # Create a mapping interface
    column_mappings = {}
    for field in ProcessInput.__annotations__.keys():
        column_mappings[field] = st.selectbox(f"Map column for {field}", df.columns, index=0)

    # Function to create dataclass instance
    def create_process_input(row, mappings):
        mapped_values = {field: row[mappings[field]] for field in mappings}
        return ProcessInput(**mapped_values)

    # Instantiate ProcessInput
    if st.button("Create ProcessInput Instance"):
        selected_index = st.selectbox("Select Row", df.index)
        selected_row = df.iloc[selected_index]
        process_input = create_process_input(selected_row, column_mappings)
        st.write("Dataclass Instance Created:", process_input)

