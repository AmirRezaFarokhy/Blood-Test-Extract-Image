import pandas as pd
import numpy as np
import pytesseract
from PIL import Image


class PreprocessingTextFromImage:
	pass



class FeatuesMatching:

	def __init__(self, hematology, differential):
		self.hematology = hematology
		self.differential = differential

	def HematologyFilter(self, blood_test, col_name):
		self.df = pd.DataFrame(columns=col_name)
		lst_test = []
		lst_res = []
		lst_risk = []
		lst_unit = []
		lst_nor = []
		for fil in self.hematology:
			for t in blood_test:
				filter_func = t.split(' ')[0].strip()
				if filter_func==fil and len(t.split(' '))>=4:
					values = t.split(' ')
					try:
						if len(values)==4:
							lst_test.append(values[0])
							lst_risk.append(np.NaN)
							lst_unit.append(values[2])
							lst_nor.append(values[3])
							lst_res.append(float(values[1]))


						elif len(values)==5 and values[2] in ['High','H','Low','L']:
							lst_test.append(values[0])
							lst_risk.append(values[2])
							lst_unit.append(values[3])
							lst_nor.append(values[4])
							lst_res.append(float(values[1]))

						else:
							lst_test.append(values[0])
							lst_risk.append(np.NaN)
							lst_unit.append(values[2])
							lst_nor.append(values[3])
							lst_res.append(float(values[1]))
							
					except Exception as e:
						try:
							lst_res.append(np.NaN)
							
						except Exception as e:
							print(f"We find Problems in {e}")
				 
		self.df['Test'] = lst_test
		self.df["Result"] = lst_res
		self.df["Risk"] = lst_risk
		self.df['Uint'] = lst_unit
		self.df['Normal Value'] = lst_nor
		return self.df


	def DifferentialFilter(self, blood_test, col_name):
		self.df = pd.DataFrame(columns=col_name)
		name = []
		accuracy = []
		for fil in self.differential:
			for t in blood_test:
				filter_func = t.split(' ')[0].strip()
				if filter_func==fil:
					values = t.split(" ")
					try:
						name.append(values[0])
						accuracy.append(float(values[1]))
					except Exception as e:
						print(f"We Find error {e}")

		self.df["Name"] = name 
		self.df["Accuracy"] = accuracy
		return self.df



class FeaturesGetValue:

	def AllValuesGetting(self, filtering_name, blood_test):
		self.df = pd.DataFrame(columns=["Symbols", "Values"])
		name = []
		value = []
		for fil in filtering_name:
			for t in blood_test:
				filter_func = t.split(' ')[0].strip()
				if filter_func==fil:
					feature = t.split(" ")
					try:
						name.append(feature[0])
						value.append(float(feature[1]))
					except Exception as e:
						try:
							value.append(np.NaN)
						except Exception as e:
							print(f"We Can't load image in this feild pleas do that manualy.")

		self.df["Symbols"] = name
		self.df["Values"] = value
		return self.df







