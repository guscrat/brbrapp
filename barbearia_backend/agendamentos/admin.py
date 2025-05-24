from django.contrib import admin
from .models import Servico, HorarioDisponivel, Agendamento

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'duracao_minutos', 'preco')
    search_fields = ('nome',)
    ordering = ('nome',)

@admin.register(HorarioDisponivel)
class HorarioDisponivelAdmin(admin.ModelAdmin):
    list_display = ('barbeiro', 'data', 'hora', 'get_barbeiro_nome')
    list_filter = ('data', 'barbeiro')
    search_fields = ('barbeiro__username', 'barbeiro__first_name', 'barbeiro__last_name')
    ordering = ('data', 'hora')
    
    def get_barbeiro_nome(self, obj):
        return obj.barbeiro.get_full_name() or obj.barbeiro.username
    get_barbeiro_nome.short_description = 'Nome do Barbeiro'
    
    # Filtra para mostrar apenas usuários que são barbeiros
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "barbeiro":
            kwargs["queryset"] = db_field.related_model.objects.filter(is_barbeiro=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'servico', 'get_barbeiro', 'get_data_hora', 'confirmado', 'criado_em')
    list_filter = ('confirmado', 'criado_em', 'horario__data', 'servico')
    search_fields = ('cliente__username', 'cliente__first_name', 'cliente__last_name')
    ordering = ('-criado_em',)
    readonly_fields = ('criado_em',)
    
    def get_barbeiro(self, obj):
        return obj.horario.barbeiro.get_full_name() or obj.horario.barbeiro.username
    get_barbeiro.short_description = 'Barbeiro'
    
    def get_data_hora(self, obj):
        return f"{obj.horario.data} {obj.horario.hora}"
    get_data_hora.short_description = 'Data e Hora'