from django.contrib import admin
from django.urls import path, include
from .views import Chatting
chat=Chatting()

urlpatterns = [
    path('add', chat.add),
    path('sendmsg', chat.sendmsg),
    path('', chat.home, name='home')
]