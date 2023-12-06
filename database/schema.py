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
    INVENTORY_OPENING_BALANCE: int
    UNIT: str
