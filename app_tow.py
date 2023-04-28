import pandas as pd
import numpy as np
from PIL import Image
import pytesseract
import os

from Extract import FeatuesMatching


IMPORTANT_NAMES = ['Hematology', 'Differential']

DIFFERENTIAL_FILTER = ["Neutrophil", "Lymphocyte", 
					   "Monocyte", "Eosinophil"]

HEMATOLOGY_FILTER = ['WBC', 'RBC', 'Hemoglobin', 
					 'Hematocrit', 'MCV', 'MCH',
					 'MCHC', 'Platelets', 'HDL', 
					 'LDL', 'SGOT(AST)', 'SGOT',
					 'SGPT(ALT)', 'SGPT']

features = FeatuesMatching(HEMATOLOGY_FILTER, DIFFERENTIAL_FILTER)

test1 = pytesseract.image_to_string(Image.open('img_test/43.jpg')).split('\n')
df1 = features.HematologyFilter(test1, ["Test", "Result", "Risk", 
							   			"Uint", "Normal Value"])

test2 = pytesseract.image_to_string(Image.open('img_test/1234.jpg')).split('\n')
df2 = features.HematologyFilter(test2, ["Test", "Result", "Risk", 
							   		 	"Uint", "Normal Value"])


main_df = pd.concat([df1, df2])

for ids, data in enumerate(zip(main_df["Test"], main_df["Result"])):
	if np.isnan(data[1]):
		print(f"you must complete nan value that system can't complete {data[0]}...")
		inp = float(input(f"Pleat Completed this field from your blood test {data[0]}: "))
		main_df["Result"].iloc[ids] = inp 


if os.path.exists('result'):
	main_df.to_csv('result/extract_features.csv')
else:
	os.mkdir('result')
	main_df.to_csv('result/extract_features.csv')
