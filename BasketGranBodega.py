import pandas as pd
import mlxtend
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
#Lecturas del excel o CSV
df = pd.read_excel('C:/Users/luis/Desktop/Ventas.xlsx')
df.head()

#Creacion de las canastas
basket = (df[df['SucursalPais'] ==7]
          .groupby(['RemisionFactura', 'CveProducto'])['Cantidad']
          .sum().unstack().reset_index().fillna(0)
          .set_index('RemisionFactura'))

basket1 = (df[df['SucursalPais'] ==9]
          .groupby(['RemisionFactura', 'CveProducto'])['Cantidad']
          .sum().unstack().reset_index().fillna(0)
          .set_index('RemisionFactura'))

basket2 = (df[df['SucursalPais'] ==18]
          .groupby(['RemisionFactura', 'CveProducto'])['Cantidad']
          .sum().unstack().reset_index().fillna(0)
          .set_index('RemisionFactura'))

basket3 = (df[df['SucursalPais'] ==53]
          .groupby(['RemisionFactura', 'CveProducto'])['Cantidad']
          .sum().unstack().reset_index().fillna(0)
          .set_index('RemisionFactura'))

basket4 = (df[df['SucursalPais'] ==41]
          .groupby(['RemisionFactura', 'CveProducto'])['Cantidad']
          .sum().unstack().reset_index().fillna(0)
          .set_index('RemisionFactura'))

basket5 = (df[df['SucursalPais'] ==59]
          .groupby(['RemisionFactura', 'CveProducto'])['Cantidad']
          .sum().unstack().reset_index().fillna(0)
          .set_index('RemisionFactura'))

basket6 = (df[df['SucursalPais'] ==60]
          .groupby(['RemisionFactura', 'CveProducto'])['Cantidad']
          .sum().unstack().reset_index().fillna(0)
          .set_index('RemisionFactura'))

basket7 = (df[df['SucursalPais'] ==28]
          .groupby(['RemisionFactura', 'CveProducto'])['Cantidad']
          .sum().unstack().reset_index().fillna(0)
          .set_index('RemisionFactura'))

basket8 = (df[df['SucursalPais'] ==65]
          .groupby(['RemisionFactura', 'CveProducto'])['Cantidad']
          .sum().unstack().reset_index().fillna(0)
          .set_index('RemisionFactura'))

basket9 = (df[df['SucursalPais'] ==75]
          .groupby(['RemisionFactura', 'CveProducto'])['Cantidad']
          .sum().unstack().reset_index().fillna(0)
          .set_index('RemisionFactura'))

basket10 = (df[df['SucursalPais'] ==75]
          .groupby(['RemisionFactura', 'CveProducto'])['Cantidad']
          .sum().unstack().reset_index().fillna(0)
          .set_index('RemisionFactura'))

#Conversion a 0 y 1 o preferible True/False
def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1
basket_sets = basket.applymap(encode_units)
basket_sets

#Obtención de la reglas de asociación
#min_support=mínimo de soporte para analizar
#Función a priori para extraer conjuntos de elementos frecuentes para la minería de reglas de asociación
frequent_itemsets = apriori(basket_sets, min_support=0.03, use_colnames=True)
frequent_itemsets

#Función que implementa FP-Growth para extraer conjuntos de elementos frecuentes para la minería de reglas de asociación
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpmax, fpgrowth
frequent_itemsets2 = fpgrowth(basket_sets, min_support=0.02, use_colnames=True)
frequent_itemsets2

#support/soporte indica que en el 0.085=8,5 % de las transacciones contienen ambas referencias
#confidence/ confianza de 0,26 indica que en el 60% de los casos que se compra el producto "1 antecedents" también aparece "2 consequents"

rules = association_rules(frequent_itemsets2, metric='lift', min_threshold=0.2, support_only=False)
rules.head()

rules[ (rules['lift'] >= 9) & (rules['confidence'] >= 0.3) ]
