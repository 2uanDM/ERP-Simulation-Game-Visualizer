import os
import sqlite3
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
            MATERIAL_DESCRIPTION TEXT,
            DISTRIBUTION_CHANNEL INTEGER,
            AREA TEXT,
            QUANTITY INTEGER,
            UNIT TEXT,
            AVERAGE_PRICE REAL,
            NET_VALUE REAL,
            CURRENCY TEXT);
        """)
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
    conn.commit()
    print("==>> Created the Current_Inventory table")


def _create_current_inventory_kpi_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Current_Inventory_KPI (
            ID TEXT,
            ROW_ID INTEGER PRIMARY KEY,
            PLANT TEXT,
            STORAGE_LOCATION TEXT,
            MATERIAL_NUMBER TEXT,
            MATERIAL_DESCRIPTION TEXT,
            MATERIAL_TYPE TEXT,
            MATERIAL_CODE TEXT,
            MATERIAL_SIZE TEXT,
            MATERIAL_LABEL TEXT,
            CURRENT_INVENTORY INTEGER,
            QUANTITY_SOLD INTEGER,
            UNIT TEXT,
            NB_STEPS_AVAILABLE INTEGER,
            SIM_ELAPSED_STEPS INTEGER
        );
    """)
    conn.commit()
    print("==>> Created the Current_Inventory_KPI table")


def _create_bom_changes_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS BOM_Changes (
            ID TEXT,
            ROW_ID INTEGER PRIMARY KEY,
            PLANT TEXT,
            SIM_ROUND TEXT,
            SIM_STEP INTEGER,
            SIM_DATE TEXT,
            SIM_CALENDAR_DATE TEXT,
            SIM_PERIOD INTEGER,
            SIM_ELAPSED_STEPS INTEGER,
            MATERIAL_NUMBER TEXT,
            ITEM TEXT,
            COMPONENT TEXT,
            MATERIAL_DESCRIPTION TEXT,
            QUANTITY REAL,
            UNIT TEXT,
            USER_NAME TEXT,
            CHANGE_TIME TEXT
        );
    """)
    conn.commit()
    print("==>> Created the BOM_Changes table")


def _create_company_valuation_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Company_Valuation (
            ID TEXT,
            ROW_ID INTEGER PRIMARY KEY,
            COMPANY_CODE TEXT,
            SIM_ROUND TEXT,
            SIM_STEP INTEGER,
            SIM_DATE TEXT,
            SIM_CALENDAR_DATE TEXT,
            SIM_PERIOD INTEGER,
            SIM_ELAPSED_STEPS INTEGER,
            BANK_CASH_ACCOUNT REAL,
            ACCOUNTS_RECEIVABLE REAL,
            BANK_LOAN REAL,
            ACCOUNTS_PAYABLE REAL,
            PROFIT REAL,
            SETUP_TIME_INVESTMENT REAL,
            DEBT_LOADING REAL,
            CREDIT_RATING TEXT,
            COMPANY_RISK_RATE_PCT REAL,
            MARKET_RISK_RATE_PCT REAL,
            COMPANY_VALUATION REAL,
            DEBT_LOADING_UNADJUSTED REAL,
            CREDIT_RATING_UNADJUSTED TEXT,
            COMPANY_RISK_RATE_UNADJUSTED REAL,
            COMPANY_VALUATION_UNADJUSTED REAL,
            CURRENCY TEXT
        );
    """)
    conn.commit()
    print("==>> Created the Company_Valuation table")


def _create_current_suppliers_prices_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Current_Suppliers_Prices (
            ID TEXT,
            ROW_ID INTEGER PRIMARY KEY,
            PURCHASING_ORGANIZATION TEXT,
            MATERIAL_NUMBER TEXT,
            MATERIAL_DESCRIPTION TEXT,
            VENDOR_CODE TEXT,
            VENDOR_NAME TEXT,
            NET_PRICE REAL,
            CURRENCY TEXT
        );
    """)
    conn.commit()
    print("==>> Created the Current_Suppliers_Prices table")


def _create_financial_postings_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Financial_Postings (
            ID TEXT,
            ROW_ID INTEGER PRIMARY KEY,
            COMPANY_CODE TEXT,
            SIM_ROUND TEXT,
            SIM_STEP INTEGER,
            SIM_DATE TEXT,
            SIM_CALENDAR_DATE TEXT,
            SIM_PERIOD INTEGER,
            SIM_ELAPSED_STEPS INTEGER,
            GL_ACCOUNT_NUMBER TEXT,
            GL_ACCOUNT_NAME TEXT,
            FS_LEVEL_1 TEXT,
            FS_LEVEL_2 TEXT,
            FS_LEVEL_3 TEXT,
            FS_LEVEL_4 TEXT,
            DEBIT_CREDIT_INDICATOR TEXT,
            AMOUNT_ABS REAL,
            AMOUNT REAL,
            AMOUNT_INV REAL,
            AMOUNT_BS REAL,
            AMOUNT_IS REAL,
            CURRENCY TEXT
        );
    """)
    conn.commit()
    print("==>> Created the Financial_Postings table")


def _create_goods_movements_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Goods_Movements (
            ID TEXT,
            ROW_ID INTEGER PRIMARY KEY,
            PLANT TEXT,
            SIM_ROUND TEXT,
            SIM_STEP INTEGER,
            SIM_DATE TEXT,
            SIM_CALENDAR_DATE TEXT,
            SIM_PERIOD INTEGER,
            SIM_ELAPSED_STEPS INTEGER,
            EVENT_TYPE TEXT,
            DOCUMENT_TYPE TEXT,
            MOVEMENT_TYPE TEXT,
            STORAGE_LOCATION TEXT,
            MATERIAL_NUMBER TEXT,
            MATERIAL_DESCRIPTION TEXT,
            MATERIAL_TYPE TEXT,
            MATERIAL_CODE TEXT,
            MATERIAL_SIZE TEXT,
            MATERIAL_LABEL TEXT,
            MATERIAL_DOCUMENT TEXT,
            DEBIT_CREDIT_INDICATOR TEXT,
            UNIT TEXT,
            QUANTITY_ABS REAL,
            QUANTITY REAL
        );
    """)
    conn.commit()
    print("==>> Created the Goods_Movements table")


def _create_independent_requirements_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Independent_Requirements (
            ID TEXT,
            ROW_ID INTEGER PRIMARY KEY,
            PLANT TEXT,
            SIM_ROUND TEXT,
            SIM_STEP INTEGER,
            SIM_DATE TEXT,
            SIM_CALENDAR_DATE TEXT,
            SIM_PERIOD INTEGER,
            SIM_ELAPSED_STEPS INTEGER,
            MATERIAL_NUMBER TEXT,
            QUANTITY INTEGER,
            UNIT TEXT
        );
    """)
    conn.commit()
    print("==>> Created the Independent_Requirements table")


def _create_marketing_expenses_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Marketing_Expenses (
            ID TEXT,
            ROW_ID INTEGER PRIMARY KEY,
            SALES_ORGANIZATION TEXT,
            SIM_ROUND TEXT,
            SIM_STEP INTEGER,
            SIM_DATE TEXT,
            SIM_CALENDAR_DATE TEXT,
            SIM_PERIOD INTEGER,
            SIM_ELAPSED_STEPS INTEGER,
            MATERIAL_NUMBER TEXT,
            MATERIAL_DESCRIPTION TEXT,
            AREA TEXT,
            AMOUNT REAL,
            CURRENCY TEXT
        );
    """)
    conn.commit()
    print("==>> Created the Marketing_Expenses table")


def _create_nps_surveys_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS NPS_Surveys (
            ID TEXT,
            ROW_ID INTEGER PRIMARY KEY,
            SIM_ROUND TEXT,
            SIM_STEP INTEGER,
            SIM_DATE TEXT,
            SIM_CALENDAR_DATE TEXT,
            SIM_PERIOD INTEGER,
            SIM_ELAPSED_STEPS INTEGER,
            PLANT TEXT,
            TYPE TEXT,
            MATERIAL_NUMBER TEXT,
            MATERIAL_DESCRIPTION TEXT,
            MATERIAL_TYPE TEXT,
            MATERIAL_CODE TEXT,
            MATERIAL_SIZE TEXT,
            MATERIAL_LABEL TEXT,
            CUSTOMER_NUMBER TEXT,
            COUNTRY TEXT,
            CITY TEXT,
            POSTAL_CODE TEXT,
            REGION TEXT,
            AREA TEXT,
            DISTRIBUTION_CHANNEL TEXT,
            SCORE_0 INTEGER,
            SCORE_1 INTEGER,
            SCORE_2 INTEGER,
            SCORE_3 INTEGER,
            SCORE_4 INTEGER,
            SCORE_5 INTEGER,
            SCORE_6 INTEGER,
            SCORE_7 INTEGER,
            SCORE_8 INTEGER,
            SCORE_9 INTEGER,
            SCORE_10 INTEGER
        );
    """)
    conn.commit()
    print("==>> Created the NPS_Surveys table")


def _create_pricing_conditions_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Pricing_Conditions (
            ID TEXT,
            ROW_ID INTEGER PRIMARY KEY,
            SALES_ORGANIZATION TEXT,
            SIM_ROUND TEXT,
            SIM_STEP INTEGER,
            SIM_DATE TEXT,
            SIM_CALENDAR_DATE TEXT,
            SIM_PERIOD INTEGER,
            SIM_ELAPSED_STEPS INTEGER,
            MATERIAL_NUMBER TEXT,
            MATERIAL_DESCRIPTION TEXT,
            DISTRIBUTION_CHANNEL TEXT,
            DC_NAME TEXT,
            PRICE REAL,
            CURRENCY TEXT
        );
    """)
    conn.commit()
    print("==>> Created the Pricing_Conditions table")


def _create_production_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Production (
            ID TEXT,
            ROW_ID INTEGER PRIMARY KEY,
            COMPANY_CODE TEXT,
            SIM_ROUND TEXT,
            SIM_STEP INTEGER,
            SIM_DATE TEXT,
            SIM_CALENDAR_DATE TEXT,
            SIM_PERIOD INTEGER,
            SIM_ELAPSED_STEPS INTEGER,
            MATERIAL_NUMBER TEXT,
            MATERIAL_DESCRIPTION TEXT,
            MATERIAL_SIZE TEXT,
            MATERIAL_LABEL TEXT,
            MATERIAL_CODE TEXT,
            YIELD TEXT,
            UNIT TEXT
        );
    """)
    conn.commit()
    print("==>> Created the Production table")


def _create_production_orders_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Production_Orders (
            ID TEXT,
            ROW_ID INTEGER PRIMARY KEY,
            COMPANY_CODE TEXT,
            SIM_ROUND TEXT,
            SIM_STEP INTEGER,
            SIM_DATE TEXT,
            SIM_CALENDAR_DATE TEXT,
            SIM_PERIOD INTEGER,
            SIM_ELAPSED_STEPS INTEGER,
            PRODUCTION_ORDER TEXT,
            MATERIAL_NUMBER TEXT,
            MATERIAL_DESCRIPTION TEXT,
            BEGIN_ROUND TEXT,
            BEGIN_STEP INTEGER,
            END_ROUND TEXT,
            END_STEP INTEGER,
            TARGET_QUANTITY INTEGER,
            CONFIRMED_QUANTITY INTEGER,
            UNIT TEXT,
            SETUP_TIME INTEGER
        );
    """)
    conn.commit()
    print("==>> Created the Production_Orders table")


def _create_purchase_orders_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Purchase_Orders (
            ID TEXT,
            ROW_ID INTEGER PRIMARY KEY,
            COMPANY_CODE TEXT,
            SIM_ROUND TEXT,
            SIM_STEP INTEGER,
            SIM_DATE TEXT,
            SIM_CALENDAR_DATE TEXT,
            SIM_PERIOD INTEGER,
            SIM_ELAPSED_STEPS INTEGER,
            PURCHASING_ORDER TEXT,
            VENDOR TEXT,
            MATERIAL_NUMBER TEXT,
            MATERIAL_DESCRIPTION TEXT,
            QUANTITY REAL,
            STATUS TEXT,
            UNIT TEXT,
            GOODS_RECEIPT_ROUND TEXT,
            GOODS_RECEIPT_STEP INTEGER,
            GOODS_RECEIPT_DATE TEXT
        );
    """)
    conn.commit()
    print("==>> Created the Purchase_Orders table")


def _create_sales_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Sales (
            ID TEXT,
            ROW_ID INTEGER PRIMARY KEY,
            SALES_ORGANIZATION TEXT,
            SIM_ROUND TEXT,
            SIM_STEP INTEGER,
            SIM_DATE TEXT,
            SIM_CALENDAR_DATE TEXT,
            SIM_PERIOD INTEGER,
            SIM_ELAPSED_STEPS INTEGER,
            SALES_ORDER_NUMBER INTEGER,
            LINE_ITEM INTEGER,
            STORAGE_LOCATION TEXT,
            REGION TEXT,
            AREA TEXT,
            CITY TEXT,
            COUNTRY TEXT,
            POSTAL_CODE TEXT,
            CUSTOMER_NUMBER TEXT,
            DISTRIBUTION_CHANNEL INTEGER,
            MATERIAL_NUMBER TEXT,
            MATERIAL_DESCRIPTION TEXT,
            MATERIAL_TYPE TEXT,
            MATERIAL_CODE TEXT,
            MATERIAL_SIZE TEXT,
            MATERIAL_LABEL TEXT,
            QUANTITY INTEGER,
            QUANTITY_DELIVERED INTEGER,
            UNIT TEXT,
            NET_PRICE REAL,
            NET_VALUE REAL,
            COST REAL,
            CURRENCY TEXT,
            CONTRIBUTION_MARGIN REAL,
            CONTRIBUTION_MARGIN_PCT REAL
        );
    """)
    conn.commit()
    print("==>> Created the Sales table")


def _create_suppliers_prices_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Suppliers_Prices (
            ID TEXT,
            ROW_ID INTEGER PRIMARY KEY,
            PURCHASING_ORGANIZATION TEXT,
            SIM_ROUND TEXT,
            SIM_STEP INTEGER,
            SIM_DATE TEXT,
            SIM_CALENDAR_DATE TEXT,
            SIM_PERIOD INTEGER,
            SIM_ELAPSED_STEPS INTEGER,
            MATERIAL_NUMBER TEXT,
            MATERIAL_DESCRIPTION TEXT,
            MATERIAL_TYPE TEXT,
            VENDOR_CODE TEXT,
            VENDOR_NAME TEXT,
            NET_PRICE REAL,
            CURRENCY TEXT
        );
    """)
    conn.commit()
    print("==>> Created the Suppliers_Prices table")


def init_db(list_tables: list = []):
    """
    Drop all tables and create them again

    Args:
        list_tables (list, optional): Defaults to []
    """
    db_path = os.path.join(os.getcwd(), "erp.db")
    conn = sqlite3.connect(db_path)

    for table in list_tables:
        conn.execute(f"DROP TABLE IF EXISTS {table};")

    if "Market" in list_tables:
        _create_market_table(conn)
    if "Inventory" in list_tables:
        _create_inventory_table(conn)
    if "Current_Inventory" in list_tables:
        _create_current_inventory_table(conn)
    if "Current_Inventory_KPI" in list_tables:
        _create_current_inventory_kpi_table(conn)
    if "BOM_Changes" in list_tables:
        _create_bom_changes_table(conn)
    if "Company_Valuation" in list_tables:
        _create_company_valuation_table(conn)
    if "Current_Suppliers_Prices" in list_tables:
        _create_current_suppliers_prices_table(conn)
    if "Financial_Postings" in list_tables:
        _create_financial_postings_table(conn)
    if "Goods_Movements" in list_tables:
        _create_goods_movements_table(conn)
    if "Independent_Requirements" in list_tables:
        _create_independent_requirements_table(conn)
    if "Marketing_Expenses" in list_tables:
        _create_marketing_expenses_table(conn)
    if "NPS_Surveys" in list_tables:
        _create_nps_surveys_table(conn)
    if "Pricing_Conditions" in list_tables:
        _create_pricing_conditions_table(conn)
    if "Production" in list_tables:
        _create_production_table(conn)
    if "Production_Orders" in list_tables:
        _create_production_orders_table(conn)
    if "Purchase_Orders" in list_tables:
        _create_purchase_orders_table(conn)
    if "Sales" in list_tables:
        _create_sales_table(conn)
    if "Suppliers_Prices" in list_tables:
        _create_suppliers_prices_table(conn)

    conn.close()


if __name__ == "__main__":
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
        "NPS_Surveys",
        "Pricing_Conditions",
        "Production",
        "Current_Game_Rules",
        "Sales",
        "Suppliers_Prices",
        "Stock_Transfers",
    ]

    init_db(tables)
