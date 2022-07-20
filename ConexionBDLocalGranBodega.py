import pyodbc
import pandas as pd
import warnings
import mlxtend
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-RGNKM9E;DATABASE=Muestra_GB;Trusted_Connection=yes;')
query ="select Remision as RemisionFactura, CveProducto, Cantidad,Fecha,Precio,ClaveCliente,Sucursal as SucursalPais from Ventas"

with warnings.catch_warnings():
     warnings.simplefilter('ignore', UserWarning)
     df = pd.read_sql(query, conn)
    
conn.close()  # Se cerró la conexión a la BD.
#df.head()
df.loc[df['Cantidad']  < 1, 'Cantidad'] = 1

basket = (df[df['SucursalPais'] ==7]
          .groupby(['RemisionFactura', 'CveProducto'])['Cantidad']
          .sum().unstack().reset_index().fillna(0)
          .set_index('RemisionFactura'))
def encode_units(x):
    if x <= 0:
        return False
    if x >= 1:
        return True
basket_sets = basket.applymap(encode_units)
basket_sets
frequent_itemsets = apriori(basket_sets, min_support=0.03, use_colnames=True)

rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.01)
rules["antecedents"] = rules["antecedents"].apply(lambda x: ', '.join(list(x))).astype("unicode")
rules["consequents"] = rules["consequents"].apply(lambda x: ', '.join(list(x))).astype("unicode")

rules.rename(columns={
    'antecedent support':'antecedentsupport',
    'consequent support':'consequentsupport',
    'antecedents':'antecedent_SKU',
    'consequents':'consequent_SKU'
},inplace=True)

from sqlalchemy.engine import URL
from sqlalchemy import create_engine

connection_string = "DRIVER={SQL Server};SERVER=DESKTOP-RGNKM9E;DATABASE=Muestra_GB"
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

engine = create_engine(connection_url)
engine.connect() 
#engine = "mssql+pyodbc://DESKTOP-RGNKM9E/Muestra_GB?driver=ODBC Driver 17 for SQL Server?trusted_connection=yes"

rules.to_sql('Analitic', con=engine, index=False, if_exists='append')
