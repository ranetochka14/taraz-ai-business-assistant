from django.db import models

class BusinessProfile(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название бизнеса")
    category = models.CharField(max_length=100, verbose_name="Категория")
    description = models.TextField(verbose_name="Описание и особенности")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255, verbose_name="Товар / Услуга")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена (₸)")
    stock = models.PositiveIntegerField(default=0, verbose_name="Остаток на складе")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return f"{self.title} ({self.price} ₸)"

class ChatLog(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='chats')
    client_identifier = models.CharField(max_length=100, verbose_name="ID клиента (Telegram ID)")
    user_message = models.TextField(verbose_name="Сообщение клиента")
    ai_response = models.TextField(verbose_name="Ответ ИИ")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Чат с {self.client_identifier} от {self.timestamp}"