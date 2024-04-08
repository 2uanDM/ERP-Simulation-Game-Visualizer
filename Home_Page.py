import json
import os
import shutil
import subprocess
from datetime import datetime

import streamlit as st

from fetcher import DataRefresher
from utils.common import product_info, tables

st.set_page_config(
    page_title="ERP SIMULATION",
    page_icon=":shark:",
    layout="wide",
)


class HomePage:
    def __init__(self):
        st.header("ERP SIMULATION")

        # Init the UI
        self.init_ui()

        # Input the config of the simulation
        self.role = st.sidebar.radio("Your Role", options=["Admin", "Client"], index=0)

        if self.role == "Admin":
            self.setup_input_config_ui()
            self.setup_database_management_ui()

    def init_ui(self):
        st.write("---")

        # Table of Product
        st.markdown("### Product")

        # Show the table of product without the vertical index
        st.table(product_info().to_pandas().set_index("Code"))

    def _save_config(self):
        new_config = {
            "data_source_link": self.data_source_link,
            "username": self.username,
            "password": self.password,
            "auto_refresh": self.auto_refresh,
        }

        print(f"==>> new_config: {new_config}")

        with open("configs/games.json", "w") as f:
            json.dump(new_config, f, indent=4, ensure_ascii=True)

        st.toast("Saved successfully!", icon="✅")

    def setup_input_config_ui(self):
        st.sidebar.header("Simulation Config")

        # Load the value from the config file
        with open("configs/games.json", "r") as f:
            config = json.load(f)

        self.data_source_link = st.sidebar.text_input(
            "Data source link", value=config["data_source_link"]
        )

        self.username = st.sidebar.text_input("Username", value=config["username"])

        self.password = st.sidebar.text_input(
            "Password", value=config["password"], type="password"
        )

        self.auto_refresh = st.sidebar.number_input(
            "Refresh data after (s)", value=config["auto_refresh"], step=1, format="%d"
        )

        # Show the save button
        if st.sidebar.button("Save Config", use_container_width=True):
            self._save_config()

        if st.sidebar.button(
            "Start Simulation", use_container_width=True, key="start_simulation"
        ):
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

    def _create_database_from_xmls(self):
        def load_files():
            with st.spinner("Creating database..."):
                if xml_files:
                    shutil.rmtree(".temp", ignore_errors=True)
                    os.makedirs(".temp", exist_ok=True)  # noqa: F821
                    for file in xml_files:
                        with open(f".temp/{file.name}", "wb") as f:
                            f.write(file.read())

                    refresher = DataRefresher()
                    refresher._set_tables(tables)
                    refresher.xmls_to_models(folder_dir=".temp")

                    st.success("Database created successfully!")

        xml_files = st.file_uploader(
            "Choose folder with xmls",
            type=["xml"],
            accept_multiple_files=True,
            key="xml_files",
        )

        st.button(
            "Create Database", key="create_database_xmls", on_click=lambda: load_files()
        )

    def _create_database_from_csv(self):
        def load_files():
            with st.spinner("Creating database..."):
                if csv_files:
                    shutil.rmtree(".temp_csvs", ignore_errors=True)
                    os.makedirs(".temp_csvs", exist_ok=True)
                    for file in csv_files:
                        with open(f".temp_csvs/{file.name}", "wb") as f:
                            f.write(file.read())

                    refresher = DataRefresher()
                    refresher._set_tables(tables)
                    refresher.csvs_to_models(folder_dir=".temp_csvs")

                    st.success("Database created successfully!")

        csv_files = st.file_uploader(
            "Choose folder with csvs",
            type=["csv"],
            accept_multiple_files=True,
            key="csv_files",
        )

        st.button(
            "Create Database", key="create_database_csvs", on_click=lambda: load_files()
        )

    def _export_csv_from_xmls(self):
        def convert():
            if xml_files:
                shutil.rmtree(".temp", ignore_errors=True)
                os.makedirs(".temp", exist_ok=True)
                for file in xml_files:
                    print(f".temp/{file.name}")
                    with open(f".temp/{file.name}", "wb") as f:
                        f.write(file.read())

                refresher = DataRefresher()
                refresher._set_tables(tables)
                path = refresher.xmls_to_csvs()

                date_now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                st.download_button(
                    label="Download zip",
                    data=open(path, "rb").read(),
                    file_name=f"{date_now}-erp_data.zip",
                )

        xml_files = st.file_uploader(
            "Choose folder with xmls",
            type=["xml"],
            accept_multiple_files=True,
            key="xml_files_to_csvs",
        )

        st.button("Convert", key="xmls_to_csvs", on_click=lambda: convert())

    def setup_database_management_ui(self):
        st.write("---")
        # Mode 1: Create database from xmls
        st.markdown("### Mode 1: Create database from xmls")
        self._create_database_from_xmls()

        st.write("---")
        # Mode 2: Create databse from csv
        st.markdown("### Mode 2: Create database from csv")
        self._create_database_from_csv()

        st.write("---")
        # Mode 3: Export csv from xmls
        st.markdown("### Mode 3: Export csv from xmls")
        self._export_csv_from_xmls()

    def start_simulation(self):
        st.toast("Simulation Started! Good luck", icon="🚀")

        # Open a new console and run the simulation
        command = "call .venv/Scripts/activate.bat && python fetcher.py"

        # Run the command
        subprocess.Popen(
            command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE
        )


if __name__ == "__main__":
    HomePage()
