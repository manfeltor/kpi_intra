from django.urls import path
from .views import *

urlpatterns = [
    path('', render_main, name="entregasmain"),
]