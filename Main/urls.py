from django.urls import path
from .views import HomePage, AnalysisBloodTest

urlpatterns = [
    path('', HomePage, name='home'),
    path('analys/', AnalysisBloodTest, name='analys'),
]

