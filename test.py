import sqlite3
import polars as pl

from database.schema import Inventory


conn = sqlite3.connect('erp.db')

data = conn.execute("""
    SELECT * FROM Inventory
    """).fetchall()

data = []

# Convert the data to a dataframe
if data == []:
    df = pl.DataFrame().to_pandas()
else:
    df = pl.DataFrame(data).to_pandas()

df.columns = Inventory.__annotations__.keys()

print(df)
