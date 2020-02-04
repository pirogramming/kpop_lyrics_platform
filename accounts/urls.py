from django.urls import path, include

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('change_pw/', views.change_pw, name='change_pw'),
    path('reset_pw/', views.reset_pw.as_view(), name='reset_pw'),
    path('reset_pw/done/', views.reset_pw_done.as_view(), name='reset_pw_done'),
    path('reset/<uidb64>/<token>', views.reset_pw_confirm.as_view(), name='reset_pw_confirm'),
    path('reset_pw/complete/', views.reset_pw_complete.as_view(), name='reset_pw_complete'),

]