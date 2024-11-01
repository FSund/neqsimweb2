import streamlit as st

welcome = st.Page(
    "welcome/welcome.py",
    title="Welcome",
    icon=":material/home:"
)

tp_flash = st.Page("tools/0_TP_flash.py")

phase_envelope = st.Page("tools/20_Phase_envelope.py")

pg = st.navigation({
    "Welcome": [welcome], 
    "Tools": [
        tp_flash, 
        phase_envelope,
    ]
})
pg.run()