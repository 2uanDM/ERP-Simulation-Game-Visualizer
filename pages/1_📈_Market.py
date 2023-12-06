import os
import sys
import pandas as pd
sys.path.append(os.getcwd())  # NOQA

import streamlit as st
import json
import sqlite3

st.set_page_config(
    page_title="Market 📈",
    page_icon="📈",
)


class Market():
    def __init__(self) -> None:
        # Load system config
        with open('configs/system.json', 'r') as f:
            self.system_cfg = json.load(f)

        # Connect to the database
        self.conn = sqlite3.connect(self.system_cfg['db_name'])

        # Init UI
        self.init_ui()
        self.init_sidebar()

        # Refresh UI
        self.refresh_ui()

    def init_sidebar(self):
        # Refresh button
        self.refresh_button = st.sidebar.button('Refresh (Press R)', use_container_width=True)

        if self.refresh_button:
            st.rerun()

        # Table of Content
        st.sidebar.markdown(
            """
            <div id="toc_container" style="background: #262730; padding: 1rem; border-radius: 0.5rem; border: 0.01rem gray solid">
                <p class="toc_title">Contents</p>
                <ul class="toc_list">
                    <li><a style="text-decoration: none;" href="#market-revenue">Market Revenue</a></li>
                    <li><a style="text-decoration: none;" href="#market-unit-sold">Market Unit Sold</a></li>
                    <li><a style="text-decoration: none;" href="#market-average-price">Market Average Price</a></li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def init_ui(self):
        st.title("Market 📈")
        st.write('---')

    """-----------------------------Query SQL commands-----------------------------"""

    def _query_revenue(self):
        result = self.conn.execute("""
            WITH CTE1 AS (
            SELECT 
                SIM_PERIOD AS week,
                SUM(NET_VALUE) AS company_revenue
            FROM Market
            WHERE SALES_ORGANIZATION = 'Company'
            GROUP BY SIM_PERIOD
        ), CTE2 AS (
            SELECT 
                SIM_PERIOD AS week,
                SUM(NET_VALUE) AS market_revenue
            FROM Market
            WHERE SALES_ORGANIZATION = 'Market'
            GROUP BY SIM_PERIOD
        )
        SELECT 
            CTE1.week,
            CTE1.company_revenue,
            CTE2.market_revenue,
            CAST(ROUND(CTE1.company_revenue * 1.0 / CTE2.market_revenue * 100, 2) AS TEXT) || "%" AS Percentage
        FROM CTE1
        JOIN CTE2 ON CTE1.week = CTE2.week
        ORDER BY CTE1.week ASC;
    """)

        return result.fetchall()

    def _query_unit_sold(self):
        result = self.conn.execute("""
            WITH CTE1 AS (
            SELECT 
                SIM_PERIOD AS week,
                SUM(QUANTITY) AS company_quantity
            FROM Market
            WHERE SALES_ORGANIZATION = 'Company'
            GROUP BY SIM_PERIOD
        ), CTE2 AS (
            SELECT 
                SIM_PERIOD AS week,
                SUM(QUANTITY) AS market_quantity
            FROM Market
            WHERE SALES_ORGANIZATION = 'Market'
            GROUP BY SIM_PERIOD
        )
        SELECT 
            CTE1.week,
            CTE1.company_quantity,
            CTE2.market_quantity,
            CAST(ROUND(CTE1.company_quantity * 1.0 / CTE2.market_quantity * 100, 2) AS TEXT) || "%" AS Percentage
        FROM CTE1
        JOIN CTE2 ON CTE1.week = CTE2.week
        ORDER BY CTE1.week ASC;
        """)

        return result.fetchall()

    def _query_average_price(self, weeks: list, distribution_channels: list = [10, 12, 14]):
        result = self.conn.execute(f"""
        WITH CTE1 AS (
            SELECT 
                p.CODE as code,
                ROUND(SUM(NET_VALUE) * 1.0 / SUM(QUANTITY),2) AS company_avg_price
            FROM Market as m
            JOIN Product as p
                ON m.MATERIAL_DESCRIPTION = p.NAME
            WHERE 1 = 1 
                AND SALES_ORGANIZATION = "Company"
                AND m.SIM_PERIOD in ({", ".join([str(i) for i in weeks])})
                AND m.DISTRIBUTION_CHANNEL in ({" ,".join([str(i) for i in distribution_channels])})
            GROUP BY p.CODE
        ), CTE2 AS (
            SELECT 
                p.CODE as code,
                ROUND(SUM(NET_VALUE) * 1.0 / SUM(QUANTITY),2) AS market_avg_price 
            FROM Market as m
            JOIN Product as p
                ON m.MATERIAL_DESCRIPTION = p.NAME
            WHERE 1 = 1 
                AND SALES_ORGANIZATION = "Market"
                AND m.SIM_PERIOD in ({", ".join([str(i) for i in weeks])})
                AND m.DISTRIBUTION_CHANNEL in ({" ,".join([str(i) for i in distribution_channels])})
            GROUP BY p.CODE
        )
        SELECT 
            CTE1.code,
            CTE1.company_avg_price,
            CTE2.market_avg_price,
            CAST(ROUND(CTE1.company_avg_price * 1.0 / CTE2.market_avg_price * 100, 2) AS TEXT) || "%" AS Percentage
        FROM CTE1
        JOIN CTE2 ON CTE1.code = CTE2.code
                ORDER BY CTE1.code ASC;
        """)

        return result.fetchall()

    """-----------------------------UI Elements-----------------------------"""

    def market_revenue(self):
        data = self._query_revenue()
        df = pd.DataFrame(data, columns=['Week', 'Company Revenue', 'Market Revenue', 'Percentage'])
        df.set_index('Week', inplace=True)
        df.index = df.index.astype(int)

        st.markdown("### Market Revenue")

        # Calculate the total in the last row of col Company Revenue and Market Revenue
        company_revenue_total = df['Company Revenue'].sum()
        market_revenue_total = df['Market Revenue'].sum()
        percentage_total = round(company_revenue_total * 1.0 / market_revenue_total * 100, 2)
        df.loc['Total'] = [company_revenue_total, market_revenue_total, f"{percentage_total}%"]

        st.dataframe(df, use_container_width=True)

        st.write('---')
        st.line_chart(
            data=df.iloc[:-1, :][['Company Revenue', 'Market Revenue']],
            color=['#FF0000', '#00FF00'],
            width=1,
            use_container_width=True
        )

    def market_unit_sold(self):
        data = self._query_unit_sold()
        df = pd.DataFrame(data, columns=['Week', 'Company Quantity', 'Market Quantity', 'Percentage'])
        df.set_index('Week', inplace=True)
        df.index = df.index.astype(int)

        st.markdown("### Market Unit Sold")

        # Calculate the total in the last row of col Company Quantity and Market Quantity
        company_quantity_total = df['Company Quantity'].sum()
        market_quantity_total = df['Market Quantity'].sum()
        percentage_total = round(company_quantity_total * 1.0 / market_quantity_total * 100, 2)
        df.loc['Total'] = [company_quantity_total, market_quantity_total, f"{percentage_total}%"]

        st.dataframe(df, use_container_width=True)
        st.write('---')
        st.line_chart(
            data=df.iloc[:-1, :][['Company Quantity', 'Market Quantity']],
            color=['#FF0000', '#00FF00'],
            width=1,
            use_container_width=True
        )

    def market_average_price(self):
        # Get the lastest week from the table Market
        self.max_week: int = self.conn.execute("""
            SELECT MAX(SIM_PERIOD) FROM Market;
        """).fetchone()[0]

        st.markdown("### Market Average Price")

        col1, col2 = st.columns(2)

        # Create the filter for the week
        with col1:
            choose_weeks: list = st.multiselect(
                label="Week",
                options=[i for i in range(1, self.max_week + 1)],
                default=[i for i in range(1, self.max_week + 1)],
                key='market_average_price_weeks'
            )

        # Create the filter for the distribution channel
        with col2:
            choose_distribution_channels: list = st.multiselect(
                label="Distribution Channel",
                options=[10, 12, 14],
                default=[10, 12, 14],
                key='market_average_price_distribution_channels'
            )

        data = self._query_average_price(
            weeks=choose_weeks,
            distribution_channels=choose_distribution_channels
        )

        df = pd.DataFrame(data, columns=['Code', 'Company Avg Price', 'Market Avg Price', 'Percentage'])

        st.dataframe(df, use_container_width=True, hide_index=True)

    """-----------------------------Refresh UI-----------------------------"""

    def refresh_ui(self):
        try:
            # Create a table of content relative to the markdown headers
            self.market_revenue()
            self.market_unit_sold()
            self.market_average_price()
        except ZeroDivisionError:
            st.error("Data is being loaded, please wait a few seconds and refresh the page again!")


if __name__ == "__main__":
    market = Market()
