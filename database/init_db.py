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


def _create_inventory_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Inventory (
            ID TEXT,
            ROW_ID INTEGER PRIMARY KEY,
            PLANT TEXT,
            SIM_ROUND TEXT,
            SIM_STEP TEXT,
            SIM_DATE TEXT,
            SIM_CALENDAR_DATE TEXT,
            SIM_PERIOD INTEGER,
            SIM_ELAPSED_STEPS INTEGER,
            STORAGE_LOCATION TEXT,
            MATERIAL_NUMBER TEXT,
            MATERIAL_DESCRIPTION TEXT,
            MATERIAL_TYPE TEXT,
            MATERIAL_CODE TEXT,
            MATERIAL_SIZE TEXT,
            MATERIAL_LABEL TEXT,
            INVENTORY_OPENING_BALANCE INTEGER,
            UNIT TEXT
        );
    """)

    # Save (commit) the changes
    conn.commit()

    print("==>> Created the Inventory table")


def _create_current_inventory_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Current_Inventory (
            ID TEXT,
            ROW_ID INTEGER PRIMARY KEY,
            PLANT TEXT,
            MATERIAL_NUMBER TEXT,
            MATERIAL_DESCRIPTION TEXT,
            STORAGE_LOCATION TEXT,
            STOCK REAL,
            RESTRICTED REAL,
            UNIT TEXT
        );
    """)

    # Save (commit) the changes
    conn.commit()

    print("==>> Created the Current_Inventory table")


def init_db(list_tables: list = []):
    """
        Drop all tables and create them again

    Args:
        list_tables (list, optional): Defaults to []
    """

    db_path = os.path.join(os.getcwd(), 'erp.db')

    # Create the database file and connect to it
    conn = sqlite3.connect(db_path)

    for table in list_tables:
        conn.execute(f"DROP TABLE IF EXISTS {table};")

    # Create the tables
    if 'Market' in list_tables:
        _create_market_table(conn)
    if 'Inventory' in list_tables:
        _create_inventory_table(conn)
    if 'Current_Inventory' in list_tables:
        _create_current_inventory_table(conn)


if __name__ == '__main__':
    init_db()  # Just admin can run this script
