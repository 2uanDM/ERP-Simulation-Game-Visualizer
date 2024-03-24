import os
import sys
import time
import traceback

sys.path.append(os.getcwd())  # NOQA

import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List

import httpx
import pandas as pd
import polars as pl
from bs4 import BeautifulSoup as bs
from lxml import etree
from pydantic import BaseModel

from database.init_db import init_db
from database.schema import (
    BOM_Changes,
    Carbon_Emission,
    Company_Valuation,
    Current_Inventory,
    Current_Inventory_KPI,
    Current_Suppliers_Prices,
    Financial_Postings,
    Goods_Movements,
    Independent_Requirements,
    Inventory,
    Market,
    Marketing_Expenses,
    NPS_Surveys,
    Pricing_Conditions,
    Production,
    Production_Orders,
    Purchase_Orders,
    Sales,
    Suppliers_Prices,
)

with open("configs/games.json", "r") as f:
    CONFIG = json.load(f)


table_to_model: dict = {
    "BOM_Changes": BOM_Changes,
    "Carbon_Emissions": Carbon_Emission,
    "Company_Valuation": Company_Valuation,
    "Current_Inventory": Current_Inventory,
    "Current_Inventory_KPI": Current_Inventory_KPI,
    "Current_Suppliers_Prices": Current_Suppliers_Prices,
    "Financial_Postings": Financial_Postings,
    "Goods_Movements": Goods_Movements,
    "Independent_Requirements": Independent_Requirements,
    "Market": Market,
    "Inventory": Inventory,
    "Marketing_Expenses": Marketing_Expenses,
    "NPS_Surveys": NPS_Surveys,
    "Pricing_Conditions": Pricing_Conditions,
    "Production": Production,
    "Production_Orders": Production_Orders,
    "Purchase_Orders": Purchase_Orders,
    "Sales": Sales,
    "Suppliers_Prices": Suppliers_Prices,
}


class DataRefresher:
    def __init__(self, main_url: str, tables: list) -> None:
        """
        Tables:
            ```python
            Company_Valuation, Financial_Postings, Purchase_Orders, Production_Orders,
            Inventory, Current_Inventory, Market, Marketing_Expenses, Sales
            ```
        Args:
            tables (list): The list of table name
        """

        os.makedirs(".temp", exist_ok=True)

        self.tables = tables
        self.urls = [
            f"{main_url}/{table}" if main_url[-1] != "/" else f"{main_url}{table}"
            for table in tables
        ]

    def _fetch_xml(self, url: str, table_name: str = None):
        try:
            with httpx.Client() as client:
                response = client.get(
                    url,
                    follow_redirects=True,
                    auth=(CONFIG["username"], CONFIG["password"]),
                    timeout=60,
                )
                response.raise_for_status()

                root = etree.fromstring(response.text)

                with open(f".temp/{table_name}.xml", "wb") as f:
                    f.write(etree.tostring(root, pretty_print=True))

        except httpx.HTTPError as e:
            print(f"HTTP Error: {e}")

    def _xml_to_model(
        self,
        table_name: str,
        model: BaseModel,
        parent_dir: str = ".temp",
    ) -> list:
        """
            Convert the xml file to the pydantic model
        Args:
            table_name (str): _description_

        Returns:
            list: _description_
        """
        lines = []

        with open(f"{parent_dir}/{table_name}.xml", "r") as f:
            contents = f.read()

        soup = bs(contents, "xml")
        rows = soup.find_all("content")

        for row in rows:
            line = {}
            columns = row.find("properties").find_all()

            for column in columns:
                line[column.name] = column.text.strip()

            lines.append(line)

        # Convert the data to the pydantic model
        model_data = [model(**item) for item in lines]

        return model_data

    def _xml_to_df(self, table_name: str) -> pd.DataFrame:
        """
            Convert the xml file to the csv
        Args:
            table_name (str): _description_

        Returns:
            Path to the csv file
        """

        lines = []

        with open(f".temp/{table_name}.xml", "r") as f:
            contents = f.read()

        soup = bs(contents, "xml")
        rows = soup.find_all("content")

        for row in rows:
            line = {}
            columns = row.find("properties").find_all()

            for column in columns:
                line[column.name] = column.text.strip()

            lines.append(line)

        df = pl.DataFrame(lines).to_pandas()

        return df

    def _build_insert_query(self, table_name: str, model: List[BaseModel]):
        print(f"=> Building query for table: {table_name}...")
        columns = list(model[0].model_dump().keys())

        query = f"INSERT INTO {table_name} ({','.join(columns)})\nVALUES\n"

        for value in model:
            query += "("
            # Query need to handel for the case string value or int, float value (no quote)
            for column in columns:
                if isinstance(getattr(value, column), str):
                    query += f'"{getattr(value, column)}",'
                else:
                    query += f"{getattr(value, column)},"

            query = query[:-1] + "),\n"

        # Remove the last comma and new line character
        query = query[:-2]

        return query + ";"

    def _fetch_data(self, url: str):
        """
            Reload the data from the server
        Args:
            url (str): The url to the server
        """

        table = url.split("/")[-1]
        print(f'Fetching data of table: "{table}"...')

        # Remove the old xml file
        if os.path.exists(f".temp/{table}.xml"):
            os.remove(f".temp/{table}.xml")

        # Fetch the data
        self._fetch_xml(url=url, table_name=table)

        print(f'Table "{table}" is fetched successfully!')

        return table

    def _insert_db(self, table_name: str, conn: sqlite3.Connection):
        print(f'=> Pushing data of table: "{table_name}"...')

        model = table_to_model[table_name]
        model_data = self._xml_to_model(table_name=table_name, model=model)
        if model_data == []:
            print("=> No data to push!")
        else:
            query = self._build_insert_query(table_name=table_name, model=model_data)
            conn.executescript(query)
            conn.commit()

    def run(self):
        while True:
            start_time = time.time()
            # Connect to the database
            self.conn = sqlite3.connect("erp.db")

            datetime_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"========>> [{datetime_now}] - Refreshing data...")

            print("===> Recreating the database...")
            init_db(self.tables)

            print("===> Fetching data")

            done_tables = []

            with ThreadPoolExecutor(max_workers=22) as executor:
                futures = [executor.submit(self._fetch_data, url) for url in self.urls]

                for future in as_completed(futures):
                    table: str = future.result()
                    done_tables.append(table)

            print("===> Pushing data to the database...")

            self.xmls_to_models(folder_dir=".temp")
            print(f"Time taken: {time.time() - start_time} seconds")

            with open("configs/games.json", "r") as f:
                CONFIG = json.load(f)

            print(f"===> Next run: {CONFIG['auto_refresh']} seconds")

            for i in range(CONFIG["auto_refresh"]):
                print(f"===> {CONFIG['auto_refresh'] - i} seconds left", end="\r")
                time.sleep(1)

            print("\n\n")

    def __subprocess_xmls_to_models(self, table: str, folder_dir: str):
        if table in (
            "Carbon_Emissions.xml",
            "Current_Game_Rules.xml",
            "Stock_Transfers.xml",
            "NPS_Surveys.xml",
        ):
            return

        just_name = table.split(".")[0]
        if just_name == "":  # .placeholder
            return

        model = table_to_model[just_name]
        model_data = self._xml_to_model(
            table_name=just_name, model=model, parent_dir=folder_dir
        )

        # Insert the data to the database
        conn = sqlite3.connect("erp.db")
        query = self._build_insert_query(table_name=just_name, model=model_data)

        if model_data == []:
            return f"No data to push for table: {just_name}"
        else:
            try:
                conn.executescript(query)
                conn.commit()
            except Exception:
                print(traceback.format_exc())  # noqa: F821
                print(f"Query: {query}")
                return

            conn.close()
            return f"Data of table: {just_name} is pushed successfully!"

    def xmls_to_models(self, folder_dir: str):
        if not os.path.exists(folder_dir):
            raise FileNotFoundError(f"Folder {folder_dir} not found!")

        # Recreate the database
        init_db(self.tables)

        tables = os.listdir(folder_dir)

        # In this case, don't use ThreadPoolExecutor will be faster
        for table in tables:
            result = self.__subprocess_xmls_to_models(table, folder_dir)
            if result:
                print(result)

        # with ThreadPoolExecutor(max_workers=1) as executor:
        #     futures = [
        #         executor.submit(self.__subprocess_xmls_to_models, table, folder_dir)
        #         for table in tables
        #     ]

        #     for idx, future in enumerate(as_completed(futures)):
        #         print(f"Processing table {idx + 1}/{len(tables)}...")
        #         result = future.result()

        #         if result:
        #             print(result)

    def xmls_to_csvs(self, fetch_data: bool = False):
        if fetch_data:
            # Fetch the data
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [
                    executor.submit(self._fetch_xml, url, table_name)
                    for url, table_name in zip(self.urls, self.tables)
                ]

                for idx, future in enumerate(as_completed(futures)):
                    future.result()

        # Convert the xml to csv
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {}

            for table in self.tables:
                futures[table] = executor.submit(self._xml_to_df, table)

            for table, future in futures.items():
                future.result().to_csv(f"output/{table}.csv")


if __name__ == "__main__":
    main_url = CONFIG["data_source_link"]

    tables = [
        "BOM_Changes",
        "Carbon_Emissions",
        "Company_Valuation",
        "Financial_Postings",
        "Goods_Movements",
        "Independent_Requirements",
        "Purchase_Orders",
        "Production_Orders",
        "Inventory",
        "Current_Inventory",
        "Current_Inventory_KPI",
        "Current_Suppliers_Prices",
        "Market",
        "Marketing_Expenses",
        "Pricing_Conditions",
        "Production",
        "Current_Game_Rules",
        "Sales",
        "Suppliers_Prices",
        "Stock_Transfers",
    ]

    data_refresher = DataRefresher(main_url=main_url, tables=tables)

    data_refresher.run()

    # start_time = time.time()
    # data_refresher.xmls_to_models(folder_dir=".temp")
    # print(f"Time taken: {time.time() - start_time} seconds")

    # data_refresher.xmls_to_csvs()
