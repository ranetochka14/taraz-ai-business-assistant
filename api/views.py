import os
import requests
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BusinessProfile, ChatLog, Product
from .serializers import (
    BusinessProfileSerializer,
    ChatLogSerializer,
    ProductSerializer,
)

class BusinessProfileViewSet(viewsets.ModelViewSet):
  queryset = BusinessProfile.objects.all()
  serializer_class = BusinessProfileSerializer


class ProductViewSet(viewsets.ModelViewSet):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer


class ChatBotViewSet(viewsets.ModelViewSet):
  queryset = ChatLog.objects.all()
  serializer_class = ChatLogSerializer

  @action(detail=False, methods=['post'])
  def interact(self, request):
    business_id = request.data.get('business_id')
    client_id = request.data.get('client_id')
    user_message = request.data.get('message').lower()

    try:
      business = BusinessProfile.objects.get(id=business_id)
    except BusinessProfile.DoesNotExist:
      return Response({'error': 'Бизнес не найден'}, status=404)

    products = business.products.all()
    catalog_str = '\n'.join(
        [
            f'- {p.title}: {p.price} ₸ (В наличии: {p.stock} шт.)'
            for p in products
        ]
    )

    if (
        'привет' in user_message
        or 'здравствуйте' in user_message
        or 'старт' in user_message
    ):
      ai_reply = (
          f'👋 Здравствуйте! Добро пожаловать в "{business.name}". Я ваш'
          f' персональный ассистент. Чем могу помочь из нашего меню?'
      )
    elif 'цена' in user_message or 'сколько' in user_message or 'меню' in user_message or 'каталог' in user_message:
      ai_reply = (
          f'📋 Вот актуальные позиции и цены в кофейне "{business.name}":\n'
          f'{catalog_str}\nЧто желаете заказать?'
      )
    elif (
        'капучино' in user_message
        or 'чай' in user_message
        or 'медовик' in user_message
    ):
      ai_reply = (
          f'🛒 Отличный выбор! Эта позиция есть в наличии в "{business.name}".'
          ' Оформить заказ или подсказать что-то еще?'
      )
    else:
      ai_reply = (
          f'🤖 В "{business.name}" всегда рады гостям! Наш ассортимент:\n'
          f'{catalog_str}\nНапишите "меню", чтобы уточнить цены, или выберите'
          ' товар.'
      )

    chat_log = ChatLog.objects.create(
        business=business,
        client_identifier=client_id,
        user_message=request.data.get('message'),
        ai_response=ai_reply,
    )

    return Response({
        'client_message': request.data.get('message'),
        'ai_response': ai_reply,
        'log_id': chat_log.id,
    })