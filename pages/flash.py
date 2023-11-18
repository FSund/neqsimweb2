import pandas as pd
import streamlit as st
from neqsim.thermo import fluid_df, TPflash, printFrame

# Default data for fluid
default_data = {
    'ComponentName':  ["nitrogen", "CO2", "methane", "ethane", "propane", "i-butane", "n-butane", "i-pentane", "n-pentane", "n-hexane", "C7", "C8", "C9", "C10", "C11", "C12", "C13", "C14", "C15", "C16", "C17", "C18", "C19", "C20"],
    'MolarComposition[-]':  [0.53, 3.3, 72.98, 7.68, 4.1, 0.7, 1.42, 0.54, 0.67, 0.85, 1.33, 1.33, 0.78, 0.61, 0.42, 0.33, 0.42, 0.24, 0.3, 0.17, 0.21, 0.15, 0.15, 0.8],
    'MolarMass[kg/mol]': [None, None, None, None, None, None, None, None, None, None, 0.0913, 0.1041, 0.1188, 0.136, 0.150, 0.164, 0.179, 0.188, 0.204, 0.216, 0.236, 0.253, 0.27, 0.391],
    'RelativeDensity[-]': [None, None, None, None, None, None, None, None, None, None, 0.746, 0.768, 0.79, 0.787, 0.793, 0.804, 0.817, 0.83, 0.835, 0.843, 0.837, 0.84, 0.85, 0.877]
}

# Function to create editable data table
def editable_table(default_df):
    st.markdown("### Edit Fluid Composition")
    # Display the default dataframe in an editable format
    df = st.dataframe(default_df)

    # Function to update the dataframe based on user input
    def update_dataframe():
        # Create a new dataframe based on the current state of the editable table
        new_data = df.values.tolist()
        columns = default_df.columns.tolist()
        updated_df = pd.DataFrame(new_data, columns=columns)
        return updated_df

    return update_dataframe

# Streamlit app
def main():
    st.title('Gas Condensate Fluid TPflash Calculation with Editable Fluid Composition')

    # Create a default DataFrame
    default_df = pd.DataFrame(default_data)
    
    # Create an editable table and get the updated dataframe
    updated_df_function = editable_table(default_df)
    
    # User inputs for temperature and pressure
    T = st.number_input('Enter Temperature (K):', min_value=0.0, value=298.15)
    P = st.number_input('Enter Pressure (bar):', min_value=0.0, value=1.0)

    if st.button('Run TPflash'):
        # Get the updated dataframe
        updated_df = updated_df_function()

        # Define the fluid with updated dataframe
        gascondensateFluid = fluid_df(updated_df, lastIsPlusFraction=True, numberOfLumpedComponents=12)

        # Set temperature and pressure
        gascondensateFluid.setTemperature(T)
        gascondensateFluid.setPressure(P)

        # Run TPflash calculation
        TPflash(gascondensateFluid)

        # Display results
        st.text("Results of TPflash Calculation:")
        st.text(printFrame(gascondensateFluid))

if __name__ == "__main__":
    main()