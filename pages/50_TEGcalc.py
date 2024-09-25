import streamlit as st
import neqsim
from neqsim.thermo import fluid, TPflash, phaseenvelope

 
# Funksjon for å beregne fasekonvolutt og TEG innhold i gassen
def calculate_teg(fluid_composition, lean_teg_wt, pressure, temperature):
    # Opprette fluid med valgt komposisjon
    fluid1 = fluid('srk')
    for component, fraction in fluid_composition.items():
        fluid1.addComponent(component, fraction)
    fluid1.setPressure(pressure, "bara")
    fluid1.setTemperature(temperature, "C")
    # Legg til Lean TEG
    fluid1.addComponent('TEG', lean_teg_wt / 100.0)
    # Flash for å oppnå likevekt
    TPflash(fluid1)
    # Beregn fasekonvolutt
    phase_env = phaseenvelope(fluid1)
    phase_env.calcPTphaseEnvelope()
    # Få TEG i gass (ppm og L/MSm3)
    gas_phase = fluid1.getPhase('gas')
    teg_in_gas_ppm = gas_phase.getComponent("TEG").getz() * 1e6  # ppm
    teg_in_gas_l_per_msm3 = gas_phase.getVolume("m3") / fluid1.getVolume("MSm3")  # L/MSm3
    return phase_env, teg_in_gas_ppm, teg_in_gas_l_per_msm3
 
# Streamlit GUI
st.title('TEG Beregning med NeqSim')
 
# Input for fluidkomposisjon
st.header('Fluid Komposisjon')
components = ["methane", "ethane", "propane", "n-butane", "CO2", "nitrogen"]
fluid_composition = {}
for component in components:
    fraction = st.number_input(f'{component} (mol%)', min_value=0.0, max_value=100.0, step=0.1)
    fluid_composition[component] = fraction / 100.0
 
# Input for Lean TEG og betingelser
st.header('Lean TEG og Betingelser')
lean_teg_wt = st.number_input('Lean TEG Weight %', min_value=0.0, max_value=100.0, step=0.1)
pressure = st.number_input('Trykk (bara)', min_value=1.0, max_value=200.0, step=0.1)
temperature = st.number_input('Temperatur (°C)', min_value=-100.0, max_value=300.0, step=0.1)
 
# Beregn knapp
if st.button('Run'):
    phase_env, teg_in_gas_ppm, teg_in_gas_l_per_msm3 = calculate_teg(fluid_composition, lean_teg_wt, pressure, temperature)
    st.subheader('Resultater')
    st.write(f'TEG i gass: {teg_in_gas_ppm:.2f} ppm')
    st.write(f'TEG i gass: {teg_in_gas_l_per_msm3:.4f} L/MSm³')
    # Plot fasekonvolutt (forenklet visualisering)
    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(phase_env.getOperation().get("pressure"), phase_env.getOperation().get("temperature"))
    plt.xlabel('Trykk (bara)')
    plt.ylabel('Temperatur (°C)')
    plt.title('Fasekonvolutt for Vannholdig Fase')
    st.pyplot(plt)