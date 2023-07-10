import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import os 

from Extract import PreprocessingTextFromImage

img_path = 'img_test/img_2.jpg'
CHUNK_W = 4
CHUNK_H = 4

App = PreprocessingTextFromImage(img_path, CHUNK_W, CHUNK_H)

if App.CountingTestText()==1 and App.CountingTestText()>0:
    information_image = App.OneTestText()
else:
    information_image = App.SeveralTestText()

App.ShuftingImage(information_image[3][0])
