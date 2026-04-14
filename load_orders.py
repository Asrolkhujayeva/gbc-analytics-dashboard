import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

RETAILCRM_API_KEY = os.getenv('RETAILCRM_API_KEY')
RETAILCRM_BASE_URL = os.getenv('RETAILCRM_BASE_URL').rstrip('/')

def get_valid_order_type():
    """Запрашивает список типов заказов из CRM и возвращает первый активный код."""
    url = f"{RETAILCRM_BASE_URL}/api/v5/reference/order-types"
    params = {'apiKey': RETAILCRM_API_KEY}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data.get('success') and data.get('orderTypes'):
            # Берем код первого попавшегося типа заказа (например, 'eshop' или 'physical')
            first_code = list(data['orderTypes'].values())[0]['code']
            print(f"🔎 Авто-определение: использую тип заказа '{first_code}'")
            return first_code
    except Exception as e:
        print(f"Ошибка при получении справочников: {e}")
    return None

def load_orders():
    # 1. Получаем реальный код из твоей системы
    valid_type = get_valid_order_type()
    if not valid_type:
        print("❌ Не удалось получить типы заказов. Проверь API ключ.")
        return

    # 2. Читаем файл
    try:
        with open('mock_orders.json', 'r', encoding='utf-8') as f:
            orders_data = json.load(f)
    except FileNotFoundError:
        print("Файл mock_orders.json не найден.")
        return

    print(f"Загрузка {len(orders_data)} заказов в {RETAILCRM_BASE_URL}...")

    for i, order in enumerate(orders_data, 1):
        # Подставляем реально существующий код
        order['orderType'] = valid_type
        
        # На всякий случай уберем orderMethod, если он тоже будет сыпать ошибками
        # CRM сама подставит метод по умолчанию для API
        if 'orderMethod' in order:
            del order['orderMethod']

        payload = {
            'apiKey': RETAILCRM_API_KEY,
            'order': json.dumps(order)
        }

        try:
            res = requests.post(f"{RETAILCRM_BASE_URL}/api/v5/orders/create", data=payload)
            result = res.json()
            if result.get('success'):
                print(f"[{i}/50] ✅ Ок! ID: {result.get('id')}")
            else:
                print(f"[{i}/50] ❌ Ошибка: {result.get('errors')}")
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    load_orders()
