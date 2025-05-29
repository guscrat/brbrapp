from django.contrib import admin
from django.utils.html import format_html
from .models import Servico, HorarioDisponivel, Agendamento

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'duracao_minutos', 'preco_formatado')
    search_fields = ('nome',)
    ordering = ('nome',)
    
    def preco_formatado(self, obj):
        return f"R$ {obj.preco:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    preco_formatado.short_description = 'Preço'

@admin.register(HorarioDisponivel)
class HorarioDisponivelAdmin(admin.ModelAdmin):
    list_display = ('get_barbeiro_nome', 'data', 'hora', 'status_agendamento')
    list_filter = ('data', 'barbeiro')
    search_fields = ('barbeiro__username', 'barbeiro__first_name', 'barbeiro__last_name')
    ordering = ('data', 'hora')
    date_hierarchy = 'data'
    
    def get_barbeiro_nome(self, obj):
        return obj.barbeiro.get_full_name() or obj.barbeiro.username
    get_barbeiro_nome.short_description = 'Barbeiro'
    
    def status_agendamento(self, obj):
        try:
            agendamento = obj.agendamento
            if agendamento.confirmado:
                return format_html('<span style="color: green;">✅ Confirmado</span>')
            else:
                return format_html('<span style="color: orange;">⏳ Pendente</span>')
        except:
            return format_html('<span style="color: blue;">📅 Disponível</span>')
    status_agendamento.short_description = 'Status'
    
    # Filtra para mostrar apenas usuários que são barbeiros
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "barbeiro":
            kwargs["queryset"] = db_field.related_model.objects.filter(is_barbeiro=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('get_cliente_nome', 'servico', 'get_barbeiro', 'get_data_hora', 'status_confirmado', 'criado_em')
    list_filter = ('confirmado', 'criado_em', 'horario__data', 'servico')
    search_fields = ('cliente__username', 'cliente__first_name', 'cliente__last_name')
    ordering = ('-criado_em',)
    readonly_fields = ('criado_em',)
    date_hierarchy = 'criado_em'
    
    def get_cliente_nome(self, obj):
        return obj.cliente.get_full_name() or obj.cliente.username
    get_cliente_nome.short_description = 'Cliente'
    
    def get_barbeiro(self, obj):
        return obj.horario.barbeiro.get_full_name() or obj.horario.barbeiro.username
    get_barbeiro.short_description = 'Barbeiro'
    
    def get_data_hora(self, obj):
        return f"{obj.horario.data.strftime('%d/%m/%Y')} às {obj.horario.hora.strftime('%H:%M')}"
    get_data_hora.short_description = 'Data e Hora'
    
    def status_confirmado(self, obj):
        if obj.confirmado:
            return format_html('<span style="color: green; font-weight: bold;">✅ Confirmado</span>')
        else:
            return format_html('<span style="color: orange; font-weight: bold;">⏳ Pendente</span>')
    status_confirmado.short_description = 'Status'
    
    # Adiciona ações em massa
    actions = ['confirmar_agendamentos', 'cancelar_confirmacao']
    
    def confirmar_agendamentos(self, request, queryset):
        updated = queryset.update(confirmado=True)
        self.message_user(request, f'{updated} agendamento(s) confirmado(s).')
    confirmar_agendamentos.short_description = "Confirmar agendamentos selecionados"
    
    def cancelar_confirmacao(self, request, queryset):
        updated = queryset.update(confirmado=False)
        self.message_user(request, f'{updated} agendamento(s) com confirmação cancelada.')
    cancelar_confirmacao.short_description = "Cancelar confirmação dos selecionados"