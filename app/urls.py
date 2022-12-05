from django.urls import path, include
from . views import *


urlpatterns = [
    path('', index_page, name='app-index-page'),
    path('<slug:action>', index_page, name='app-index-page')
]
