from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Agendamento
from .serializers import AgendamentoSerializer

class AgendamentoListCreateView(generics.ListCreateAPIView):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Agendamento.objects.filter(cliente=self.request.user)

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)
