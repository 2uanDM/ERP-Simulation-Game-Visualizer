import os
import sys
sys.path.append(os.getcwd())  # NOQA

from utils.db.schema import Market
from typing import List


def convert_data_to_schema(data: List[dict]) -> List[Market]:
    converted_data = [Market(**item) for item in data]
    return converted_data


data = [
    {'ID': '905', 'ROW_ID': '905', 'COMPANY_CODE': 'A2', 'SALES_ORGANIZATION': 'Market', 'SIM_ROUND': '03', 'SIM_PERIOD': '9', 'MATERIAL_DESCRIPTION': '500g Raisin Muesli',
        'DISTRIBUTION_CHANNEL': '14', 'AREA': 'West', 'QUANTITY': '3006', 'UNIT': 'ST', 'AVERAGE_PRICE': '5.38', 'NET_VALUE': '16172.28', 'CURRENCY': 'EUR'}
]
print(getattr(convert_data_to_schema(data)[0], 'ID'))
