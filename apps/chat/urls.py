from django.urls import path
from .views import ConversationListView, MessageListView, SendMessageView

urlpatterns = [
    path('chat/conversations', ConversationListView.as_view(), name='chat_conversations'),
    path('chat/messages', MessageListView.as_view(), name='chat_messages'),
    path('chat/send-message', SendMessageView.as_view(), name='send_message'),
]
