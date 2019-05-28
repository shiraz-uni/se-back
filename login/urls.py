from django.urls import path

from . import views

urlpatterns = [
    path('test', views.test, name='test'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('already_in', views.already_in, name='already_in'),
    path('week_data', views.week_data, name='week_data'),
    path('self_data', views.self_data, name='self_data'),
]