import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import pytesseract
import os 
import sys
import cv2

from Extract import PreprocessingTextFromImage

if sys.platform[:3]=='win':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

IMG_PATH = 'img_test/img_3.jpg'
CHUNK_W = 4
CHUNK_H = 4

App = PreprocessingTextFromImage(IMG_PATH, CHUNK_W, CHUNK_H)

if App.CountingTestText()==1 and App.CountingTestText()>0:
    print("Start With One...")
    #information_image = App.OneTestText(resolution=False)
    info = App.OneTestText()
    df = pd.DataFrame(columns=['Test', 'Result'])
    # print(info['Test'], len(info['Test']))
    # print('#############################')
    # print(info['Result'], len(info['Result']))
    df['Test'] = info['Test']
    df['Result'] = info['Result']
    print(df)
else:
    print("Start With Several...")
    information_image = App.SeveralTestText()
    App.ExtractingFeaturesSeveralTest(information_image)
    # App.ShuftingImage(information_image[3][0])
    # App.ShowBoxesDetected(information_image[-1][0])



