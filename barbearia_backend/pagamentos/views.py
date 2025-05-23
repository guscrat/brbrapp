from rest_framework import generics
from .models import Pagamento
from .serializers import PagamentoSerializer

class PagamentoListCreateView(generics.ListCreateAPIView):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
