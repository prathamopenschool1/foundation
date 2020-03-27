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
    path('show_details/<int:pk>/', views.show_details_of_app, name='show_details'),
    path('master_list/<int:pk>/', views.MasterListByParent, name='master_list'),
    path('return_json_value/<int:pk>/', views.return_json_value, name='return_json_value'),
    path('downloads/', views.download_and_save, name='downloads'),
    path('update_checker/<int:pk>/', views.update_checker, name='update_checker'),
]
