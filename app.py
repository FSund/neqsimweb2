import streamlit as st
import logging
from neqsimweb.app_logging import SQLAlchemyHandler

logger = logging.getLogger(__name__)


def setup_logging():
    sql_handler = SQLAlchemyHandler()
    sql_handler.setLevel(logging.DEBUG)
    
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    
    logging.basicConfig(
        level=logging.INFO,  # root logger level
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[  # handlers to add to the root logger
            logging.FileHandler("debug.log"),
            stream_handler,
            sql_handler,
        ]
    )


if __name__ == "__main__":
    setup_logging()
    logger.info("App started")
    
    welcome = st.Page(
        "welcome/welcome.py",
        title="Welcome",
        icon=":material/home:"
    )

    tp_flash = st.Page(
        "tools/tp_flash.py",
        title="TP flash",
    )
    phase_envelope = st.Page(
        "tools/phase_envelope.py",
        title="Phase envelope",
    )
    logs = st.Page(
        "welcome/logs.py",
        title="Logs",
    )
    changelog = st.Page(
        "welcome/changelog.py",
        title="Changelog",
    )

    # simple
    pg = st.navigation([
        welcome,
        # tp_flash, 
        phase_envelope,
        logs,
        changelog,
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
