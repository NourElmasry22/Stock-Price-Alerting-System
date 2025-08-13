from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('userinfo/', views.current_user, name='user_info'),
    path('userinfo/update/', views.current_user, name='user_update'),
     path('forgot_password/', views.forgot_password,name='forgot_password'), 
    path('reset_password/<str:token>', views.reset_password,name='reset_password'), 
    path('change_password/', views.change_password, name = 'change_password'),
    path('logout/', views.logout, name="logout" )
]
