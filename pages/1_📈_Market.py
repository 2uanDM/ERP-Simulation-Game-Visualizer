import os
import sys

import pandas as pd

sys.path.append(os.getcwd())  # NOQA

import json
import sqlite3

import altair as alt
import streamlit as st

st.set_page_config(
    page_title="Market 📈",
    page_icon="📈",
    layout="wide",
)


class Market:
    def __init__(self) -> None:
        # Load system config
        with open("configs/system.json", "r") as f:
            self.system_cfg = json.load(f)

        # Connect to the database
        self.conn = sqlite3.connect(self.system_cfg["db_name"])

        # Init UI
        self.init_ui()
        self.init_sidebar()

        # Refresh UI
        self.refresh_ui()

    def init_sidebar(self):
        # Refresh button
        self.refresh_button = st.sidebar.button(
            "Refresh (Press R)", use_container_width=True
        )

        if self.refresh_button:
            st.rerun()

        # Table of Content
        st.sidebar.markdown(
            """
            <div id="toc_container" style="background: #D6F7FF; padding: 1rem; border-radius: 0.5rem; border: 0.01rem gray solid">
                <p class="toc_title">Contents</p>
                <ul class="toc_list">
                    <li><a style="text-decoration: none;" href="#market-revenue">Market Revenue</a></li>
                    <li><a style="text-decoration: none;" href="#market-products-ranking">Market Products Ranking</a></li>
                    <li><a style="text-decoration: none;" href="#market-unit-sold">Market Unit Sold</a></li>
                    <li><a style="text-decoration: none;" href="#market-average-price">Market Average Price</a></li>
                    <li><a style="text-decoration: none;" href="#market-bar-chart">Market Bar Chart</a></li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def init_ui(self):
        st.title("Market 📈")
        st.write("---")

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

    def _query_average_price(
        self, weeks: list, distribution_channels: list = [10, 12, 14]
    ):
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

    def _query_quantity_sold_by_product(
        self, weeks: list, distribution_channels: list, area: list, sales_organization
    ):
        result = self.conn.execute(f"""
            SELECT 
                p.CODE as code,
                SUM(m.QUANTITY) as quantity
            FROM Market as m
            JOIN Product as p ON m.MATERIAL_DESCRIPTION = p.NAME
            WHERE m.SIM_PERIOD in ({", ".join([str(i) for i in weeks])})
            AND m.AREA in ({", ".join([f"'{i}'" for i in area])})
            AND m.DISTRIBUTION_CHANNEL in ({", ".join([str(i) for i in distribution_channels])})
            AND m.SALES_ORGANIZATION = '{sales_organization}'
            GROUP BY p.CODE
            ORDER BY quantity ASC;
        """)

        return result.fetchall()

    def _query_net_value_by_product(
        self, weeks: list, distribution_channels: list, area: list, sales_organization
    ):
        result = self.conn.execute(f"""
            SELECT 
                p.CODE as code,
                SUM(m.NET_VALUE) as net_value
            FROM Market as m
            JOIN Product as p ON m.MATERIAL_DESCRIPTION = p.NAME
            WHERE m.SIM_PERIOD in ({", ".join([str(i) for i in weeks])})
            AND m.AREA in ({", ".join([f"'{i}'" for i in area])})
            AND m.DISTRIBUTION_CHANNEL in ({", ".join([str(i) for i in distribution_channels])})
            AND m.SALES_ORGANIZATION = '{sales_organization}'
            GROUP BY p.CODE
            ORDER BY net_value ASC;
        """)

        return result.fetchall()

    def _query_ranking_products(
        self,
        rounds: list,
        weeks: list,
        distribution_channels: list,
        area: list,
    ):
        result = self.conn.execute(f"""
            with company_unit_sold as (
                select
                    p.CODE,
                    sum(QUANTITY) as total_quantity
                from Product as p
                left join Market as m
                    on m.MATERIAL_DESCRIPTION = p.NAME
                where 1 = 1
                    and m.SIM_ROUND in ({','.join([str(i) for i in rounds])})
                    and m.SIM_PERIOD in ({','.join([str(i) for i in weeks])})
                    and m.AREA in ({','.join([f"'{i}'" for i in area])})
                    and m.DISTRIBUTION_CHANNEL in ({','.join([str(i) for i in distribution_channels])})
                    and m.SALES_ORGANIZATION = 'Company'
                group by p.CODE
            ), market_unit_sold as (
                select
                    p.CODE,
                    sum(QUANTITY) as total_quantity
                from Product as p
                left join Market as m
                    on m.MATERIAL_DESCRIPTION = p.NAME
                where 1 = 1
                    and m.SIM_ROUND in ({','.join([str(i) for i in rounds])})
                    and m.SIM_PERIOD in ({','.join([str(i) for i in weeks])})
                    and m.AREA in ({','.join([f"'{i}'" for i in area])})
                    and m.DISTRIBUTION_CHANNEL in ({','.join([str(i) for i in distribution_channels])})
                    and m.SALES_ORGANIZATION = 'Market'
                group by p.CODE
            )
            select
                c.CODE,
                c.total_quantity as company_sold,
                m.total_quantity as market_sold,
                round((c.total_quantity * 1.0 / m.total_quantity),3) * 100 as proportion,
                rank() over (order by (c.total_quantity * 1.0 / m.total_quantity) desc) as rank
            from company_unit_sold as c, market_unit_sold as m
            where c.CODE = m.CODE;
            """)

        return result.fetchall()

    """-----------------------------UI Elements-----------------------------"""

    def market_revenue(self):
        data = self._query_revenue()
        df = pd.DataFrame(
            data, columns=["Week", "Company Revenue", "Market Revenue", "Percentage"]
        )
        df.set_index("Week", inplace=True)
        df.index = df.index.astype(int)

        st.markdown("### Market Revenue")

        # Calculate the total in the last row of col Company Revenue and Market Revenue
        company_revenue_total = df["Company Revenue"].sum()
        market_revenue_total = df["Market Revenue"].sum()
        percentage_total = round(
            company_revenue_total * 1.0 / market_revenue_total * 100, 2
        )
        df.loc["Total"] = [
            company_revenue_total,
            market_revenue_total,
            f"{percentage_total}%",
        ]

        st.dataframe(df, use_container_width=True)

        st.write("---")
        # st.line_chart(
        #     data=df.iloc[:-1, :][["Company Revenue", "Market Revenue"]],
        #     color=["#FF0000", "#00FF00"],
        #     width=1,
        #     use_container_width=True,
        # )

    def market_products_ranking(self):
        st.markdown("### Market Products Ranking")

        col1, col2 = st.columns(2)

        with col1:
            self.max_round: int = int(
                self.conn.execute(""" 
                SELECT MAX(SIM_ROUND) FROM Market;
            """).fetchone()[0]
            )

            choose_rounds: list = st.multiselect(
                label="Round",
                options=[i for i in range(1, self.max_round + 1)],
                default=self.max_round,
                key="market_products_ranking_rounds",
            )

        with col2:
            # Get the lastest week from the table Market
            self.max_week: int = int(
                self.conn.execute("""
                SELECT MAX(SIM_PERIOD) FROM Market;
            """).fetchone()[0]
            )

            choose_weeks: list = st.multiselect(
                label="Week",
                options=[i for i in range(1, self.max_week + 1)],
                default=[i for i in range(1, self.max_week + 1)],
                key="market_products_ranking_weeks",
            )

        col3, col4 = st.columns(2)

        with col3:
            result = self.conn.execute("""
                SELECT DISTINCT AREA FROM Market;
            """).fetchall()

            choose_area: list = st.multiselect(
                label="Area",
                options=[i[0] for i in result],
                default=[i[0] for i in result],
                key="market_products_ranking_area",
            )

        with col4:
            choose_distribution_channels: list = st.multiselect(
                label="Distribution Channel",
                options=[10, 12, 14],
                default=[10, 12, 14],
                key="market_products_ranking_distribution_channels",
            )

        data = self._query_ranking_products(
            choose_rounds, choose_weeks, choose_distribution_channels, choose_area
        )

        # Create the DataFrame
        headers = ["Code", "Company Sold", "Market Sold", "Proportion", "Rank"]
        df = pd.DataFrame(data, columns=headers)
        df.set_index("Code", inplace=True)

        # Create the table
        st.dataframe(df, use_container_width=True)

    def market_unit_sold(self):
        data = self._query_unit_sold()
        df = pd.DataFrame(
            data, columns=["Week", "Company Quantity", "Market Quantity", "Percentage"]
        )
        df.set_index("Week", inplace=True)
        df.index = df.index.astype(int)

        st.markdown("### Market Unit Sold")

        # Calculate the total in the last row of col Company Quantity and Market Quantity
        company_quantity_total = df["Company Quantity"].sum()
        market_quantity_total = df["Market Quantity"].sum()
        percentage_total = round(
            company_quantity_total * 1.0 / market_quantity_total * 100, 2
        )
        df.loc["Total"] = [
            company_quantity_total,
            market_quantity_total,
            f"{percentage_total}%",
        ]

        st.dataframe(df, use_container_width=True)
        st.write("---")
        # st.line_chart(
        #     data=df.iloc[:-1, :][["Company Quantity", "Market Quantity"]],
        #     color=["#FF0000", "#00FF00"],
        #     width=1,
        #     use_container_width=True,
        # )

    def market_average_price(self):
        st.markdown("### Market Average Price")

        col1, col2 = st.columns(2)

        # Create the filter for the week
        with col1:
            choose_weeks: list = st.multiselect(
                label="Week",
                options=[i for i in range(1, self.max_week + 1)],
                default=self.max_week,
                key="market_average_price_weeks",
            )

        # Create the filter for the distribution channel
        with col2:
            choose_distribution_channels: list = st.multiselect(
                label="Distribution Channel",
                options=[10, 12, 14],
                default=[10, 12, 14],
                key="market_average_price_distribution_channels",
            )

        data = self._query_average_price(
            weeks=choose_weeks, distribution_channels=choose_distribution_channels
        )

        df = pd.DataFrame(
            data,
            columns=["Code", "Company Avg Price", "Market Avg Price", "Percentage"],
        )

        st.dataframe(df, use_container_width=True, hide_index=True)

    def market_bar_chart(self):
        st.markdown("### Market Bar Chart")

        col3, col4 = st.columns(2)

        with col3:
            type = st.selectbox(
                label="Type",
                options=["Quantity Sold", "Net Value"],
                index=0,
                key="market_bar_chart_choose_type",
            )

            type = "quantity_sold" if type == "Quantity Sold" else "net_value"

        with col4:
            sales_organization = st.selectbox(
                label="Sales Organization",
                options=["Company", "Market"],
                index=1,
                key="market_bar_chart_choose_sales_organization",
            )

        # Create the filter for the week

        col1, col2 = st.columns(2)

        with col1:
            choose_area: list = st.multiselect(
                label="Area",
                options=["North", "South", "West"],
                default=["North", "South", "West"],
                key=f"market_bar_chart_{type}_area",
            )

        with col2:
            choose_distribution_channels: list = st.multiselect(
                label="Distribution Channel",
                options=[10, 12, 14],
                default=[10, 12, 14],
                key=f"market_bar_chart_{type}_distribution_channels",
            )

        choose_weeks: list = st.multiselect(
            label="Week",
            options=[i for i in range(1, self.max_week + 1)],
            default=[i for i in range(1, self.max_week + 1)],
            key=f"market_bar_chart_{type}_weeks",
        )

        args = (
            choose_weeks,
            choose_distribution_channels,
            choose_area,
            sales_organization,
        )

        if type == "quantity_sold":
            data = self._query_quantity_sold_by_product(*args)
        elif type == "net_value":
            data = self._query_net_value_by_product(*args)

        type_to_column = {"quantity_sold": "Quantity", "net_value": "Net Value"}

        df = pd.DataFrame(data, columns=["Code", type_to_column[type]])

        st.markdown("Result:")

        # Draw the column chart (Sorted by Quantity)
        if sales_organization == "Company":
            chart_element = alt.Chart(
                df.sort_values(by=[type_to_column[type]], ascending=True)
            ).mark_bar()  # Light Blue
        else:
            chart_element = alt.Chart(
                df.sort_values(by=[type_to_column[type]], ascending=True)
            ).mark_bar(color="#1ED760")

        st.write(
            chart_element.encode(
                x=alt.X(
                    "Code", title="Product Code", sort=None, axis=alt.Axis(labelAngle=0)
                ),
                y=alt.Y(
                    type_to_column[type],
                    title=type_to_column[type],
                    axis=alt.Axis(format="s"),
                ),
                tooltip=["Code", type_to_column[type]],
                text=alt.Text(
                    type_to_column[type], format=".0f"
                ),  # Add this line to show data label
            )
            .properties(width=700, height=450)
            .configure_mark(align="center", baseline="bottom")
            .configure_axis(labelFontSize=12, titleFontSize=14)
        )

    """-----------------------------Refresh UI-----------------------------"""

    def refresh_ui(self):
        try:
            # Create a table of content relative to the markdown headers
            self.market_revenue()
            st.write("---")
            self.market_products_ranking()
            st.write("---")
            self.market_unit_sold()
            st.write("---")
            self.market_average_price()
            st.write("---")
            self.market_bar_chart()

        except ZeroDivisionError:
            st.error(
                "Data is being loaded, please wait a few seconds and refresh the page again!"
            )


if __name__ == "__main__":
    market = Market()
