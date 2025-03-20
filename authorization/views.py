import re
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User
from core.models import Worker


def validate_password(password):
    if len(password) < 8:
        raise ValidationError('Пароль должен содержать минимум 8 символов.')

    if not re.search(r'[A-Z]', password):
        raise ValidationError('Пароль должен содержать хотя бы одну заглавную букву.')

    if not re.search(r'[0-9]', password):
        raise ValidationError('Пароль должен содержать хотя бы одну цифру.')


def validate_username(username):
    if len(username) < 3:
        raise ValidationError('Имя пользователя должно быть не менее 3 символов.')

    if not re.match(r'^[\w.@+-]+$', username):
        raise ValidationError('Имя пользователя может содержать только буквы, цифры, и символы @ . + -.')



def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()
        role = request.POST.get('role', 'tenant')

        if not all([first_name, last_name, phone_number, username, password, email, role]):
            messages.error(request, "Пожалуйста, заполните все поля.")
            return redirect('authorization:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Пользователь с таким именем уже существует.")
            return redirect('authorization:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Пользователь с таким email уже существует.")
            return redirect('authorization:register')

        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect('authorization:register')

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            role=role
        )

        if role == 'landlord':
            Worker.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number
            )

        login(request, user)
        return redirect('account:account')

    return render(request, 'authorization/register.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('account:account')  # Перенаправление на главную страницу
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')

    return render(request, 'authorization/login.html')
