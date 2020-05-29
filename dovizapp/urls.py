from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('homepage', views.index, name='homepage'),
    path('sarrafiye', views.show_enduser_sarrafiye, name='sarrafiye'),
    path('kurlar', views.show_enduser_kurlar, name='kurlar'),
    path('mobilsarrafiye', views.show_mobil_sarrafiye, name='mobilsarrafiye'),
    path('mobilkurlar', views.show_mobil_kurlar, name='mobilkurlar'),

    # buradan sonra login, logout vs
    path('login', LoginView.as_view(template_name='gunesadmin/gunes_first_auth.html',
                                    redirect_field_name='onepage.html')),
    # path('logout/<str:username>/', views.logout, name='logout'),
    path('dovizadmin', views.admin_page, name='dovizadmin'),
    # path('girisyap', views.username_password_form, name='girisyap')
]
