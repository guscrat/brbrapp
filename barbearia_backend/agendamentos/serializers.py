from rest_framework import serializers
from .models import Servico, HorarioDisponivel, Agendamento

class ServicoSerializer(serializers.ModelSerializer):
    preco_formatado = serializers.SerializerMethodField()
    
    class Meta:
        model = Servico
        fields = '__all__'
    
    def get_preco_formatado(self, obj):
        return f"R$ {obj.preco:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

class HorarioDisponivelSerializer(serializers.ModelSerializer):
    barbeiro_nome = serializers.SerializerMethodField()
    data_formatada = serializers.SerializerMethodField()
    hora_formatada = serializers.SerializerMethodField()
    disponivel = serializers.SerializerMethodField()
    
    class Meta:
        model = HorarioDisponivel
        fields = '__all__'
    
    def get_barbeiro_nome(self, obj):
        return obj.barbeiro.get_full_name() or obj.barbeiro.username
    
    def get_data_formatada(self, obj):
        return obj.data.strftime('%d/%m/%Y')
    
    def get_hora_formatada(self, obj):
        return obj.hora.strftime('%H:%M')
    
    def get_disponivel(self, obj):
        return not hasattr(obj, 'agendamento')

class AgendamentoSerializer(serializers.ModelSerializer):
    servico_nome = serializers.CharField(source='servico.nome', read_only=True)
    barbeiro_nome = serializers.CharField(source='horario.barbeiro.get_full_name', read_only=True)
    data_hora = serializers.SerializerMethodField()
    valor_servico = serializers.CharField(source='servico.preco', read_only=True)
    
    class Meta:
        model = Agendamento
        fields = '__all__'
        read_only_fields = ['confirmado', 'criado_em']
    
    def get_data_hora(self, obj):
        return f"{obj.horario.data.strftime('%d/%m/%Y')} às {obj.horario.hora.strftime('%H:%M')}"
    
    def validate_horario(self, value):
        # Verificar se o horário ainda está disponível
        if hasattr(value, 'agendamento'):
            raise serializers.ValidationError("Este horário já está ocupado.")
        return value

# pagamentos/serializers.py  
from rest_framework import serializers
from .models import Pagamento

class PagamentoSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='agendamento.cliente.get_full_name', read_only=True)
    servico_nome = serializers.CharField(source='agendamento.servico.nome', read_only=True)
    data_agendamento = serializers.SerializerMethodField()
    valor_formatado = serializers.SerializerMethodField()
    
    class Meta:
        model = Pagamento
        fields = '__all__'
        read_only_fields = ['criado_em']
    
    def get_data_agendamento(self, obj):
        return f"{obj.agendamento.horario.data.strftime('%d/%m/%Y')} às {obj.agendamento.horario.hora.strftime('%H:%M')}"
    
    def get_valor_formatado(self, obj):
        return f"R$ {obj.valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')