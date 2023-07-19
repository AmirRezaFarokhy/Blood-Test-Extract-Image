from celery import shared_task
from django.core.files import File 
from .models import ImageBloodTest

from ModelsApp.Extract import PreprocessingTextFromImage
import cv2
import pandas as pd
import os 


@shared_task
def UploadAndProcessingImage(IMG_PATH):
    
    print('Start processing image...')
    IMG_SAVE = '/home/amir/programming/git_repo/Blood-Test-Extract-Image/Main/static/detected'
    IMAEG_NAME = os.listdir(IMG_PATH)
    CHUNK_W = 4
    CHUNK_H = 4

    App = PreprocessingTextFromImage(IMG_PATH+IMAEG_NAME[0], CHUNK_W, CHUNK_H)
    if App.CountingTestText()==1 and App.CountingTestText()>0:
        print("Start With One...")
        info, images = App.OneTestText()
        img = App.ShowBoxesDetected(images[2])
        img = img[:-200]
        df = pd.DataFrame(columns=['Test', 'Result'])
        df['Test'] = info['Test']
        df['Result'] = info['Result']
        cv2.imwrite(f'{IMG_SAVE}/result_1.jpg', img) 
        print("Image Extract succesfully...") 
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
        
        cv2.imwrite(f'{IMG_SAVE}/result_1.jpg', append_vertically[1])
        print("Image Extract succesfully...")    
        

    # Removing Image To Avoiding extra files
    for image in IMAEG_NAME:
        file_path = os.path.join(IMG_PATH ,image)
        if os.path.exists(file_path):
            os.remove(file_path)
            print("Images removed succesfully...")
    
    return True 


    
