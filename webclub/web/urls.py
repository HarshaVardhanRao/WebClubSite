from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('leaderboard', views.leaderboard, name='leaderboard'),
    path('uploadBulk', views.upload_students, name='uploadBulk')
]
