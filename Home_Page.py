import json
import os
import streamlit as st
import subprocess
from utils.common import product_info

st.set_page_config(
    page_title="ERP SIMULATION",
    page_icon=":shark:",
)


class HomePage():
    def __init__(self):
        st.header("ERP SIMULATION")

        # Init the UI
        self.init_ui()

        # Input the config of the simulation
        self.role = st.sidebar.radio("Your Role", options=['Admin', 'Client'], index=1)

        if self.role == 'Admin':
            self.setup_input_config_ui()

    def init_ui(self):
        st.write('---')

        # Table of Product
        st.markdown("### Product")

        # Show the table of product without the vertical index
        st.table(product_info().to_pandas().set_index('Code'))

    def _save_config(self):
        new_config = {
            "data_source_link": self.data_source_link,
            'username': self.username,
            'password': self.password,
            'auto_refresh': self.auto_refresh
        }

        print(f"==>> new_config: {new_config}")

        with open('configs/games.json', 'w') as f:
            json.dump(new_config, f, indent=4, ensure_ascii=True)

        st.toast("Saved successfully!", icon='✅')

    def setup_input_config_ui(self):
        st.sidebar.header("Simulation Config")

        # Load the value from the config file
        with open('configs/games.json', 'r') as f:
            config = json.load(f)

        self.data_source_link = st.sidebar.text_input("Data source link", value=config["data_source_link"])

        self.username = st.sidebar.text_input("Username", value=config["username"])

        self.password = st.sidebar.text_input("Password", value=config["password"], type="password")

        self.auto_refresh = st.sidebar.number_input(
            "Refresh data after (s)", value=config["auto_refresh"], step=1, format="%d")

        print(f"==>> self.data_source_link: {self.data_source_link}")

        # Show the save button
        if st.sidebar.button("Save Config", use_container_width=True):
            self._save_config()

        if st.sidebar.button("Start Simulation", use_container_width=True, key='start_simulation'):
            self.start_simulation()

        # Change the CSS of the button
        st.markdown(
            """
            <style>
                button[data-testid="baseButton-secondary"] {
                    background-color: green !important;
                    border-color: #262730 !important;
                    color: white !important;
                    border-radius: 0.5rem !important;
                    border: 0.01rem gray solid !important;
                }

                button[data-testid="baseButton-secondary"][key="start_simulation"] {
                    background-color: red !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

    def start_simulation(self):
        st.toast("Simulation Started! Good luck", icon='🚀')

        # Open a new console and run the simulation
        command = 'call .venv/Scripts/activate.bat && python fetcher.py'

        # Run the command
        subprocess.call(command, shell=True)


if __name__ == '__main__':
    HomePage()
