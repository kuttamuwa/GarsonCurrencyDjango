from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('homepage', views.index, name='homepage'),
    path('sarrafiye', views.show_enduser_sarrafiye, name='sarrafiye'),
    path('kurlar', views.show_enduser_kurlar, name='kurlar'),
    path('mobilsarrafiye', views.show_mobil_sarrafiye, name='mobilsarrafiye'),
    path('mobilkurlar', views.show_mobil_kurlar, name='mobilkurlar'),
]
