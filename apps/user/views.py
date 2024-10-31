from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from .models import Admin, Customer
from .serializers import AdminSerializer, CustomerSerializer


# Create your views here.


class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all().order_by('-created_at')
    serializer_class = AdminSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ['first_name', 'last_name']

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ['first_name', 'last_name']

