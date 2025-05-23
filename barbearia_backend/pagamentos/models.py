from django.db import models
from agendamentos.models import Agendamento

class Pagamento(models.Model):
    agendamento = models.OneToOneField(Agendamento, on_delete=models.CASCADE)
    metodo = models.CharField(max_length=20, choices=[
        ('pix', 'PIX'),
        ('cartao', 'Cartão'),
        ('manual', 'Manual'),
    ])
    valor = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('falhou', 'Falhou'),
    ], default='pendente')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pagamento {self.agendamento.id} - {self.status}"
