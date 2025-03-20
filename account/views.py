import re
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from authorization.views import validate_password
from core.models import Order, FreeEquipment, Equipment, RentalRequest
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RentalRequestForm


@login_required
def create_rental_request(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = RentalRequestForm(request.POST)
        if form.is_valid():
            rental_request = form.save(commit=False)
            rental_request.driver = request.user.worker
            rental_request.save()

            return JsonResponse({
                'success': True,
                'request': {
                    'id': rental_request.id,
                    'name': rental_request.name,
                    'status': rental_request.get_status_display(),
                    'number': rental_request.number,
                }
            })

    else:
        form = RentalRequestForm()

    user_requests = RentalRequest.objects.filter(driver=request.user.worker)

    return render(request, "account/add_equipment.html", {
        "form": form,
        "user_requests": user_requests
    })

def validate_phone_number(phone_number):
    phone_regex = r'^\+7\d{10}$'
    if not re.match(phone_regex, phone_number):
        raise ValidationError('Номер телефона должен быть в формате +7XXXXXXXXXX')

@login_required
def account_view(request):
    return render(request, 'account/account.html')

def add_equipment(request):
    return render(request, 'account/add_equipment.html')


@login_required
def change_phone_number_view(request):
    return render(request, 'account/change_phone_number.html')


@login_required
def change_email_view(request):
    return render(request, 'account/change_email.html')


@login_required
def change_password_view(request):
    return render(request, 'account/change_password.html')


@login_required
def change_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            validate_email(email)
            request.user.email = email
            request.user.save()
            messages.success(request, 'Почта успешно изменена.')
            return redirect('account:change_email_view')
        except ValidationError:
            messages.error(request, 'Введите корректный email.')

    return render(request, 'account/change_email.html')



@login_required
def change_phone_number(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        try:
            # Валидация номера телефона
            validate_phone_number(phone_number)
            # Обновляем номер телефона текущего пользователя
            request.user.phone_number = phone_number
            request.user.save()
            messages.success(request, 'Номер телефона успешно изменен.')
            return redirect('account:change_phone_number_view')  # Редирект на страницу аккаунта
        except ValidationError:
            messages.error(request, 'Введите корректный номер телефона в формате +7XXXXXXXXXX.')

    return render(request, 'account/change_phone_number.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        password = new_password

        if new_password != confirm_password:
            messages.error(request, 'Новый пароль и подтверждение пароля не совпадают.')
            return redirect('account:change_password_view')

        if not request.user.check_password(current_password):
            messages.error(request, 'Текущий пароль неверен.')
            return redirect('account:change_password_view')

        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, e.message)
            return redirect('account:change_password_view')

        request.user.set_password(new_password)
        request.user.save()

        update_session_auth_hash(request, request.user)

        messages.success(request, 'Пароль успешно изменен.')
        return redirect('account:change_password_view')

    return render(request, 'change_password.html')


@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user)  # Фильтруем заказы только для текущего пользователя
    return render(request, "account/user_orders.html", {"orders": orders})


def equipment_list(request):
    equipment = FreeEquipment.objects.filter(driver=request.user.worker)
    return render(request, 'account/equipment_list.html',
                  {'equipment': equipment})




@login_required
def orders(request):
    worker = request.user.worker

    free_equipment = FreeEquipment.objects.filter(driver=worker)

    orders = Order.objects.filter(free_equipment__in=free_equipment)

    return render(request, 'account/user_orders_t.html', {'orders': orders})
