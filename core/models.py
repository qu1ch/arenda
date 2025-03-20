from django.db import models
from django.conf import settings  # Используем кастомную модель пользователя
from django.utils import timezone

from authorization.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Категория")

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="equipment", verbose_name="Категория")
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за час")
    lifting_capacity = models.BooleanField(default=False, verbose_name="Грузоподъемность")
    boom_reach = models.BooleanField(default=False, verbose_name="Вылет стрелы")
    lift_height = models.BooleanField(default=False, verbose_name="Высота подъема")
    body_volume = models.BooleanField(default=False, verbose_name="Объем кузова")
    image = models.ImageField(upload_to='equipment/', verbose_name="Фото")

    def __str__(self):
        return self.name


class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker')
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class FreeEquipment(models.Model):
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE, related_name="free_equipment",
                                  verbose_name="Оборудование")
    name = models.CharField(max_length=255, verbose_name="Название")
    lifting_capacity = models.FloatField(blank=True, null=True,
                                         verbose_name="Грузоподъемность")
    boom_reach = models.FloatField(blank=True, null=True, verbose_name="Вылет стрелы")
    lift_height = models.FloatField(blank=True, null=True, verbose_name="Высота подъема")
    body_volume = models.FloatField(blank=True, null=True, verbose_name="Объем кузова")
    number = models.CharField(max_length=255, verbose_name="Гос номер")
    driver = models.ForeignKey(Worker, on_delete=models.SET_NULL, blank=True, null=True, related_name="orders",
                               verbose_name="Водитель")
    status = models.CharField(
        max_length=50,
        choices=[("Свободно", "Свободно"), ("Занято", "Занято"), ("На ремонте", "На ремонте")],
        default="Свободно",
        verbose_name="Статус"
    )


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь",
                             related_name="orders")  # Связь с пользователем
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="orders",
                                  verbose_name="Оборудование")
    free_equipment = models.ForeignKey(FreeEquipment, on_delete=models.SET_NULL, blank=True, null=True,
                                       related_name="orders",
                                       verbose_name="Свободная техника")  # Связь со свободной техникой
    task_description = models.TextField(verbose_name="Техническое задание")
    order_date = models.DateField(verbose_name="Дата заказа", default=timezone.now)
    order_time = models.TimeField(verbose_name="Время начала", default=timezone.now)
    hours = models.IntegerField(verbose_name="Количество часов", default=1)
    address = models.CharField(max_length=255, verbose_name="Адрес")
    customer_name = models.CharField(max_length=255, verbose_name="Имя заказчика")
    customer_phone = models.CharField(max_length=20, verbose_name="Телефон заказчика")
    total_cost = models.IntegerField(verbose_name="Общая стоимость", default=0)
    created_at = models.DateTimeField(verbose_name="Дата создания", null=True, blank=True)
    status = models.CharField(max_length=50, verbose_name="Статус", default="Ожидает подтверждения")
    lifting_capacity = models.FloatField(blank=True, null=True, verbose_name="Грузоподъемность")
    boom_reach = models.FloatField(blank=True, null=True, verbose_name="Вылет стрелы")
    lift_height = models.FloatField(blank=True, null=True, verbose_name="Высота подъема")
    body_volume = models.FloatField(blank=True, null=True, verbose_name="Объем кузова")
    end_date = models.DateField(verbose_name="Дата окончания", null=True, blank=True)
    end_time = models.TimeField(verbose_name="Время окончания", null=True, blank=True)

    def __str__(self):
        return f"Заказ: {self.equipment.name} - {self.customer_name} - {self.order_date}"


class RentalRequest(models.Model):
    STATUS_CHOICES = [
        ("На рассмотрении", "На рассмотрении"),
        ("Одобрено", "Одобрено"),
        ("Отклонено", "Отклонено"),
    ]

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="rental_requests",
                                  verbose_name="Оборудование")
    name = models.CharField(max_length=255, verbose_name="Название техники")
    lifting_capacity = models.FloatField(blank=True, null=True, verbose_name="Грузоподъемность")
    boom_reach = models.FloatField(blank=True, null=True, verbose_name="Вылет стрелы")
    lift_height = models.FloatField(blank=True, null=True, verbose_name="Высота подъема")
    body_volume = models.FloatField(blank=True, null=True, verbose_name="Объем кузова")
    number = models.CharField(max_length=255, verbose_name="Гос номер")
    driver = models.ForeignKey(Worker, on_delete=models.SET_NULL, blank=True, null=True, related_name="rental_requests",
                               verbose_name="Водитель")

    # Новые поля
    sts_number = models.CharField(max_length=255, verbose_name="Номер СТС")
    driver_license = models.CharField(max_length=255, verbose_name="Водительское удостоверение")
    passport_number = models.CharField(max_length=255, verbose_name="Номер паспорта")

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="На рассмотрении",
        verbose_name="Статус заявки"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подачи заявки")

    def __str__(self):
        return f"Заявка на {self.name} ({self.number}) - {self.status}"