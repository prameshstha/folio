
from django.urls import path

from .views import LaptopFeatures, PredictPrice

urlpatterns = [
    path('laptop-features/', LaptopFeatures.as_view(), name='movie'),
    path('predict-price/', PredictPrice.as_view(), name='movie'),
]