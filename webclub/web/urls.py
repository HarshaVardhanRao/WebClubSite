from django.urls import path
from . import views

urlpatterns = [
    path('',views.devspace,name='devspace'),
    # path('about', views.about, name='about'),
    # path('contact', views.contact, name='contact'),
    # path('leaderboard', views.leaderboard, name='leaderboard'),
    path('uploadBulk', views.upload_students, name='uploadBulk'),
    # path('complete-task/', views.complete_task, name='complete_task'),
    # path('select-mentor/', views.select_mentor, name='select_mentor'),
    path('deassign-mentors/', views.deassign_all_mentors, name='deassign_all_mentors'),
    path('assign-task/', views.assign_task, name='assign_task'),
]
