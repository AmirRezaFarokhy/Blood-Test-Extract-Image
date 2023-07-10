import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import os 
import cv2

from Extract import PreprocessingTextFromImage

IMG_PATH = 'img_test/img_3.jpg'
CHUNK_W = 4
CHUNK_H = 4

App = PreprocessingTextFromImage(IMG_PATH, CHUNK_W, CHUNK_H)

if App.CountingTestText()==1 and App.CountingTestText()>0:
    print("Start With One...")
    #information_image = App.OneTestText(resolution=False)
    App.OneTestText()
else:
    print("Start With Several...")
    information_image = App.SeveralTestText()
    App.ExtractingFeaturesSeveralTest(information_image)
    # App.ShuftingImage(information_image[3][0])
    # App.ShowBoxesDetected(information_image[-1][0])



