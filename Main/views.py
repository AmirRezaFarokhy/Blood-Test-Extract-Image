from django.shortcuts import render
from .models import ImageBloodTest
from ModelsApp import app_three


def HomePage(request):
    return render(request=request, 
                  template_name='index.html')


def AnalysisBloodTest(request):
    if request.method=='POST':
        image = request.FILES['upload']
        image_data = ImageBloodTest(information="Hi", image=image)   
        image_data.save()
        
        return render(request=request,
                      template_name='result.html',
                      context={'result':'successfully uploaded'})

