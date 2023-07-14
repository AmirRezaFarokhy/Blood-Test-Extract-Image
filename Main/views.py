from django.shortcuts import render
from .models import ImageBloodTest

from ModelsApp.Extract import PreprocessingTextFromImage
import cv2
import pandas as pd
import time
import os 


def HomePage(request):
    return render(request=request, 
                  template_name='index.html')


def AnalysisBloodTest(request):
    IMG_PATH = '/home/amir/programming/git_repo/Blood-Test-Extract-Image/media/images/'
    IMG_SAVE = '/home/amir/programming/git_repo/Blood-Test-Extract-Image/Main/static/detected'
    IMAEG_NAME = os.listdir(IMG_PATH)
    CHUNK_W = 4
    CHUNK_H = 4
    if request.method=='POST':
        image = request.FILES['upload']
        image_data = ImageBloodTest(information="Hi", image=image)   
        image_data.save()

        # put out model to do process data
        if len(IMAEG_NAME)!=0:
            App = PreprocessingTextFromImage(IMG_PATH+IMAEG_NAME[0], CHUNK_W, CHUNK_H)
            if App.CountingTestText()==1 and App.CountingTestText()>0:
                print("Start With One...")
                info, images = App.OneTestText()
                img = App.ShowBoxesDetected(images[2])
                df = pd.DataFrame(columns=['Test', 'Result'])
                df['Test'] = info['Test']
                df['Result'] = info['Result']
                cv2.imwrite(f'{IMG_SAVE}/result.jpg', img) 
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
                
                cv2.imwrite(f'{IMG_SAVE}/result.jpg', img)       
                

            # Removing Image To Avoiding extra files
            for image in IMAEG_NAME:
                file_path = os.path.join(IMG_PATH ,image)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print("Images removed succesfully...")

            # time.sleep(1)
            return render(request=request,
                        template_name='result.html',
                        context={'result':image_data})

        else:
            message = 'successfully uploaded and we try to fetch data from your image...'
            return render(request=request,
                        template_name='result.html',
                        context={'result':message})

