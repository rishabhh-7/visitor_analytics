from django.contrib import admin
from django.urls import path
from analytics_app import views

urlpatterns = [
    path('', views.home_page, name = 'home'),
    path('upload/', views.upload_video, name='upload_video'),
    path('graph/', views.show_graph, name='show_graphh'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
]