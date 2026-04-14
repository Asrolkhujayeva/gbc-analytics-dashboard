import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

CRM_URL = os.getenv('RETAILCRM_BASE_URL').rstrip('/')
CRM_KEY = os.getenv('RETAILCRM_API_KEY')
SB_URL = os.getenv('SUPABASE_URL').rstrip('/')
SB_KEY = os.getenv('SUPABASE_KEY')

def sync():
    print("🔄 Получаю данные из RetailCRM...")
    crm_res = requests.get(f"{CRM_URL}/api/v5/orders", params={'apiKey': CRM_KEY, 'limit': 50})
    orders = crm_res.json().get('orders', [])

    headers = {
        "apikey": SB_KEY,
        "Authorization": f"Bearer {SB_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates" 
    }

    supabase_api_url = f"{SB_URL}/rest/v1/orders"
    success_count = 0

    for o in orders:
        # ЛОГИКА ИСПРАВЛЕНИЯ СУММЫ:
        # 1. Сначала пробуем взять готовую общую сумму
        total = o.get('totalSum')
        
        # 2. Если она 0 или None, считаем вручную по товарам (items)
        if not total or float(total) == 0:
            items = o.get('items', [])
            total = sum(float(item.get('initialPrice', 0)) * int(item.get('quantity', 1)) for item in items)

        payload = {
            "id": o.get('id'),
            "external_id": o.get('externalId'),
            "first_name": o.get('firstName'),
            "last_name": o.get('lastName'),
            "total_sum": float(total), # Записываем число
            "status": o.get('status')
        }
        
        try:
            res = requests.post(supabase_api_url, headers=headers, json=payload)
            if res.status_code in [200, 201, 204]:
                success_count += 1
                print(f"✅ Заказ {o.get('id')} — Сумма: {total} ₸")
            else:
                print(f"❌ Ошибка Supabase ({res.status_code}): {res.text}")
        except Exception as e:
            print(f"⚠️ Ошибка сети: {e}")

    print(f"\n🚀 Готово! Обновлено заказов: {success_count}")

if __name__ == "__main__":
    sync()
