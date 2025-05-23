from django.db import models
from django.conf import settings

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    duracao_minutos = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.nome

class HorarioDisponivel(models.Model):
    barbeiro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'is_barbeiro': True}
    )
    data = models.DateField()
    hora = models.TimeField()

    class Meta:
        unique_together = ('barbeiro', 'data', 'hora')

    def __str__(self):
        return f"{self.barbeiro.username} - {self.data} {self.hora}"

class Agendamento(models.Model):
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='agendamentos'
    )
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    horario = models.ForeignKey(HorarioDisponivel, on_delete=models.CASCADE)
    confirmado = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente.username} - {self.horario}"
 