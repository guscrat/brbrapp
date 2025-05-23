from django.urls import path
from .views import PagamentoListCreateView

urlpatterns = [
    path('', PagamentoListCreateView.as_view()),
]
