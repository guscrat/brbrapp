from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Pagamento
from .serializers import PagamentoSerializer

class PagamentoListView(generics.ListAPIView):
    serializer_class = PagamentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Pagamento.objects.filter(cliente=self.request.user)
