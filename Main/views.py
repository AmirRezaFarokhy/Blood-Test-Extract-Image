from django.shortcuts import render
from django.http import HttpResponse
from .models import ImageBloodTest

def HomePage(request):
    if request.method=='POST':
        image = request.FILES['upload']
        data = ImageBloodTest(information="Hi" ,image=image)   
        data.save()
        return render(request=request,
                        template_name='index.html',
                        context={'result':'successfully uploaded'})


    return render(request=request, 
                    template_name='index.html', 
                    )

