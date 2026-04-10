from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from utils.responses import success_response, error_response

class ConversationListView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user).order_by('-updated_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response("Conversations retrieved successfully", data=serializer.data)

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # We can pass conversation_id as query param to get specific chat
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            return Message.objects.filter(
                conversation__id=conversation_id, 
                conversation__user=self.request.user
            ).order_by('created_at')
        
        # Or just return all messages for this user
        return Message.objects.filter(conversation__user=self.request.user).order_by('created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response("Messages retrieved successfully", data=serializer.data)

class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        content = request.data.get('content')
        conversation_id = request.data.get('conversation_id')

        if not content:
            return error_response("Message content is required")

        # Find or create conversation
        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id, user=request.user)
            except Conversation.DoesNotExist:
                return error_response("Conversation not found", status_code=404)
        else:
            conversation, created = Conversation.objects.get_or_create(user=request.user)

        # Update conversation timestamp
        conversation.save()

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )

        serializer = MessageSerializer(message)
        return success_response("Message sent successfully", data=serializer.data, status_code=201)
