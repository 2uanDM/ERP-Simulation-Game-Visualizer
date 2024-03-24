from typing import Optional

from pydantic import BaseModel


class Market(BaseModel):
    ID: str
    ROW_ID: int  # Primary Key
    COMPANY_CODE: str
    SALES_ORGANIZATION: str
    SIM_ROUND: int
    SIM_PERIOD: int
    MATERIAL_DESCRIPTION: str
    DISTRIBUTION_CHANNEL: int
    AREA: str
    QUANTITY: int
    UNIT: str
    AVERAGE_PRICE: float
    NET_VALUE: float
    CURRENCY: str


class Inventory(BaseModel):
    ID: Optional[str]
    ROW_ID: int  # Primary Key
    PLANT: str
    SIM_ROUND: str
    SIM_STEP: str
    SIM_DATE: str
    SIM_CALENDAR_DATE: str
    SIM_PERIOD: int
    SIM_ELAPSED_STEPS: int
    STORAGE_LOCATION: str
    MATERIAL_NUMBER: str
    MATERIAL_DESCRIPTION: str
    MATERIAL_TYPE: str
    MATERIAL_CODE: str
    MATERIAL_SIZE: str
    MATERIAL_LABEL: str
    INVENTORY_OPENING_BALANCE: float
    UNIT: str


class Current_Inventory(BaseModel):
    ID: Optional[str]
    ROW_ID: int
    PLANT: str
    MATERIAL_NUMBER: str
    MATERIAL_DESCRIPTION: str
    STORAGE_LOCATION: str
    STOCK: float
    RESTRICTED: float
    UNIT: str


class Current_Inventory_KPI(BaseModel):
    ID: Optional[str]
    ROW_ID: int
    PLANT: str
    STORAGE_LOCATION: str
    MATERIAL_NUMBER: str
    MATERIAL_DESCRIPTION: str
    MATERIAL_TYPE: str
    MATERIAL_CODE: str
    MATERIAL_SIZE: str
    MATERIAL_LABEL: str
    CURRENT_INVENTORY: int
    QUANTITY_SOLD: int
    UNIT: str
    NB_STEPS_AVAILABLE: int
    SIM_ELAPSED_STEPS: int


class BOM_Changes(BaseModel):
    ID: Optional[str]
    ROW_ID: int
    PLANT: str
    SIM_ROUND: str
    SIM_STEP: int
    SIM_DATE: str
    SIM_CALENDAR_DATE: str
    SIM_PERIOD: int
    SIM_ELAPSED_STEPS: int
    MATERIAL_NUMBER: str
    ITEM: str
    COMPONENT: str
    MATERIAL_DESCRIPTION: str
    QUANTITY: float
    UNIT: str
    USER_NAME: str
    CHANGE_TIME: str


class Company_Valuation(BaseModel):
    ID: Optional[str]
    ROW_ID: int
    COMPANY_CODE: str
    SIM_ROUND: str
    SIM_STEP: int
    SIM_DATE: str
    SIM_CALENDAR_DATE: str
    SIM_PERIOD: int
    SIM_ELAPSED_STEPS: int
    BANK_CASH_ACCOUNT: float
    ACCOUNTS_RECEIVABLE: float
    BANK_LOAN: float
    ACCOUNTS_PAYABLE: float
    PROFIT: float
    SETUP_TIME_INVESTMENT: float
    DEBT_LOADING: float
    CREDIT_RATING: str
    COMPANY_RISK_RATE_PCT: float
    MARKET_RISK_RATE_PCT: float
    COMPANY_VALUATION: float
    DEBT_LOADING_UNADJUSTED: float
    CREDIT_RATING_UNADJUSTED: float
    COMPANY_RISK_RATE_UNADJUSTED: float
    COMPANY_VALUATION_UNADJUSTED: float
    CURRENCY: str


class Current_Suppliers_Prices(BaseModel):
    ID: Optional[str]
    ROW_ID: int
    PURCHASING_ORGANIZATION: str
    MATERIAL_NUMBER: str
    MATERIAL_DESCRIPTION: str
    VENDOR_CODE: str
    VENDOR_NAME: str
    NET_PRICE: float
    CURRENCY: str


class Financial_Postings(BaseModel):
    ID: Optional[str]
    ROW_ID: int
    COMPANY_CODE: str
    SIM_ROUND: str
    SIM_STEP: int
    SIM_DATE: str
    SIM_CALENDAR_DATE: str
    SIM_PERIOD: int
    SIM_ELAPSED_STEPS: int
    GL_ACCOUNT_NUMBER: str
    GL_ACCOUNT_NAME: str
    FS_LEVEL_1: str
    FS_LEVEL_2: str
    FS_LEVEL_3: str
    FS_LEVEL_4: str
    DEBIT_CREDIT_INDICATOR: str
    AMOUNT_ABS: float
    AMOUNT: float
    AMOUNT_INV: float
    AMOUNT_BS: float
    AMOUNT_IS: float
    CURRENCY: str


class Goods_Movements(BaseModel):
    ID: Optional[str]
    ROW_ID: int
    PLANT: str
    SIM_ROUND: str
    SIM_STEP: int
    SIM_DATE: str
    SIM_CALENDAR_DATE: str
    SIM_PERIOD: int
    SIM_ELAPSED_STEPS: int
    EVENT_TYPE: str
    DOCUMENT_TYPE: str
    MOVEMENT_TYPE: str
    STORAGE_LOCATION: str
    MATERIAL_NUMBER: str
    MATERIAL_DESCRIPTION: str
    MATERIAL_TYPE: str
    MATERIAL_CODE: str
    MATERIAL_SIZE: str
    MATERIAL_LABEL: str
    MATERIAL_DOCUMENT: str
    DEBIT_CREDIT_INDICATOR: str
    UNIT: str
    QUANTITY_ABS: float
    QUANTITY: float


class Independent_Requirements(BaseModel):
    ID: Optional[str]
    ROW_ID: int
    PLANT: str
    SIM_ROUND: str
    SIM_STEP: int
    SIM_DATE: str
    SIM_CALENDAR_DATE: str
    SIM_PERIOD: int
    SIM_ELAPSED_STEPS: int
    MATERIAL_NUMBER: str
    QUANTITY: int
    UNIT: str


class Marketing_Expenses(BaseModel):
    ID: Optional[str]
    ROW_ID: int
    SALES_ORGANIZATION: str
    SIM_ROUND: str
    SIM_STEP: int
    SIM_DATE: str
    SIM_CALENDAR_DATE: str
    SIM_PERIOD: int
    SIM_ELAPSED_STEPS: int
    MATERIAL_NUMBER: str
    MATERIAL_DESCRIPTION: str
    AREA: str
    AMOUNT: float
    CURRENCY: str


class NPS_Surveys(BaseModel):
    ID: Optional[str]
    ROW_ID: int
    SIM_ROUND: str
    SIM_STEP: int
    SIM_DATE: str
    SIM_CALENDAR_DATE: str
    SIM_PERIOD: int
    SIM_ELAPSED_STEPS: int
    PLANT: str
    TYPE: str
    MATERIAL_NUMBER: str
    MATERIAL_DESCRIPTION: str
    MATERIAL_TYPE: str
    MATERIAL_CODE: str
    MATERIAL_SIZE: str
    MATERIAL_LABEL: str
    CUSTOMER_NUMBER: str
    COUNTRY: str
    CITY: str
    POSTAL_CODE: str
    REGION: str
    AREA: str
    DISTRIBUTION_CHANNEL: str
    SCORE_0: int
    SCORE_1: int
    SCORE_2: int
    SCORE_3: int
    SCORE_4: int
    SCORE_5: int
    SCORE_6: int
    SCORE_7: int
    SCORE_8: int
    SCORE_9: int
    SCORE_10: int


class Pricing_Conditions(BaseModel):
    ID: Optional[str]
    ROW_ID: int
    SALES_ORGANIZATION: str
    SIM_ROUND: str
    SIM_STEP: int
    SIM_DATE: str
    SIM_CALENDAR_DATE: str
    SIM_PERIOD: int
    SIM_ELAPSED_STEPS: int
    MATERIAL_NUMBER: str
    MATERIAL_DESCRIPTION: str
    DISTRIBUTION_CHANNEL: str
    DC_NAME: str
    PRICE: float
    CURRENCY: str


class Production(BaseModel):
    ID: Optional[str]
    ROW_ID: int
    COMPANY_CODE: str
    SIM_ROUND: str
    SIM_STEP: int
    SIM_DATE: str
    SIM_CALENDAR_DATE: str
    SIM_PERIOD: int
    SIM_ELAPSED_STEPS: int
    MATERIAL_NUMBER: str
    MATERIAL_DESCRIPTION: str
    MATERIAL_SIZE: str
    MATERIAL_LABEL: str
    MATERIAL_CODE: str
    YIELD: int
    UNIT: str


class Production_Orders(BaseModel):
    ID: Optional[str]
    ROW_ID: int
    COMPANY_CODE: str
    SIM_ROUND: str
    SIM_STEP: int
    SIM_DATE: str
    SIM_CALENDAR_DATE: str
    SIM_PERIOD: int
    SIM_ELAPSED_STEPS: int
    PRODUCTION_ORDER: str
    MATERIAL_NUMBER: str
    MATERIAL_DESCRIPTION: str
    BEGIN_ROUND: str
    BEGIN_STEP: int
    END_ROUND: str
    END_STEP: int
    TARGET_QUANTITY: int
    CONFIRMED_QUANTITY: int
    UNIT: str
    SETUP_TIME: int


class Purchase_Orders(BaseModel):
    ID: Optional[str]
    ROW_ID: int
    COMPANY_CODE: str
    SIM_ROUND: str
    SIM_STEP: int
    SIM_DATE: str
    SIM_CALENDAR_DATE: str
    SIM_PERIOD: int
    SIM_ELAPSED_STEPS: int
    PURCHASING_ORDER: str
    VENDOR: str
    MATERIAL_NUMBER: str
    MATERIAL_DESCRIPTION: str
    QUANTITY: float
    STATUS: str
    UNIT: str
    GOODS_RECEIPT_ROUND: str
    GOODS_RECEIPT_STEP: int
    GOODS_RECEIPT_DATE: str


class Sales(BaseModel):
    ID: Optional[str]
    ROW_ID: int
    SALES_ORGANIZATION: str
    SIM_ROUND: str
    SIM_STEP: int
    SIM_DATE: str
    SIM_CALENDAR_DATE: str
    SIM_PERIOD: int
    SIM_ELAPSED_STEPS: int
    SALES_ORDER_NUMBER: int
    LINE_ITEM: int
    STORAGE_LOCATION: str
    REGION: str
    AREA: str
    CITY: str
    COUNTRY: str
    POSTAL_CODE: str
    CUSTOMER_NUMBER: str
    DISTRIBUTION_CHANNEL: int
    MATERIAL_NUMBER: str
    MATERIAL_DESCRIPTION: str
    MATERIAL_TYPE: str
    MATERIAL_CODE: str
    MATERIAL_SIZE: str
    MATERIAL_LABEL: str
    QUANTITY: int
    QUANTITY_DELIVERED: int
    UNIT: str
    NET_PRICE: float
    NET_VALUE: float
    COST: float
    CURRENCY: str
    CONTRIBUTION_MARGIN: float
    CONTRIBUTION_MARGIN_PCT: float


class Suppliers_Prices(BaseModel):
    ID: Optional[str]
    ROW_ID: int
    PURCHASING_ORGANIZATION: str
    SIM_ROUND: str
    SIM_STEP: int
    SIM_DATE: str
    SIM_CALENDAR_DATE: str
    SIM_PERIOD: int
    SIM_ELAPSED_STEPS: int
    MATERIAL_NUMBER: str
    MATERIAL_DESCRIPTION: str
    MATERIAL_TYPE: str
    VENDOR_CODE: str
    VENDOR_NAME: str
    NET_PRICE: float
    CURRENCY: str


class Carbon_Emission(BaseModel):
    pass


class Current_Game_Rules(BaseModel):
    pass


class Stock_Transfers(BaseModel):
    pass
