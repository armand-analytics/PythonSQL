import datetime
import pandas as pd

def extractMarket(cell):
    import re
    results = re.findall(r'SELECT|SBU_USC|MIDSIZE',cell)
    if results==[]:
        return 'OTHER'
    elif results[0]=='SBU_USC':
        return 'SMALL'
    else:
        return results[0]

def calculateFiscalQuarter(date):

    #Determine FY
    if date.month>=8:
        year=date.year+1
    else:
        year=date.year

    #Determine Quarter
    if date.month in [8,9,10]:
        quarter = 1
    elif date.month in [11,12,1]:
        quarter = 2
    elif date.month in [2,3,4]:
        quarter = 3
    elif date.month in [5,6,7]:
        quarter = 4

    return f"Q{quarter} FY{year}"

#AR RR Weekly Reporting without GEO ID.xlsx
#AR_Snapshot_Weekly(6).csv

master_sheet = input('Type the name of the master sheet including file format (i.e. example.csv): ')
snapshot_sheet = input('Type the name of the weekly snapshot sheet including file format (i.e. example.csv): ')

print('''

Loading Datasets... (This action might take several minutes)

''')

'''df2 = pd.read_excel(master_sheet)'''

df2 = pd.read_csv(master_sheet , index_col=0, low_memory=False)
remove_cols = [col for col in df2.columns if 'Unnamed' in col]
df2.drop(remove_cols, axis='columns', inplace=True)
df = pd.read_csv(snapshot_sheet)
df2.columns = df2.columns.str.strip()
'''df
df2'''
df['Market'] = df['Level 5'].apply(lambda x: extractMarket(x))

selection =input('''

Please select one option:

1) Use Current System Date for "Pulled Date" field 
2) Use Custom Date for "Pulled Date" field

Selection: ''')

if selection=='1':
    df['Date Pulled'] = pd.to_datetime(datetime.datetime.now().strftime("%x"))
elif selection=='2':
    selectedDate = input('Please enter custom date: YYYY-MM-DD')
    selectedDate = selectedDate.split('-')
    df['Date Pulled'] = pd.to_datetime(datetime.datetime(int(selectedDate[0]),int(selectedDate[1]),int(selectedDate[2])))
    #selectedDate = datetime.datetime(int(selectedDate[0]),int(selectedDate[1]),int(selectedDate[2]))
    #print(selectedDate)

df['Fiscal Quarter'] = df['Date Pulled'].apply(lambda x: calculateFiscalQuarter(x))

#if SFC Instance In Scope Flag ==n then pass  New Service Item Quantity 15 Months else pass  Total Service Item Quantity 15 Months 
sfc_adj_unit_nmr = []
for value in zip(df['SFC Instance In Scope Flag'],df['New Service Item Quantity 15 Months'],df['Total Service Item Quantity 15 Months']):
    #print(value)
    if value[0]=='N':
        sfc_adj_unit_nmr.append(value[1])
    else:
        sfc_adj_unit_nmr.append(value[2])
df['SFC Adj Unit Nmr'] = sfc_adj_unit_nmr


#SFC Adj $ Nmr = if SFC Instance In Scope Flag ==Y then pass  Total Service 15 Months else pass New Service 15 Months
sfc_adj_quant_nmr = []
for value in zip(df['SFC Instance In Scope Flag'],df['New Service 15 Months'],df['Total Service 15 Months']):
    #print(value)
    if value[0]=='Y':
        sfc_adj_quant_nmr.append(value[2])
    else:
        sfc_adj_quant_nmr.append(value[1])
df['SFC Adj $ Nmr'] = sfc_adj_quant_nmr

fw = int(input('''

Please type the fiscal week number: '''))

df['FW'] = fw
df['Fiscal Week'] = fw-1

df = df[['Shipped Month', 'Snapshot Month', 'Level 2', 'Level 3', 'Level 4','Level 5', 'Level 6', 'Best Site GU Name', 'SAVM ID', 'SAVM Name','Partner Name', 'Market', 'Product Family ID', 'Product ID', 'Warranty Category', 'Product Band', 'SFC Instance In Scope Flag', 'New Service 15 Months', 'Total Service 15 Months', 'New Service Item Quantity 15 Months','Total Service Item Quantity 15 Months', 'Date Pulled', 'SFC Adj Unit Nmr', 'SFC Adj $ Nmr', 'FW', 'Fiscal Week','Fiscal Quarter']]


final_df = pd.concat([df2,df])

selection =input('''

Select the final file format:

1) CSV format 
2) XLSX format (Creating this format is slower than creating a CSV)
3) Both (Slowest option of them all)

Selection: ''')

print('''

Creating Final Dataset(s)... (This action might take several minutes)

''')

if selection=='1':
    final_df.to_csv('FinalMasterSheetTest.csv', index=False)
elif selection=='2': 
    final_df.to_excel('FinalMasterSheetTest.xlsx', index=False)
elif selection=='3':
    final_df.to_excel('FinalMasterSheetTest.xlsx', index=False)
    final_df.to_csv('FinalMasterSheetTest.csv', index=False)

input('''

Finished creating datasets! Press any key to quit

''')