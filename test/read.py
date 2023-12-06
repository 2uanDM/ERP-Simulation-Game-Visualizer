from copy import deepcopy
from bs4 import BeautifulSoup as bs
import polars as pl

lines = []


def get_line() -> dict:
    sample = {
        'ID': '',
        'ROW_ID': '',
        'SIM_ROUND': '',
        'SIM_STEP': '',
        'SIM_DATE': '',
        'SIM_PERIOD': '',
        'SIM_ELAPSED_STEPS': '',
        'STORAGE_LOCATION': '',
        'MATERIAL_NUMBER': '',
        'MATERIAL_DESCRIPTION': '',
        'MATERIAL_TYPE': '',
        'MATERIAL_CODE': '',
        'MATERIAL_SIZE': '',
        'MATERIAL_LABEL': '',
        'INVENTORY_OPENING_BALANCE': '',
        'UNIT': '',
    }

    return deepcopy(sample)


# Reading the file
with open('test/response.xml', 'r') as f:
    contents = f.read()

soup = bs(contents, 'xml')

bs_item = soup.find_all('content')

for item in bs_item:
    lines.append(get_line())

    lines[-1]['ID'] = item.find('d:ID').text
    lines[-1]['ROW_ID'] = item.find('d:ROW_ID').text
    lines[-1]['SIM_ROUND'] = item.find('d:SIM_ROUND').text
    lines[-1]['SIM_STEP'] = item.find('d:SIM_STEP').text
    lines[-1]['SIM_DATE'] = item.find('d:SIM_DATE').text
    lines[-1]['SIM_PERIOD'] = item.find('d:SIM_PERIOD').text
    lines[-1]['SIM_ELAPSED_STEPS'] = item.find('d:SIM_ELAPSED_STEPS').text
    lines[-1]['STORAGE_LOCATION'] = item.find('d:STORAGE_LOCATION').text
    lines[-1]['MATERIAL_NUMBER'] = item.find('d:MATERIAL_NUMBER').text
    lines[-1]['MATERIAL_DESCRIPTION'] = item.find('d:MATERIAL_DESCRIPTION').text
    lines[-1]['MATERIAL_TYPE'] = item.find('d:MATERIAL_TYPE').text
    lines[-1]['MATERIAL_CODE'] = item.find('d:MATERIAL_CODE').text
    lines[-1]['MATERIAL_SIZE'] = item.find('d:MATERIAL_SIZE').text
    lines[-1]['MATERIAL_LABEL'] = item.find('d:MATERIAL_LABEL').text
    lines[-1]['INVENTORY_OPENING_BALANCE'] = item.find('d:INVENTORY_OPENING_BALANCE').text
    lines[-1]['UNIT'] = item.find('d:UNIT').text

print(lines)

df = pl.DataFrame(lines)

# Writing the file
df.write_csv('response.csv')
