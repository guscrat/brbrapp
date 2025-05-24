from django.urls import path
from .views import ServicoListCreateView, HorarioDisponivelListCreateView, AgendamentoListCreateView

urlpatterns = [
    path('servicos/', ServicoListCreateView.as_view()),
    path('horarios/', HorarioDisponivelListCreateView.as_view()),
    path('agendamentos/', AgendamentoListCreateView.as_view()),
]
