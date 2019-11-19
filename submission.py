import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

cols=['TRANSACTION_DATE','DOSAGE_UNIT','BUYER_COUNTY']
coldtypes={ 'DOSAGE_UNIT':np.float32 , 'BUYER_COUNTY':'category' }

change2year=lambda x : int(x[-4:])
nationdfall=pd.read_csv('../prescription/arcos_all_washpost.tsv' , sep='\t', 
                   usecols= cols,  dtype=coldtypes , verbose=True , engine='c',converters={ 'TRANSACTION_DATE':change2year } )

nationdfall['TRANSACTION_DATE']=nationdfall['TRANSACTION_DATE'].astype('category')

import pickle
pickle.dump(nationdfall, open( "nation.pkl", "wb" ) )\

import pickle
with open('nation.pkl','rb') as pkldfile :
    ndf=pickle.load(pkldfile)

pivot4years={}

for cat in ndf.TRANSACTION_DATE.cat.categories:
    temp=ndf[ndf.TRANSACTION_DATE == cat ]
    pivot4years[str(cat)]=temp.pivot_table(values='DOSAGE_UNIT',aggfunc=np.sum,index=temp.BUYER_COUNTY,columns=temp.TRANSACTION_DATE ,fill_value=0)


import pickle
pickle.dump(pivot4years, open( "pivot4years.pkl", "wb" ) )

deaths_dtypes={'Year':int,'County':str,'Notes':str,'County Code':int,'Year Code':int , 'Deaths':pd.Int32Dtype(),'Population':int,'Crude Rate':float }
deaths=pd.read_csv('MCDNewEngland20062012.tsv',sep='\t',index_col=['County','Year'],dtype=df2dtypes, na_values=['Suppressed','Unreliable'])

with open('pivot4years.pkl','rb') as pkldfile :
    pivotByYear=pickle.load(pkldfile)

import geopandas as gpd
smallcounties = gpd.read_file('cb_2018_us_county_500k/cb_2018_us_county_500k.shp')

state_dict={ '25':'Massachusetts', '09':'Connecticut' , '23':'Maine', '33':'New Hampshire', '50':'Vermont' ,'44':'Rhode Island'  }
necounties=smallcounties[smallcounties['STATEFP'].isin(state_dict.keys())].copy()

geoOPyear=dict()
for i in pivotByYear.keys():
    geoOPyear[i]=necounties.merge(pivotByYear[i],left_on='NAME',right_on='BUYER_COUNTY')
    geoOPyear[i].drop(columns=['ALAND','AWATER'])

deathspivot=deaths['Deaths'].unstack()
geoDeath=dict()
for i in geoOPyear.keys():
    temp=deathspivot[[int(i),'CName']]
    geoDeath[i]=geoOPyear[i].merge(temp,left_on='NAME',right_on='CName')
    geoDeath[i].drop(columns=['ALAND','AWATER']

