from django.shortcuts import render
from .models import ImageBloodTest

from Main.task import UploadAndProcessingImage
import os 


def HomePage(request):
    return render(request=request, 
                  template_name='index.html')


def AnalysisBloodTest(request):
    IMG_PATH = '/home/amir/programming/git_repo/Blood-Test-Extract-Image/media/images/'
    IMAEG_NAME = os.listdir(IMG_PATH)
    if request.method=='POST':
        image = request.FILES['upload']
        image_data = ImageBloodTest(information="Hi", image=image)   
        image_data.save()

        # Using Celery to doing image processing 
        if len(IMAEG_NAME)!=0:
            UploadAndProcessingImage(IMG_PATH)
            return render(request=request,
                        template_name='result.html',
                        context={'result':image_data})
        else:
            message = 'successfully uploaded and we try to fetch data from your image...'
            return render(request=request,
                        template_name='result.html',
                        context={'result':message})
        
        

