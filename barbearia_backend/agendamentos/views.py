from rest_framework import generics
from .models import Servico, HorarioDisponivel, Agendamento
from .serializers import ServicoSerializer, HorarioDisponivelSerializer, AgendamentoSerializer

class ServicoListCreateView(generics.ListCreateAPIView):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer

class HorarioDisponivelListCreateView(generics.ListCreateAPIView):
    queryset = HorarioDisponivel.objects.all()
    serializer_class = HorarioDisponivelSerializer

class AgendamentoListCreateView(generics.ListCreateAPIView):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
