# Requirement: preinstalled pandas and openpyxl libraries

import pandas as pd
import re

df = pd.read_excel('to_format.xlsx', sheet_name=0)

new_columns = pd.DataFrame({
    'Old': [None] * len(df),
    'New': [None] * len(df),
    'Standard': [None] * len(df)
})

df_updated = pd.concat([df.iloc[:, :3], new_columns, df.iloc[:, 3:]], axis=1)

def row_format(df_updated):
    for index, row in df_updated.iterrows():
        if "??? " in row["Назва"]:
            row["Назва"] = row["Назва"][4:]
        new = None
        old = re.findall(r'^(\d*) ', row["Назва"])
        if old:
            new = re.findall(r"\(\s*\D*(\d+)\D*\s*\)", row["Назва"][6:21])
            if new:
                row["Old"] = old[0]
                row["New"] = new[0]
                rest = row["Назва"].index(new[0]) + len(new[0]) + 1
                row["Назва"] = row["Назва"][rest:]
            else:
                row["Standard"] = old[0]
                row["Назва"] = row["Назва"][len(old[0]):]
        row["Назва"] = row["Назва"].strip().lstrip("- ")
        df_updated.loc[index] = row

    return df_updated

df_to_save = row_format(df_updated)

df_to_save.to_excel('output.xlsx', index=False)

if __name__ == "__main__":
    pass