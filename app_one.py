import numpy as np 
import pandas as pd 
from PIL import Image
import pytesseract
import os

from Extract import FeaturesGetValue

STR_VALUE_DICT = {"Negetive":0, "Positive":1}

sym_df = pd.read_csv("symbol_name/symbols.csv")

features = FeaturesGetValue()

test1 = pytesseract.image_to_string(Image.open('img_test/43.jpg')).split('\n')
df1 = features.AllValuesGetting(sym_df['Symbols'].values ,test1)

test2 = pytesseract.image_to_string(Image.open('img_test/1234.jpg')).split('\n')
df2 = features.AllValuesGetting(sym_df['Symbols'].values ,test2)

main_df = pd.concat([df1, df2])

for ids, data in enumerate(zip(main_df["Symbols"], main_df["Values"])):
	if np.isnan(data[1]):
		print(f"you must complete nan value that system can't complete {data[0]}...")
		inp = float(input(f"Pleat Completed this field from your blood test {data[0]}: "))
		main_df["Values"].iloc[ids] = inp 

if os.path.exists('result'):
	main_df.to_csv('result/GetJustValues.csv')
else:
	os.mkdir('result')
	main_df.to_csv('result/GetJustValues.csv')

