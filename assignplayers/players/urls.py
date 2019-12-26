from django.urls import path
from . import views

app_name = 'players'

urlpatterns = [
    # path('setup_wizard/', views.setup_wizard, name='setup_wizard'),
    path('programs/', views.program_call, name='programs'),
    path('states/', views.state_call, name='states'),
    path('crls/', views.crl_call, name='crls'),
    path('districts/', views.district_call, name='districts'),
    path('blocks/', views.block_call, name='blocks'),
    path('villages/', views.show_villages, name='villages'),
    path('post_villages/', views.post_villages, name='post_villages'),
    path('apps_list/', views.apps_list, name='apps_list'),
    path('app_available/', views.app_available, name='app_available'),
    path('user_login/', views.user_login, name='user_login'),
    path('downloads/', views.download_and_save, name='downloads'),
]
