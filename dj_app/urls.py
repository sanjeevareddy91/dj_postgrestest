from django.urls import path
from .views import *

urlpatterns = [
    path('',display_data,name="display_data"),
    path('add_data',add_data,name="add_data"),
    path('edit_table',edit_table,name="edit_table")
]
