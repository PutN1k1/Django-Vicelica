from django.urls import path
from . import views

urlpatterns = [
    path('', views.vicelica_game, name='vicelica_game'),
]
