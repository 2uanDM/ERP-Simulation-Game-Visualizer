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
        'BANK_CASH_ACCOUNT': '',
        'MATERIAL_NUMBER': '',
        'ACCOUNTS_RECEIVABLE': '',
        'BANK_LOAN': '',
        'ACCOUNTS_PAYABLE': '',
        'PROFIT': '',
        'SETUP_TIME_INVESTMENT': '',
        'DEBT_LOADING': '',
        'CREDIT_RATING': '',
        'COMPANY_RISK_RATE_PCT': '',
        'MARKET_RISK_RATE_PCT': '',
        'COMPANY_VALUATION': '',
        'CREDIT_RATING_UNADJUSTED': '',
        'COMPANY_RISK_RATE_UNADJUSTED': '',
        'COMPANY_VALUATION_UNADJUSTED': '',
        'CURRENCY': '',
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
    lines[-1]['BANK_CASH_ACCOUNT'] = item.find('d:BANK_CASH_ACCOUNT').text
    lines[-1]['ACCOUNTS_RECEIVABLE'] = item.find('d:ACCOUNTS_RECEIVABLE').text
    lines[-1]['BANK_LOAN'] = item.find('d:BANK_LOAN').text
    lines[-1]['ACCOUNTS_PAYABLE'] = item.find('d:ACCOUNTS_PAYABLE').text
    lines[-1]['PROFIT'] = item.find('d:PROFIT').text
    lines[-1]['SETUP_TIME_INVESTMENT'] = item.find('d:SETUP_TIME_INVESTMENT').text
    lines[-1]['DEBT_LOADING'] = item.find('d:DEBT_LOADING').text
    lines[-1]['CREDIT_RATING'] = item.find('d:CREDIT_RATING').text
    lines[-1]['COMPANY_RISK_RATE_PCT'] = item.find('d:COMPANY_RISK_RATE_PCT').text
    lines[-1]['MARKET_RISK_RATE_PCT'] = item.find('d:MARKET_RISK_RATE_PCT').text
    lines[-1]['COMPANY_VALUATION'] = item.find('d:COMPANY_VALUATION').text
    lines[-1]['CREDIT_RATING_UNADJUSTED'] = item.find('d:CREDIT_RATING_UNADJUSTED').text
    lines[-1]['COMPANY_RISK_RATE_UNADJUSTED'] = item.find('d:COMPANY_RISK_RATE_UNADJUSTED').text
    lines[-1]['COMPANY_VALUATION_UNADJUSTED'] = item.find('d:COMPANY_VALUATION_UNADJUSTED').text
    lines[-1]['CURRENCY'] = item.find('d:CURRENCY').text

print(lines)

# Sort the list by the key
lines.sort(key=lambda x: x['ROW_ID'])

df = pl.DataFrame(lines)

# Writing the file
df.write_csv('response_company_val.csv')
