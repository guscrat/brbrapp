from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Agendamento, Servico, HorarioDisponivel
from .serializers import AgendamentoSerializer, ServicoSerializer, HorarioDisponivelSerializer

class AgendamentoListCreateView(generics.ListCreateAPIView):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Agendamento.objects.filter(cliente=self.request.user)

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)

class ServicoListCreateView(generics.ListCreateAPIView):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
    permission_classes = [IsAuthenticated]

class HorarioDisponivelListCreateView(generics.ListCreateAPIView):
    queryset = HorarioDisponivel.objects.all()
    serializer_class = HorarioDisponivelSerializer
    permission_classes = [IsAuthenticated]