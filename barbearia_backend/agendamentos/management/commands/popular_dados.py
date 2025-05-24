from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from agendamentos.models import Servico, HorarioDisponivel
from datetime import datetime, timedelta, time
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados iniciais para teste'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpa os dados existentes antes de popular',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Limpando dados existentes...')
            HorarioDisponivel.objects.all().delete()
            Servico.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        # Criar usuários de teste
        self.stdout.write('Criando usuários...')
        
        # Barbeiros
        barbeiros_data = [
            {'username': 'joao_barbeiro', 'first_name': 'João', 'last_name': 'Silva', 'email': 'joao@barbearia.com'},
            {'username': 'carlos_barbeiro', 'first_name': 'Carlos', 'last_name': 'Santos', 'email': 'carlos@barbearia.com'},
            {'username': 'pedro_barbeiro', 'first_name': 'Pedro', 'last_name': 'Oliveira', 'email': 'pedro@barbearia.com'},
        ]
        
        barbeiros = []
        for data in barbeiros_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email'],
                    'is_barbeiro': True,
                    'password': 'pbkdf2_sha256$720000$dummy$dummy'  # senha: 123456
                }
            )
            if created:
                user.set_password('123456')
                user.save()
            barbeiros.append(user)
            self.stdout.write(f'  ✓ Barbeiro: {user.get_full_name()} ({user.username})')

        # Clientes
        clientes_data = [
            {'username': 'maria_cliente', 'first_name': 'Maria', 'last_name': 'Costa', 'email': 'maria@email.com'},
            {'username': 'jose_cliente', 'first_name': 'José', 'last_name': 'Ferreira', 'email': 'jose@email.com'},
            {'username': 'ana_cliente', 'first_name': 'Ana', 'last_name': 'Pereira', 'email': 'ana@email.com'},
        ]
        
        clientes = []
        for data in clientes_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email'],
                    'is_barbeiro': False,
                    'password': 'pbkdf2_sha256$720000$dummy$dummy'  # senha: 123456
                }
            )
            if created:
                user.set_password('123456')
                user.save()
            clientes.append(user)
            self.stdout.write(f'  ✓ Cliente: {user.get_full_name()} ({user.username})')

        # Criar serviços
        self.stdout.write('Criando serviços...')
        servicos_data = [
            {'nome': 'Corte Masculino', 'duracao_minutos': 30, 'preco': 25.00},
            {'nome': 'Barba', 'duracao_minutos': 20, 'preco': 15.00},
            {'nome': 'Corte + Barba', 'duracao_minutos': 45, 'preco': 35.00},
            {'nome': 'Sobrancelha', 'duracao_minutos': 15, 'preco': 10.00},
            {'nome': 'Corte Infantil', 'duracao_minutos': 25, 'preco': 20.00},
        ]
        
        servicos = []
        for data in servicos_data:
            servico, created = Servico.objects.get_or_create(
                nome=data['nome'],
                defaults={
                    'duracao_minutos': data['duracao_minutos'],
                    'preco': data['preco']
                }
            )
            servicos.append(servico)
            status = '✓ Criado' if created else '• Já existe'
            self.stdout.write(f'  {status}: {servico.nome} - R$ {servico.preco}')

        # Criar horários disponíveis
        self.stdout.write('Criando horários disponíveis...')
        
        # Horários de funcionamento: 8h às 18h
        horarios = [
            time(8, 0), time(8, 30), time(9, 0), time(9, 30),
            time(10, 0), time(10, 30), time(11, 0), time(11, 30),
            time(14, 0), time(14, 30), time(15, 0), time(15, 30),
            time(16, 0), time(16, 30), time(17, 0), time(17, 30)
        ]
        
        # Criar horários para os próximos 14 dias
        hoje = datetime.now().date()
        contador = 0
        
        for barbeiro in barbeiros:
            for i in range(14):  # Próximos 14 dias
                data = hoje + timedelta(days=i)
                
                # Pular domingos (weekday 6)
                if data.weekday() == 6:
                    continue
                
                # Criar alguns horários aleatórios para cada barbeiro
                horarios_do_dia = random.sample(horarios, random.randint(6, 12))
                
                for hora in horarios_do_dia:
                    horario, created = HorarioDisponivel.objects.get_or_create(
                        barbeiro=barbeiro,
                        data=data,
                        hora=hora
                    )
                    if created:
                        contador += 1

        self.stdout.write(f'  ✓ {contador} horários criados')

        # Resumo final
        self.stdout.write(self.style.SUCCESS('\n=== RESUMO ==='))
        self.stdout.write(f'Barbeiros: {User.objects.filter(is_barbeiro=True).count()}')
        self.stdout.write(f'Clientes: {User.objects.filter(is_barbeiro=False, is_superuser=False).count()}')
        self.stdout.write(f'Serviços: {Servico.objects.count()}')
        self.stdout.write(f'Horários disponíveis: {HorarioDisponivel.objects.count()}')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Dados populados com sucesso!'))
        self.stdout.write('\n📝 CREDENCIAS DE TESTE:')
        self.stdout.write('Barbeiros: joao_barbeiro, carlos_barbeiro, pedro_barbeiro')
        self.stdout.write('Clientes: maria_cliente, jose_cliente, ana_cliente')
        self.stdout.write('Senha para todos: 123456')
