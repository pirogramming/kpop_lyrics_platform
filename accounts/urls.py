from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('change_pw/', views.change_pw, name='change_pw'),
    path('reset_pw/', views.reset_pw.as_view(), name='reset_pw'),
    path('reset_pw/done/', views.reset_pw_done.as_view(), name='reset_pw_done'),
    path('reset/<uidb64>/<token>/', views.reset_pw_confirm.as_view(), name='reset_pw_confirm'),
    path('reset_pw/complete/', views.reset_pw_complete.as_view(), name='reset_pw_complete'),
    path('change_info/', views.change_info, name='change_info'),
    path('check_comment/', views.check_comment, name='check_comment'),
    path('check_comment/del/<int:comment_pk>/', views.delete_comment, name='delete_comment'),
]
