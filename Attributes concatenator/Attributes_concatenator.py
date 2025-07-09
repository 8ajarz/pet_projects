# Requirement: preinstalled pandas and openpyxl libraries

import pandas as pd


df = pd.read_excel('attrs.xlsx', sheet_name='Attributes')
colnames = df.columns.to_list()

product_attrs = {}

def row_attr_extractor(row_attrs: list) -> dict:
    product_name = row_attrs[0]
    attrs_dict = {}
    for indx, value in enumerate(colnames[1:], start=1):
        if pd.isna(row_attrs[indx]):
            continue
        else:
            attrs_dict[value] = attrs_dict.get(value, "") + str(row_attrs[indx])
    return product_name, attrs_dict


def product_attrs_extender(row_name_and_attrs: tuple) -> None:
    prod_name = row_name_and_attrs[0]
    attrs_dict = row_name_and_attrs[1]
    if prod_name not in product_attrs:
        product_attrs[prod_name] = {}
    for key, value in attrs_dict.items():
        if key not in product_attrs[prod_name]:
            product_attrs[prod_name][key] = ""
        if value not in product_attrs[prod_name][key]:
                product_attrs[prod_name][key] += f",{value}"
            

for index, row in df.iterrows():
    product_attrs_extender(row_attr_extractor(row.to_list()))

for dict_key, dict_val in product_attrs.items():
    for key, value in dict_val.items():
        dict_val[key] = value.lstrip(",")

rows = []
for ProductCod, attributes in product_attrs.items():
    first = True
    for attr, value in attributes.items():
        if first:
            rows.append([ProductCod, attr, value])
            first = False
        else:
            rows.append(['', attr, value])

df = pd.DataFrame(rows, columns=['ProductCod', 'Attribute', 'Value'])

df.to_excel('output.xlsx', index=False)