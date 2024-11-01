from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .models import Review
from .serializers import ReviewSerializer


# Create your views here.


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['product']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='customer'):
            return queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
