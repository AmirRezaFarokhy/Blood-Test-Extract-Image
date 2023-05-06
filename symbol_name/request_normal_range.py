import requests 
import pandas as pd
import numpy as np

urls_normal_range = "https://www.msdmanuals.com/professional/resources/normal-laboratory-values/blood-tests-normal-values"

def GetNormalValue():
    for conv, si in zip(df["Conventional Units"], df['SI Units']):
        
        try:
            x_max_conv = conv.split('<')
            x_max_si = si.split('<')
            if len(x_max_conv)==2 and len(x_max_si)==2:
                df["Conventional Units"].iloc[cnt] = float(x_max_conv[1][:3].strip())
                df['SI Units'].iloc[cnt] = float(x_max_si[1][:4].strip())
        except Exception as e:
            pass        
        
        try:
            x_min_conv = conv.split('>')
            x_min_si = si.split('>')
            if len(x_min_conv)==2 and len(x_min_si)==2:
                df["Conventional Units"].iloc[cnt] = float(x_min_conv[1][:3].strip())
                df['SI Units'].iloc[cnt] = float(x_min_si[1][:3].strip())
        except Exception as e:
            pass  

        try:
            x_center_max_conv = conv.split('–')[1].split(' ')[0]
            x_center_min_conv = conv.split('–')[0]
            x_center_max_si = si.split('–')[1].split(' ')[0]
            x_center_min_si = si.split('–')[0]
            if len(conv.split('–'))==2 and len(si.split('–'))==2:
                df["Conventional Units"].iloc[cnt] = str(x_center_min_conv)+'-'+str(x_center_max_conv)
                df['SI Units'].iloc[cnt] = str(x_center_min_si)+'-'+str(x_center_max_si)
        except Exception as e:
            pass
        
        cnt += 1
    
    return df

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

get_normal_range = requests.get(urls_normal_range)
df = pd.read_html(get_normal_range.text)[0]
sym_df = pd.read_csv("symbols.csv")

df = GetNormalValue()
main_df = UpdateSymbols()

main_df.to_csv("Update_symbols_with_normal_range.csv")
