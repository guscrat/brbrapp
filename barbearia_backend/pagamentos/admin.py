from django.contrib import admin
from .models import Pagamento

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('get_cliente', 'get_servico', 'metodo', 'valor', 'status', 'criado_em')
    list_filter = ('metodo', 'status', 'criado_em')
    search_fields = ('agendamento__cliente__username', 'agendamento__cliente__first_name')
    ordering = ('-criado_em',)
    readonly_fields = ('criado_em',)
    
    def get_cliente(self, obj):
        return obj.agendamento.cliente.get_full_name() or obj.agendamento.cliente.username
    get_cliente.short_description = 'Cliente'
    
    def get_servico(self, obj):
        return obj.agendamento.servico.nome
    get_servico.short_description = 'Serviço'