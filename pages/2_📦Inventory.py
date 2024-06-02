import json
import os
import sqlite3
import sys

import polars as pl

sys.path.append(os.getcwd())  # NOQA

import streamlit as st

from database.schema import Inventory

with open("configs/games.json", "r") as f:
    CONFIG = json.load(f)

st.set_page_config(
    page_title="Inventory 📦",
    page_icon="📦",
    layout="wide",
)


def main():
    st.title("Inventory 📦")

    st.write("---")

    # Refresh button
    refresh_button = st.sidebar.button("Refresh (Press R)", use_container_width=True)

    with st.spinner("Loading Inventory table..."):
        conn = sqlite3.connect("erp.db")

        remove_col = [
            "ID",
            "ROW_ID",
            "PLANT",
            "SIM_DATE",
            "SIM_CALENDAR_DATE",
            "SIM_ELAPSED_STEPS",
            "MATERIAL_LABEL",
            "MATERIAL_SIZE",
        ]

        select_col = list(Inventory.__annotations__.keys())
        select_col = [x for x in select_col if x not in remove_col]

        max_day = conn.execute("""
            SELECT MAX(SIM_STEP) FROM Inventory
            """)

        result = max_day.fetchone()

        if result[0] is None:
            st.error(
                "The Inventory table does not exist! Wait for the data to be fetched!"
            )
            return

        max_day = int(result[0])

        day = st.sidebar.multiselect(
            "Day",
            list(range(1, max_day + 1)),
            key="inventory_day_filter",
            default=list(range(1, max_day + 1)),
        )

        data = conn.execute(f"""
            SELECT
                SIM_ROUND,
                SIM_STEP,
                SIM_PERIOD,
                STORAGE_LOCATION,
                MATERIAL_NUMBER,
                MATERIAL_DESCRIPTION,
                MATERIAL_TYPE,
                MATERIAL_CODE,
                INVENTORY_OPENING_BALANCE,
                UNIT
            FROM Inventory
            WHERE SIM_STEP in ({', '.join([str(x) for x in day])})
            """).fetchall()

        if data == []:
            st.error(
                "The Inventory table does not exist! Wait for the data to be fetched!"
            )
        else:
            inventory_df = pl.DataFrame(data).to_pandas()
            inventory_df.columns = select_col
            st.dataframe(inventory_df, hide_index=True)

        conn.close()


if __name__ == "__main__":
    main()
