from rest_framework import viewsets

from models import TableSymbol
from serializers import TableSymbolSerializer


class TableSymbolViewSet(viewsets.ModelViewSet):
    queryset = TableSymbol.objects.all()
    serializer_class = TableSymbolSerializer
