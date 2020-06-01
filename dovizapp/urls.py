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
    path('logout', views.dovizadmin_logout, name='logout'),
    path('register', views.register_alternative, name='register'),
    path('dovizlogin', views.doviz_admin_login, name='dovizlogin'),
    # aynisi
    path('login', views.doviz_admin_login, name='login'),

    # bizim admin panelimiz
    path('dovizadmin', views.manage_data_view, name='dovizadmin')
    # bir de django admin paneli var o da bizim kullanıcıları, admini
    # filan etkiliyor

]
