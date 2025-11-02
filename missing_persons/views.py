from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import MissingPerson
from .serializers import MissingPersonSerializer


class MissingPersonViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MissingPersonSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['gender', 'last_seen_date']
    search_fields = ['name', 'last_seen_location']
    ordering_fields = ['upload_date', 'last_seen_date', 'name']
    ordering = ['-upload_date']
    
    def get_queryset(self):
        return MissingPerson.objects.filter(is_active=True).select_related('owner')
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        latest_person = self.get_queryset().first()
        if latest_person:
            serializer = self.get_serializer(latest_person)
            return Response(serializer.data)
        return Response({'detail': 'No active records found'}, status=404)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        queryset = self.get_queryset()
        total_count = queryset.count()
        stats = {
            'total_active': total_count,
            'by_gender': {
                'male': queryset.filter(gender='male').count(),
                'female': queryset.filter(gender='female').count(),
                'other': queryset.filter(gender='other').count(),
            },
            'last_updated': queryset.first().last_updated if total_count > 0 else None,
        }
        return Response(stats)