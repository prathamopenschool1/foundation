from rest_framework import viewsets, permissions
from players.models import PlayersDatastore
from rest_framework.filters import SearchFilter, BaseFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
import django_filters.rest_framework
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import PlayersDatastoreSerializer


class PlayerDataStoreView(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    queryset = PlayersDatastore.objects.order_by('id')
    serializer_class = PlayersDatastoreSerializer
    filter_fields = ('filter_name', 'table_name')
    pagination_class = PageNumberPagination

