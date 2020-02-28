
# coding: utf-8


import pandas as pd
import numpy as np
import pymongo

import wget
import os

filename = "20200226-FULL-1_1.csv"
if os.path.exists(filename):
    os.remove(filename)

url = 'https://webgate.ec.europa.eu/europeaid/fsd/fsf/public/files/csvFullSanctionsList_1_1/content?token=n00378g1'
filename = wget.download(url)


df = pd.read_csv(filename, sep=";")


# Get rid of unused columns
df1 = df[['Entity_SubjectType_ClassificationCode', 'NameAlias_WholeName', 'NameAlias_FirstName', 'NameAlias_LastName']]

df1 = df1.replace(np.nan, '', regex=True)
df1.columns = ['is_person', 'name', 'firstname', 'lastname']
df1['aliases'] = df1['firstname']+" "+df1['lastname']
df1['aliases'] = np.where(df1['aliases']==" ", "", df1['aliases']);
df1['aliases'] = df1['aliases'].str.split(",");
df1['sanctioned'] = True;
df1['is_person'] = np.where(df1['is_person']=="person", True , False);
df1['list'] = 'european_sanctions_list';
df1.drop( df1[ df1['name'] == '' ].index , inplace=True)
df1 = df1[['is_person', 'name', 'aliases', 'sanctioned', 'list']]
df1


filename = "deduped_opensanctions_2511.csv"
if os.path.exists(filename):
    os.remove(filename)

url = 'https://raw.githubusercontent.com/alephdata/opensanctions/master/datascience/deduped_opensanctions_2511.csv'
filename = wget.download(url)


# In[87]:

# Load it in a Spark DataFrame
un = pd.read_csv(filename, sep=",")


# In[88]:

un1 = un[['schema', 'name', 'alias']]
un1 = un1.replace(np.nan, '', regex=True)
un1['sanctioned'] = True;
un1['is_person'] = np.where(un1['schema']=="person", True , False);
un1['list'] = 'open_sanctions_list';
un1['aliases'] = un1['alias'].str.split(",");
un1 = un1[['name', 'aliases', 'sanctioned', 'is_person', 'list']]
un1.drop( un1[ un1['name'] == '' ].index , inplace=True)
un1



myclient = pymongo.MongoClient("mongodb://mongo:27018/")
mydb = myclient["mongo-test"]
mycol = mydb["sanctioneds"]


mycol.delete_many({});

x = mycol.insert_many(un1.to_dict(orient='records'))
x
