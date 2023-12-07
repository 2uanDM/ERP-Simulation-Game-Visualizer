import json
import os
import sqlite3
import sys
import polars as pl
sys.path.append(os.getcwd())  # NOQA

import streamlit as st
from database.schema import Inventory

with open('configs/games.json', 'r') as f:
    CONFIG = json.load(f)

st.set_page_config(
    page_title="Inventory 📦",
    page_icon="📦",
)


def main():
    st.title("Inventory 📦")

    st.write('---')

    # Refresh button
    refresh_button = st.sidebar.button('Refresh (Press R)', use_container_width=True)

    # Get the Inventory table
    if not os.path.exists(".temp/Inventory.xml"):
        st.error("The Inventory table does not exist! Wait for the data to be fetched!")
        return

    with st.spinner("Loading Inventory table..."):
        conn = sqlite3.connect('erp.db')

        data = conn.execute("""
            SELECT * FROM Inventory
            """).fetchall()

        if data == []:
            st.error("The Inventory table does not exist! Wait for the data to be fetched!")
        else:
            inventory_df = pl.DataFrame(data).to_pandas()
            inventory_df.columns = Inventory.__annotations__.keys()

        conn.close()

        st.dataframe(inventory_df)


if __name__ == '__main__':
    main()
