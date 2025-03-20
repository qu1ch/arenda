import json

from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from core.models import Order, FreeEquipment, Equipment, RentalRequest
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404



@staff_member_required
def admin_orders_view(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'administrator/admin_orders.html', {'orders': orders})


@staff_member_required
def update_order_status(request, order_id, status):
    order = get_object_or_404(Order, id=order_id)

    if status == "confirm":
        order.status = "Ожидает оплаты"
    elif status == "reject":
        order.status = "Отменен"

    order.save()
    return redirect('administrator:admin_orders')


@staff_member_required
def equipment_list(request):
    equipment = FreeEquipment.objects.all()
    equipment_types = Equipment.objects.all()
    return render(request, 'administrator/equipment_list.html',
                  {'equipment': equipment, 'equipment_types': equipment_types})


@staff_member_required
@csrf_exempt
def add_equipment(request):
    if request.method == "POST":
        equipment_id = request.POST.get("equipment_id")
        name = request.POST.get("name")
        number = request.POST.get("number")
        lifting_capacity = request.POST.get("lifting_capacity") or None
        boom_reach = request.POST.get("boom_reach") or None
        lift_height = request.POST.get("lift_height") or None
        body_volume = request.POST.get("body_volume") or None

        if equipment_id and name:
            equipment = get_object_or_404(Equipment, id=equipment_id)
            new_equipment = FreeEquipment.objects.create(
                equipment=equipment,
                name=name,
                number=number,
                lifting_capacity=lifting_capacity,
                boom_reach=boom_reach,
                lift_height=lift_height,
                body_volume=body_volume,
                status="Свободно"
            )
            return JsonResponse({
                "success": True,
                "id": new_equipment.id,
                "name": new_equipment.name,
                "number": new_equipment.number,
                "equipment_name": new_equipment.equipment.name,
                "lifting_capacity": new_equipment.lifting_capacity or "—",
                "boom_reach": new_equipment.boom_reach or "—",
                "lift_height": new_equipment.lift_height or "—",
                "body_volume": new_equipment.body_volume or "—",
                "status": new_equipment.status
            })

    return JsonResponse({"success": False, "error": "Ошибка при добавлении техники."})


@staff_member_required
def update_equipment_status(request):
    if request.method == "POST":
        equipment_id = request.POST.get("equipment_id")
        new_status = request.POST.get("new_status")

        equipment = get_object_or_404(FreeEquipment, id=equipment_id)
        equipment.status = new_status
        equipment.save()

        return JsonResponse({"success": True, "new_status": new_status})

    return JsonResponse({"success": False})


@staff_member_required
def admin_rental_requests(request):
    rental_requests = RentalRequest.objects.filter()
    return render(request, "administrator/admin_rental_requests.html", {"rental_requests": rental_requests})

@staff_member_required
def approve_rental_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        request_id = data.get("request_id")
        new_status = data.get("status")

        rental_request = get_object_or_404(RentalRequest, id=request_id)
        rental_request.status = new_status
        rental_request.save()

        if new_status == "Одобрено":
            FreeEquipment.objects.create(
                equipment=rental_request.equipment,
                name=rental_request.name,
                lifting_capacity=rental_request.lifting_capacity,
                boom_reach=rental_request.boom_reach,
                lift_height=rental_request.lift_height,
                body_volume=rental_request.body_volume,
                number=rental_request.number,
                driver=rental_request.driver,
                status="Свободно"  # По умолчанию техника свободна
            )

        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)