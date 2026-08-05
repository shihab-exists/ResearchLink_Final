from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list_view, name='chat_list'),
    path('chat/<int:contact_id>/', views.chat_list_view, name='chat_room'),
    path('send/<int:receiver_id>/', views.send_message_view, name='send_message'),
]
