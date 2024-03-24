import json
import os
import sqlite3
import sys

import polars as pl

sys.path.append(os.getcwd())  # NOQA

import streamlit as st

from database.schema import Current_Inventory

with open("configs/games.json", "r") as f:
    CONFIG = json.load(f)

st.set_page_config(
    page_title="Current Inventory 📊",
    page_icon="📊",
    layout="wide",
)


def main():
    st.title("Current Inventory 📊")

    st.write("---")

    # Refresh button
    refresh_button = st.sidebar.button("Refresh (Press R)", use_container_width=True)

    with st.spinner("Loading Current_Inventory table..."):
        conn = sqlite3.connect("erp.db")

        data = conn.execute("""
            SELECT
                MATERIAL_NUMBER,
                MATERIAL_DESCRIPTION,
                STORAGE_LOCATION,
                STOCK,
                RESTRICTED,
                UNIT 
            FROM Current_Inventory
            """).fetchall()

        if data == []:
            st.error(
                "The Current_Inventory table does not exist! Wait for the data to be fetched!"
            )
        else:
            inventory_df = pl.DataFrame(data).to_pandas()

            col_key = list(Current_Inventory.__annotations__.keys())

            for remove_col in ["ID", "ROW_ID", "PLANT"]:
                del col_key[col_key.index(remove_col)]

            inventory_df.columns = col_key

            st.dataframe(inventory_df, hide_index=True)

        conn.close()


if __name__ == "__main__":
    main()
