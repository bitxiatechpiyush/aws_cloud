from django.urls import path
from .views import add_item

urlpatterns = [
    path('add-item/', add_item, name='add-item'),
]
