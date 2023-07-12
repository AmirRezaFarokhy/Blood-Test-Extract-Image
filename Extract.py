import pandas as pd
import numpy as np
import pytesseract
from pytesseract import Output
from PIL import Image
import cv2 
import imutils
import re
import matplotlib.pyplot as plt


class PreprocessingTextFromImage:

	def __init__(self, image_path, chunk_w, chunk_h):
		self.check_key_value = ["test", "testname", "result"]
		self.img = cv2.imread(image_path)
		self.chunk_w = chunk_w
		self.chunk_h = chunk_h
		self.slice_w = self.img.shape[0] // chunk_w
		self.slice_h = self.img.shape[1] // chunk_h
		if self.img.shape[0]<1280 or self.img.shape[1]<1000:
			increas_value_vote = 1400 - max(self.img.shape)
			self.img = imutils.resize(self.img, 
								width=self.img.shape[0]+increas_value_vote, 
								height=self.img.shape[1]+increas_value_vote)
			

	def CountingTestText(self):
		count = 0
		for wigth in range(0, self.img.shape[0], self.slice_w):
			slice_img = self.img[wigth:wigth+self.slice_w, 0:self.slice_h]
			slice_text = pytesseract.image_to_string(slice_img).split('\n')
			for text in slice_text:
				text = text.strip().split(' ')[0]
				text = re.sub(r'[^a-zA-Z]+', '', text)
				if text.lower() in self.check_key_value[:-1]:
					count += 1
		return count


	def HighestResolution(self, img, epslilon_vote):
		img = imutils.resize(self.img, 
								width=img.shape[0]+epslilon_vote, 
								height=img.shape[1]+epslilon_vote)
		return img


	def ShiftingImage(self, image):
		if self.resolution:
			image = self.HighestResolution(image, 5)

		if self.CountingTestText()>1:
			slice_data = pytesseract.image_to_data(image, 
												output_type=Output.DICT)
			for i in range(len(slice_data['level'])):
				epsilon_decay = 0
				if slice_data['text'][i].lower() in self.check_key_value:
					(X, y) = (slice_data['top'][i], 
							slice_data['left'][i])
					if min(X, y)<=epsilon_decay:
						epsilon_decay = min(X, y)
						X, y = X-epsilon_decay, y-epsilon_decay
						if slice_data['text'][i].lower()=='result':
							print(X, y)
						image = image[X:, y:]
					else:
						X, y = X-epsilon_decay, y-epsilon_decay
						if slice_data['text'][i].lower()=='result':
							print(X, y)
						image = image[X:, y:]

		else:
			for wigth in range(0, self.img.shape[0], self.slice_w):
				slice_img = self.img[wigth:wigth+self.slice_w, 0:self.slice_h]
				slice_text = pytesseract.image_to_string(slice_img).split('\n')
				for text in slice_text:
					text = text.strip().split(' ')[0]
					text = re.sub(r'[^a-zA-Z]+', '', text)
					if text.lower() in self.check_key_value[:-1]:
						image = self.img[wigth:, :]

		return image
		

	def OneTestText(self, resolution=False):

		def Checking(list_words, information):
			for word in list_words[:-4]:
				if len(word.split(' '))>=3:
					word = word.split(' ')
					check_word_test = re.sub(r'[^a-zA-Z]+', '', word[0])
					check_word_res = re.sub(r'[^a-zA-Z]+', '', word[1])
					if check_word_test not in self.check_key_value and word[0] not in information["Test"]:
						informations['Test'].append([word[0], word[1]])
						if check_word_res not in self.check_key_value:
							informations['Result'].append([word[2], word[3]])
			return information

		self.resolution = resolution
		filter_image = self.ShiftingImage(self.img)
		informations = {'Test':[], "Result":[]}
		for wigth in range(0, filter_image.shape[0], self.slice_w):
			slice_img_1 = filter_image[wigth:wigth+self.slice_w, :] 
			filter_img_1 = pytesseract.image_to_string(slice_img_1).split('\n')
			informations = Checking(filter_img_1, informations)

			slice_img_2 = filter_image[wigth:, :]
			filter_img_2 = pytesseract.image_to_string(slice_img_2).split('\n')
			informations = Checking(filter_img_2, informations)

			show_boxes = self.ShowBoxesDetected(slice_img_1)
			cv2.imshow("image boxes", show_boxes)
			cv2.waitKey(0)
			
		return informations


	def SeveralTestText(self, resolution=False):
		self.resolution = resolution
		index_slice = 0
		informations = []
		slice_w = self.img.shape[0] // self.chunk_w
		slice_h = self.img.shape[1] // self.chunk_h
		noises = 50
		try:
			for wigth in range(0, self.img.shape[0], slice_w):
				slice_img = self.img[wigth:wigth+slice_w, 0:slice_h]
				slice_text = pytesseract.image_to_string(slice_img).split('\n')
				for text in slice_text:
					text = text.strip().split(' ')[0]
					text = re.sub(r'[^a-zA-Z]+', '', text)
					image_get = []
					height = 0
					if text.lower() in self.check_key_value:
						if wigth!=0:
							for i in range(self.chunk_h-1):
								if height!=0:
									filter_image_data = self.img[wigth:wigth+slice_w, 
															height-noises:slice_h+height]
									filter_image_data = self.ShiftingImage(filter_image_data)
									
									height += slice_h 
								else:
									filter_image_data = self.img[wigth:wigth+slice_w, 
															height:slice_h+noises]
									filter_image_data = self.ShiftingImage(filter_image_data)
									height += slice_h 

								if filter_image_data.shape[1]>50:
									image_get.append(filter_image_data)
									index_slice += 1
									
							informations.append(image_get)

						else:
							for i in range(self.chunk_h-1):
								if height!=0:
									filter_image_data = self.img[wigth:wigth+slice_w, 
															height-noises:slice_h+height]
									filter_image_data = self.ShiftingImage(filter_image_data)
									height += slice_h 
								else:
									filter_image_data = self.img[wigth:wigth+slice_w, 
															height:slice_h+noises]
									filter_image_data = self.ShiftingImage(filter_image_data)
									height += slice_h 

								if filter_image_data.shape[1]>100:
									image_get.append(filter_image_data)
									index_slice += 1

							informations.append(image_get)
			return informations

		except Exception as error:
			print(f"We Can't do this becaus {error}")


	def ExtractingFeaturesSeveralTest(self, information_image):
		for image_match in information_image:
			for image in image_match:
				try:
					text = pytesseract.image_to_string(image)
					text_edited = re.sub(r'[^a-zA-Z]+', ' ', text).split(' ')
					for text_add in text_edited:
						if text_add.lower() in self.check_key_value:
							text = text.strip().split('\n')
							text = [t for t in text if t!='']
							text = [t for t in text if t!=' ']
							print(text)
				except Exception as error:
					print(f"We Can't do this becaus {error}")


	def ShowBoxesDetected(self, image):
		d = pytesseract.image_to_data(image, 
									  output_type=Output.DICT)
		n_boxes = len(d['level'])
		for i in range(n_boxes):
			if(d['text'][i] != ""):
				(x, y, w, h) = (d['left'][i], 
		    					d['top'][i], 
								d['width'][i], 
								d['height'][i])
				cv2.rectangle(image, 
		  					  (x, y), 
							  (x+w, y+h), 
		  					  (0,255,0), 2)

		image = cv2.resize(image, (720, 720))
		cv2.imshow('show boxes', image)
		cv2.waitKey(0)


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







