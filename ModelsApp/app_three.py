import pandas as pd 
import matplotlib.pyplot as plt 
import pytesseract
import os 
import sys
import cv2

from ModelsApp.Extract import PreprocessingTextFromImage


if sys.platform[:3]=='win':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


IMG_PATH = '/home/amir/programming/git_repo/Blood-Test-Extract-Image/media/images/'
IMAEG_NAME = os.listdir(IMG_PATH)
CHUNK_W = 4
CHUNK_H = 4

if len(IMAEG_NAME)!=0:
    App = PreprocessingTextFromImage(IMG_PATH+IMAEG_NAME[0], CHUNK_W, CHUNK_H)

    if App.CountingTestText()==1 and App.CountingTestText()>0:
        print("Start With One...")
        info, images = App.OneTestText()
        img = App.ShowBoxesDetected(images[2])
        df = pd.DataFrame(columns=['Test', 'Result'])
        df['Test'] = info['Test']
        df['Result'] = info['Result']
        print(df)
        plt.imshow(img)
        plt.show()   
    else:
        print("Start With Several...")
        information_image = App.SeveralTestText()
        App.ExtractingFeaturesSeveralTest(information_image)
        append_vertically = []
        append_all = []
        for inf in information_image:
            image_one = App.ShowBoxesDetected(inf[0])
            image_tow = App.ShowBoxesDetected(inf[1])
            append_vertically.append(cv2.hconcat([image_one, image_tow]))
            if len(append_vertically)==len(information_image):
                for img in append_vertically:
                    append_all.append(cv2.vconcat([img[0], img[1]]))
        
        plt.imshow(append_vertically[1])
        plt.show()        
        

    # Removing Image To Avoiding extra files
    for image in IMAEG_NAME:
        file_path = os.path.join(IMG_PATH ,image)
        os.remove(file_path)
        print("Images removed succesfully...")




