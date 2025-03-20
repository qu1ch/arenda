from django.http import HttpResponse
from .models import Equipment, Category, Order, FreeEquipment
from datetime import timedelta, datetime
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


def catalog(request):
    categories = Category.objects.prefetch_related('equipment').all()
    return render(request, 'core/catalog.html', {'categories': categories})


def core(request):
    return HttpResponse("Ошибка")


@login_required
def order_success(request):
    return render(request, 'core/success.html')


def equipment_order(request, equipment_id):
    if request.user.is_authenticated:
        equipment = get_object_or_404(Equipment, id=equipment_id)


        customer_name = request.user.get_full_name() or request.user.username
        customer_phone = getattr(request.user, 'phone_number', '') or ''

        if request.method == 'POST':

            task_description = request.POST.get('task_description')
            order_date = request.POST.get('order_date')
            order_time = request.POST.get('order_time')
            hours = request.POST.get('hours')
            hours = int(hours) if hours and hours.isdigit() else 8
            address = request.POST.get('address')
            lifting_capacity = request.POST.get('lifting_capacity')
            boom_reach = request.POST.get('boom_reach')
            lift_height = request.POST.get('lift_height')
            body_volume = request.POST.get('body_volume')

            order_start = datetime.combine(datetime.strptime(order_date, '%Y-%m-%d'),
                                           datetime.strptime(order_time, '%H:%M').time())
            order_end = order_start + timedelta(hours=hours)

            filtered_equipment = FreeEquipment.objects.filter(
                equipment=equipment,
                status="Свободно"
            )

            if lifting_capacity:
                filtered_equipment = filtered_equipment.filter(
                    lifting_capacity__gte=float(lifting_capacity)
                )
            if boom_reach:
                filtered_equipment = filtered_equipment.filter(
                    boom_reach__gte=float(boom_reach)
                )
            if lift_height:
                filtered_equipment = filtered_equipment.filter(
                    lift_height__gte=float(lift_height)
                )
            if body_volume:
                filtered_equipment = filtered_equipment.filter(
                    body_volume__gte=float(body_volume)
                )

            if not filtered_equipment.exists():
                return render(request, 'core/equipment_order.html', {
                    'equipment': equipment,
                    'customer_name': customer_name,
                    'customer_phone': customer_phone,
                    'error_message': 'Нет подходящей техники'
                })

            conflicting_orders_info = []
            date_range_start = order_start - timedelta(days=1)
            date_range_end = order_start + timedelta(days=1)

            for free_equipment in filtered_equipment:
                conflicting_orders = Order.objects.filter(
                    free_equipment=free_equipment,
                    status__in=["Создан", "Ожидает подтверждения", "Ожидает оплаты"],
                    order_date__range=(date_range_start.date(), date_range_end.date())
                )

                for order in conflicting_orders:
                    existing_order_start = datetime.combine(order.order_date, order.order_time)
                    existing_order_end = datetime.combine(order.end_date, order.end_time)

                    if existing_order_end > order_start and existing_order_start < order_end:
                        conflicting_orders_info.append({
                            'start': existing_order_start,
                            'end': existing_order_end
                        })
                        break
                else:
                    total_cost = hours * equipment.price_per_hour
                    end_date = order_end.date()
                    end_time = order_end.time()
                    custom_created_at = timezone.localtime(timezone.now())

                    order = Order.objects.create(
                        user=request.user,
                        equipment=equipment,
                        free_equipment=free_equipment,
                        task_description=task_description,
                        order_date=order_date,
                        order_time=order_time,
                        hours=hours,
                        address=address,
                        customer_name=customer_name,
                        customer_phone=customer_phone,
                        total_cost=total_cost,
                        lifting_capacity=lifting_capacity,
                        boom_reach=boom_reach,
                        lift_height=lift_height,
                        body_volume=body_volume,
                        end_date=end_date,
                        end_time=end_time,
                        created_at=custom_created_at
                    )

                    return redirect('core:order_success')

            return render(request, 'core/equipment_order.html', {
                'equipment': equipment,
                'customer_name': customer_name,
                'customer_phone': customer_phone,
                'error_message': 'Нет подходящей свободной техники',
                'conflicting_orders': conflicting_orders_info
            })

        return render(request, 'core/equipment_order.html', {
            'equipment': equipment,
            'customer_name': customer_name,
            'customer_phone': customer_phone
        })
    else:
        return redirect('authorization:login')


def update_free_equipment_status():
    now = timezone.localtime(timezone.now())
    print(now)

    orders = Order.objects.all()

    for order in orders:
        order_start = timezone.make_aware(datetime.combine(order.order_date, order.order_time))

        if order.end_date and order.end_time:
            order_end = timezone.make_aware(datetime.combine(order.end_date, order.end_time))
        else:
            order_end = None

        if order_end and order_start <= now <= order_end:
            if order.free_equipment:
                free_equipment = order.free_equipment
                free_equipment.status = "Занято"
                free_equipment.save()
            order.status = "В процессе"
            order.save()

        elif order_end and now > order_end:
            if order.free_equipment:
                free_equipment = order.free_equipment
                free_equipment.status = "Свободно"
                free_equipment.save()
            order.status = "Завершен"
            order.save()

    pending_orders = Order.objects.filter(status="Ожидает оплаты")
    for order in pending_orders:
        time_since_created = now - order.created_at
        if time_since_created > timedelta(minutes=30):
            order.status = "Отменен"
            order.save()

    pending_confirmation_orders = Order.objects.filter(status="Ожидает подтверждения")
    for order in pending_confirmation_orders:
        time_since_created = now - order.created_at
        if time_since_created > timedelta(minutes=1):
            order.status = "Ожидает оплаты"
            order.save()


@login_required
def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == "POST":
        order.status = "Создан"
        order.save()
        return redirect('account:user_orders')

    return render(request, 'core/payment.html', {'order': order})
