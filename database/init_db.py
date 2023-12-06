import sqlite3
import os
import sys
sys.path.append(os.getcwd())


def _create_market_table(conn):
    conn.execute("""
        CREATE TABLE Market (
        ID TEXT,
        ROW_ID INTEGER PRIMARY KEY,
        COMPANY_CODE TEXT,
        SALES_ORGANIZATION TEXT,
        SIM_ROUND TEXT,
        SIM_PERIOD INTEGER,
        MATERIAL_DESCRIPTION TEXT CONSTRAINT fk_product REFERENCES Product (NAME) ON DELETE CASCADE ON UPDATE CASCADE,
        DISTRIBUTION_CHANNEL INTEGER CONSTRAINT fk_distribution_channel REFERENCES Distribution_Channel (CHANNEL) ON DELETE CASCADE ON UPDATE CASCADE,
        AREA TEXT CONSTRAINT fk_area REFERENCES Area (NAME) ON DELETE CASCADE ON UPDATE CASCADE,
        QUANTITY INTEGER,
        UNIT TEXT,
        AVERAGE_PRICE REAL,
        NET_VALUE REAL,
        CURRENCY TEXT
    );
    """)

    # Save (commit) the changes
    conn.commit()

    print("==>> Created the Market table")


def init_db():
    db_path = os.path.join(os.getcwd(), 'erp.db')

    # Create the database file and connect to it
    conn = sqlite3.connect(db_path)

    # If the table exists, drop it
    list_tables = ['Market']

    for table in list_tables:
        conn.execute(f"DROP TABLE IF EXISTS {table};")

    # Create the tables
    _create_market_table(conn)


if __name__ == '__main__':
    init_db()  # Just admin can run this script
