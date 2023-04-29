import requests 
import pandas as pd
import numpy as np

urls_normal_range = "https://www.msdmanuals.com/professional/resources/normal-laboratory-values/blood-tests-normal-values"

get_normal_range = requests.get(urls_normal_range)
df = pd.read_html(get_normal_range.text)[0]

sym_df = pd.read_csv("symbols.csv")

def UpdateSymbols():
    closing_len = len(sym_df) - 1
    for i in range(len(df)):
        sym_df["Actual_name"].iloc[i] = sym_df["Actual_name"].iloc[i].lower()
        if i==closing_len:
            break

    closing = len(df) - 1
    for i in range(len(df)):
        df["Test"].iloc[i] = df["Test"].iloc[i].split("(")[0].strip().lower()
        if i==closing:
            break

    sym_df["Specimen"] = np.NaN
    sym_df["Conventional Units"] = np.NaN
    sym_df["SI Units"] = np.NaN
    for i, sym_name in enumerate(sym_df["Actual_name"]):
        for j, test_name in enumerate(df["Test"]):
            if sym_name==test_name:
                sym_df["Specimen"].iloc[i] = df["Specimen"].iloc[j]
                sym_df["Conventional Units"].iloc[i] = df["Conventional Units"].iloc[j]
                sym_df["SI Units"].iloc[i] = df["SI Units"].iloc[j]

    return sym_df

main_df = UpdateSymbols()
main_df.to_csv("Update_symbols_with_normal_range.csv")
