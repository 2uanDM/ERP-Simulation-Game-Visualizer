import os
import sys
import time
sys.path.append(os.getcwd())  # NOQA

import json
import httpx
import sqlite3
import polars as pl

from lxml import etree
from bs4 import BeautifulSoup as bs
from typing import List
from pydantic import BaseModel

from database.schema import Market
from database.init_db import init_db


with open('configs/games.json', 'r') as f:
    CONFIG = json.load(f)


class ProcessXML():
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
        self.urls = [f"{main_url}/{table}" if main_url[-1] != "/" else f"{main_url}{table}" for table in tables]

        # Connect to the database
        self.conn = sqlite3.connect('erp.db')

    def _fetch_xml(self, url: str, table_name: str = None):
        try:
            with httpx.Client() as client:
                response = client.get(url, follow_redirects=True, auth=(CONFIG['username'], CONFIG['password']))
                response.raise_for_status()

                root = etree.fromstring(response.text)

                with open(f".temp/{table_name}.xml", "wb") as f:
                    f.write(etree.tostring(root, pretty_print=True))

        except httpx.HTTPError as e:
            print(f"HTTP Error: {e}")

    def _xml_to_model(self, table_name: str, model: BaseModel) -> list:
        """
            Convert the xml file to the pydantic model
        Args:
            table_name (str): _description_

        Returns:
            list: _description_
        """
        lines = []

        with open(f".temp/{table_name}.xml", "r") as f:
            contents = f.read()

        soup = bs(contents, 'xml')
        rows = soup.find_all('content')

        for row in rows:
            line = {}
            columns = row.find('properties').find_all()

            for column in columns:
                line[column.name] = column.text.strip()

            lines.append(line)

        # Convert the data to the pydantic model
        model_data = [model(**item) for item in lines]

        return model_data

    def _build_insert_query(self, table_name: str, model: List[BaseModel]):
        columns = list(model[0].model_dump().keys())

        query = f"INSERT INTO {table_name} ({','.join(columns)})\nVALUES\n"

        for value in model:
            query += "("
            # Query need to handel for the case string value or int, float value (no quote)
            for column in columns:
                if isinstance(getattr(value, column), str):
                    query += f"'{getattr(value, column)}',"
                else:
                    query += f"{getattr(value, column)},"

            query = query[:-1] + "),\n"

        # Remove the last comma and new line character
        query = query[:-2]

        return query + ";"


if __name__ == '__main__':
    main_url = "https://kosovo.cob.csuchico.edu:8025/odata/305"
    tables = ['Company_Valuation', 'Market', 'Inventory']

    while True:
        print('==>> Fetching data...')

        # Remove the old xml file
        if os.path.exists('.temp/Market.xml'):
            os.remove('.temp/Market.xml')

        # Init the DB
        init_db()

        # Fetch the data
        worker = ProcessXML(main_url, tables)
        worker._fetch_xml(
            url="https://kosovo.cob.csuchico.edu:8025/odata/305/Market",
            table_name="Market")

        # Convert the xml file to the pydantic model
        market_model = worker._xml_to_model("Market", model=Market)

        # Insert the data to the database
        conn = sqlite3.connect('erp.db')

        query = worker._build_insert_query(
            table_name="Market",
            model=market_model
        )

        conn.execute(query)
        conn.commit()
        conn.close()

        for i in range(30):
            print(f"==>> {30 - i} seconds left", end='\r')
            time.sleep(1)
