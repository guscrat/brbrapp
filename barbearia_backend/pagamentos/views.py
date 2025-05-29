from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Pagamento
from .serializers import PagamentoSerializer

class PagamentoListCreateView(generics.ListCreateAPIView):
    serializer_class = PagamentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Corrigido: filtra pagamentos pelos agendamentos do usuário logado
        return Pagamento.objects.filter(agendamento__cliente=self.request.user)

    def perform_create(self, serializer):
        # Validação: garantir que o agendamento pertence ao usuário logado
        agendamento = serializer.validated_data['agendamento']
        if agendamento.cliente != self.request.user:
            raise serializers.ValidationError("Você só pode criar pagamentos para seus próprios agendamentos.")
        
        # Definir valor automaticamente baseado no serviço
        if not serializer.validated_data.get('valor'):
            serializer.validated_data['valor'] = agendamento.servico.preco
            
        serializer.save()