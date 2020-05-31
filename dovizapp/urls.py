from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('homepage', views.index, name='homepage'),
    path('about', views.about_page, name='about'),
    path('sarrafiye', views.show_enduser_sarrafiye, name='sarrafiye'),
    path('kurlar', views.show_enduser_kurlar, name='kurlar'),
    path('mobilsarrafiye', views.show_mobil_sarrafiye, name='mobilsarrafiye'),
    path('mobilkurlar', views.show_mobil_kurlar, name='mobilkurlar'),

    # login, logout vs
    # path('login', views.login_form, name='login'),
    path('logout/<str:username>/', views.dovizadmin_logout, name='logout'),
    path('register', views.register_alternative, name='register'),
    path('login', views.login_form, name='login'),

    # bizim admin panelimiz
    path('dovizadmin', views.manage_data_view, name='dovizadmin')
    # bir de django admin paneli var o da bizim kullanıcıları, admini
    # filan etkiliyor

]
