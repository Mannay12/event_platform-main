from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, permissions

from .models import Event, EventAttender
from .serializers import EventSerializer, EventAttenderSerializer
from .permissions import IsEventPlannerOrReadOnly


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsEventPlannerOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['date', 'start_time']
    search_fields = ['name', 'type']
    ordering_fields = ['date', 'start_time']


class RegisterForEventView(viewsets.ModelViewSet):
    queryset = EventAttender.objects.all()
    serializer_class = EventAttenderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user  # Get the authenticated user
        event = serializer.validated_data.get('event')
        EventAttender.objects.create(user=user, event=event)