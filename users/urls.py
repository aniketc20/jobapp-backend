from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register),
    path('api-token-auth/', views.CustomAuthToken.as_view()),
    path('createJob/', views.createJob),
    path('apply/', views.apply),
    path('get-applications/', views.applications),
    path('update-applications/', views.update_application),
    path('jobs/', views.getJobs),
]