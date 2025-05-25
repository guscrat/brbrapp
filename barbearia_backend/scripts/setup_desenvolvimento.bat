echo "Aplicando migracoes..."
python manage.py migrate

echo "Criando superusuario (admin/admin123)..."
python manage.py criar_superuser

echo "Populando dados de teste..."
python manage.py popular_dados --clear

echo "Pronto! Agora execute o servidor com:"
echo "python manage.py runserver"