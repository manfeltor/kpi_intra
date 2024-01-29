from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',login1, name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name="logout")
]
