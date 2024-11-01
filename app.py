import streamlit as st

welcome = st.Page(
    "welcome/welcome.py",
    title="Welcome",
    icon=":material/home:"
)

tp_flash = st.Page("tools/tp_flash.py")
phase_envelope = st.Page("tools/phase_envelope.py")

# simple
pg = st.navigation([
    welcome,
    # tp_flash, 
    phase_envelope,
])

# with headers
# pg = st.navigation({
#     "Welcome": [welcome], 
#     "Tools": [
#         tp_flash, 
#         phase_envelope,
#     ]
# })

pg.run()
