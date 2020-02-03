from django.urls import path, include

from accounts import views

urlpatterns = [
    path('', include('allauth.urls')),
    path('', include('django.contrib.auth.urls')),
    path('connection/', views.connection, name='connection'),
]