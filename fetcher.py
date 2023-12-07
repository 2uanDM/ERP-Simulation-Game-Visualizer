import os
import sys
import time
sys.path.append(os.getcwd())  # NOQA

import json
import httpx
import sqlite3

from lxml import etree
from bs4 import BeautifulSoup as bs
from typing import List
from pydantic import BaseModel
from datetime import datetime

from database.schema import Market
from database.init_db import init_db

from concurrent.futures import ThreadPoolExecutor, as_completed


with open('configs/games.json', 'r') as f:
    CONFIG = json.load(f)


table_to_model = {
    'Market': Market
}


class DataRefresher():
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

    def _fetch_data(self, url: str):
        """
            Reload the data from the server
        Args:
            url (str): The url to the server
        """

        table = url.split('/')[-1]
        print(f'Fetching data of table: "{table}"...')

        # Remove the old xml file
        if os.path.exists(f'.temp/{table}.xml'):
            os.remove(f'.temp/{table}.xml')

        # Fetch the data
        self._fetch_xml(url=url, table_name=table)

        print(f'Table "{table}" is updated successfully!')

        return table

    def run(self):
        while True:
            # Connect to the database
            self.conn = sqlite3.connect('erp.db')

            datetime_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"========>> [{datetime_now}] - Refreshing data...")

            print('===> Recreating the database...')
            init_db(self.tables)

            print('===> Fetching data')

            done_tables = []

            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(self._fetch_data, url) for url in self.urls]

                for future in as_completed(futures):
                    table: str = future.result()
                    done_tables.append(table)

            print('===> Pushing data to the database...')

            for table in done_tables:
                print(f'=> Pushing data of table: "{table}"...')
                model = table_to_model[table]
                model_data = self._xml_to_model(table_name=table, model=model)
                query = self._build_insert_query(table_name=table, model=model_data)

                self.conn.executescript(query)

            print('===> Done pushing to database!')
            print('===> Closing the connection...')

            # Close the connection
            self.conn.close()

            with open('configs/games.json', 'r') as f:
                CONFIG = json.load(f)

            print(f"===> Next run: {CONFIG['auto_refresh']} seconds")

            for i in range(CONFIG['auto_refresh']):
                print(f"===> {CONFIG['auto_refresh'] - i} seconds left", end='\r')
                time.sleep(1)

            print('\n\n')


if __name__ == '__main__':
    main_url = CONFIG['data_source_link']
    tables = ['Market']

    data_refresher = DataRefresher(main_url=main_url, tables=tables)

    data_refresher.run()
