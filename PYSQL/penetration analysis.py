# %%
# this code is a example on how to cxonnect to hanna SAP and exract data as well as to transform it as you need using pandas
#  from IPython.core.display import display, HTML

# display(HTML('<style>.container {width: 100% !important}</style>'))
from os import getcwd
# import pyodbc
import pandas as pd
import numpy as np
# import jaydebeapi
# import pyhdb
from hdbcli import dbapi
import time
import os
import glob
import itertools
os.chdir(r"C:\Users\Penetration Analysis\Automated")
#Connection string 

conn = dbapi.connect(
    address="some-hana-address", 
    port=30015, 
    user="user",
    password="pass", 
    db='_SYS_BIC'
)
conn


# %%
#Calling sql query 
var-LCS =pd.read_sql('''
select distinct 
*
from  "_SYS_BIC".theaddressofthe.table"
where 
prod1 in ('L')
;''', conn)

Nonvar-LCS=pd.read_sql('''
    select 
    *
    FROM "_SYS_BIC".theOtheraddressofthe.table"/T"
    where
    reg in ('Ame')
    AND (YEAR BETWEEN 2015 AND 2020)
    AND FISCAL_Q in ('20243','20244','20251','20252', '20253','20254', '20261', '20262', '20263', '20264' ) -- next 2 yrs 
    AND STATUS='Latest'
    AND PRICE > 0
 group by
    1,2,3,4,5,6,7,8,9
    --limit 100
     ;''', conn)

NonLcs=NonLcs.drop_duplicates()
PENTABLE=pd.concat([LS, NonLcs])
PENTABLE=PENTABLE.fillna(0)
del LCS
del NonLcs
PENTABLE.to_csv('PENTABLE.csv', index=False)
PENTABLE

# %%
MPTBLre[' Name'].unique()

# %%
 X=pd.merge(PENTABLE, MPTBLre[' SALES GROUP ', 'group'], left_on='clave1', right_on='clave2', how='inner')

# %%

PENTABLE=PENTABLE.drop(columns=['Unnamed: 0'])

#calling the true mapping table 
truemapping=pd.read_csv(r"C:\Users\TrueMappingMethodebased.csv"
                        ,encoding='latin-1')


#new array called sub to automate the multiple merges in a for loop

sub=['SL3','SL4','SL5','SL6']
for x in sub:
            PENTABLE= pd.merge(PENTABLE,truemapping, how='left',
                     left_on=[x], right_on=['Key']
                   )

        
#replacing the automatic writed names for names with subindex from 3-6         
        
count = itertools.count(3)
new_cols = [f"CV_x" if col == "CV_y" else col for col in PENTABLE.columns]
PENTABLE.columns = new_cols

count = itertools.count(3)
new_cols = [f"CV_x{next(count)}" if col == "CV_x" else col for col in PENTABLE.columns]
PENTABLE.columns = new_cols

PENTABLE=PENTABLE.drop(['Key_x'], axis=1)
PENTABLE=PENTABLE.drop(['Key_y'], axis=1)


PENTABLE= pd.merge(PENTABLE,truemapping, how='left',
                     left_on=['GROUP'], right_on=['Key']
                   )
PENTABLE=PENTABLE.drop(['Key'], axis=1)




#the CSAV translation compLete***




PENTABLE['CV0'] = PENTABLE.apply(lambda row:
                                      row['CV_x3'] if pd.notnull(row['CV_x3']) else
                                      (row['CV_x4'] if pd.notnull(row['CV_x4']) else
                                      (row['CV_x5'] if pd.notnull(row['CV_x5']) else
                                      (row['CV_x6'] if pd.notnull(row['CV_x6']) else
                                       row['CV']
                                          )
                                          )
                                          ), axis=1)



ELMT=pd.read_csv(r"C:\Users\T.csv",encoding='latin-1')
ELMT.drop_duplicates(subset=['GROUP'], keep='first', inplace=True, ignore_index=True)


#new variable after merge
PENTABLE1= pd.merge(PENTABLE,ELMT, how='left',
                     left_on=['CV0'], right_on=['NAME']

                   )


#new filter by PKM

list=['P','K','M']
PENTABLE1=PENTABLE1[PENTABLE1.Tier.isin(list)]


#droping not deeded variables and tables


PENTABLE1.to_csv('PKM.csv')

fin = time.time()
print(fin-inicio)
PENTABLE1


