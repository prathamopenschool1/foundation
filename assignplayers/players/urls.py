from django.urls import path
from . import views

app_name = 'players'

urlpatterns = [
    path('programs/', views.program_call, name='programs'),
    path('states/', views.state_call, name='states'),
    path('crls/', views.crl_call, name='crls'),
    path('districts/', views.district_call, name='districts'),
    path('blocks/', views.block_call, name='blocks'),
    path('villages/', views.show_villages, name='villages'),
    path('post_villages/', views.post_villages, name='post_villages'),
    path('user_login/', views.user_login, name='user_login'),
]
