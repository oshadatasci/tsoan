# loaddata.py

import pandas as pd
import csv

##############################################################
# NAICS LOOKUP
##############################################################
lookup = {11 : 'Agriculture, forestry, fishing and hunting',
          21 : 'Mining',
          22 : 'Utilities',
          23 : 'Construction',
          31 : 'Manufacturing',
          32 : 'Manufacturing',
          33 : 'Manufacturing',
          42 : 'Wholesale trade',
          44 : 'Retail trade',
          45 : 'Retail trade',
          48 : 'Transportation and warehousing',
          49 : 'Transportation and warehousing',
          51 : 'Information',
          52 : 'Finance and insurance',
          53 : 'Real estate and rental and leasing',
          54 : 'Professional, scientific, and technical services (scope changed in 2009)',
          55 : 'Management of companies and enterprises',
          56 : 'Administrative and support and waste management and remediation services',
          61 : 'Educational services',
          62 : 'Health care and social assistance',
          71 : 'Arts, entertainment, and recreation',
          72 : 'Accommodation and food services',
          81 : 'Other services, except public administration',
          92 : 'Public administration'
        }

##############################################################
# LOAD AND CLEAN THE EMPLOYMENT DATA
##############################################################
# First get data from County Business Patterns - See README
read_emp = pd.read_csv("cpbseries_v2.csv", low_memory=False)
view_emp = pd.DataFrame(read_emp, columns=['fipstate', 'fipscty', 'naics', 'emp', 'year'])
view_emp['year'] = view_emp['year'].astype(str)
view_emp['fipstate'] = view_emp['fipstate'].astype(str)
view_emp['fipscty'] = view_emp['fipscty'].astype(str)
view_emp['naics'] = view_emp['naics'].astype(str)
view_emp['naics'] = view_emp['naics'].str.replace('-','')
view_emp['naics'] = view_emp['naics'].str.replace('11','Agriculture, forestry, fishing and hunting')
view_emp['naics'] = view_emp['naics'].str.replace('21','Mining')
view_emp['naics'] = view_emp['naics'].str.replace('22','Utilities')
view_emp['naics'] = view_emp['naics'].str.replace('23','Construction')
view_emp['naics'] = view_emp['naics'].str.replace('31','Manufacturing')
view_emp['naics'] = view_emp['naics'].str.replace('32','Manufacturing')
view_emp['naics'] = view_emp['naics'].str.replace('33','Manufacturing')
view_emp['naics'] = view_emp['naics'].str.replace('42','Wholesale trade')
view_emp['naics'] = view_emp['naics'].str.replace('44','Retail trade')
view_emp['naics'] = view_emp['naics'].str.replace('45','Retail trade')
view_emp['naics'] = view_emp['naics'].str.replace('48','Transportation and warehousing')
view_emp['naics'] = view_emp['naics'].str.replace('49','Transportation and warehousing')
view_emp['naics'] = view_emp['naics'].str.replace('51','Information')
view_emp['naics'] = view_emp['naics'].str.replace('52','Finance and insurance')
view_emp['naics'] = view_emp['naics'].str.replace('53','Real estate and rental and leasing')
view_emp['naics'] = view_emp['naics'].str.replace('54','Professional, scientific, and technical services (scope changed in 2009)')
view_emp['naics'] = view_emp['naics'].str.replace('55','Management of companies and enterprises')
view_emp['naics'] = view_emp['naics'].str.replace('56','Administrative and support and waste management and remediation services')
view_emp['naics'] = view_emp['naics'].str.replace('61','Educational services')
view_emp['naics'] = view_emp['naics'].str.replace('62','Health care and social assistance')
view_emp['naics'] = view_emp['naics'].str.replace('71','Arts, entertainment, and recreation')
view_emp['naics'] = view_emp['naics'].str.replace('72','Accommodation and food services')
view_emp['naics'] = view_emp['naics'].str.replace('81','Other services, except public administration')
view_emp['naics'] = view_emp['naics'].str.replace('92','Public administration')

view_emp.to_csv("employment_data.csv")



##############################################################
# LOAD AND CLEAN THE INJURY ILLNESS RATES DATA
##############################################################
#First download CSV from BLS - see the README
read_rates = pd.read_csv("ii_data_select_ind_all_numbs.csv", low_memory=False) 
view_rates = pd.DataFrame(read_rates, columns=['area_name','case_type_code','data_type_code','industry_name','year','value'])
view_rates.columns = ['area_name','case_type_code','data_type_code','naics','year','value']
view_rates.to_csv("rate_data.csv")
