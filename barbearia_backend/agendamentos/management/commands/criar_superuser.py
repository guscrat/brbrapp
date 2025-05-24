from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Cria um superusuário admin padrão para desenvolvimento'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@barbearia.com'
        password = 'admin123'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Usuário "{username}" já existe!')
            )
            return
        
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name='Administrador',
            last_name='Sistema'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Superusuário criado com sucesso!')
        )
        self.stdout.write(f'Username: {username}')
        self.stdout.write(f'Email: {email}')
        self.stdout.write(f'Password: {password}')
        self.stdout.write('\n🔗 Acesse: http://127.0.0.1:8000/admin/')
