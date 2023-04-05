from rest_framework import viewsets, filters
from .models import Poll
from .serializers import PollSerializer


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'choices__text']
    ordering = ['-expiry_date']
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100
