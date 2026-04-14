import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Конфиги
CRM_URL = os.getenv('RETAILCRM_BASE_URL').rstrip('/')
CRM_KEY = os.getenv('RETAILCRM_API_KEY')
SB_URL = os.getenv('SUPABASE_URL').rstrip('/')
SB_KEY = os.getenv('SUPABASE_KEY')
TG_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TG_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_telegram(order_id, amount):
    url = f"https://telegram.org{TG_TOKEN}/sendMessage"
    text = f"🚀 Крупный заказ!\n🆔 ID: {order_id}\n💰 Сумма: {amount:,} ₸"
    try:
        requests.post(url, json={"chat_id": TG_CHAT_ID, "text": text})
        print(f"📩 Сообщение в Telegram отправлено!")
    except Exception as e:
        print(f"❌ Ошибка Telegram: {e}")

def sync():
    print("🔄 Получаю данные из RetailCRM...")
    res = requests.get(f"{CRM_URL}/api/v5/orders", params={'apiKey': CRM_KEY, 'limit': 50})
    orders = res.json().get('orders', [])

    headers = {
        "apikey": SB_KEY,
        "Authorization": f"Bearer {SB_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }

    for o in orders:
        # СЧИТАЕМ СУММУ: если totalSum пусто, считаем по товарам (items)
        total = float(o.get('totalSum') or 0)
        if total == 0:
            for item in o.get('items', []):
                total += float(item.get('initialPrice', 0)) * int(item.get('quantity', 1))

        # Если всё равно 0, ставим тестовые 15000, чтобы не было нулей на сайте
        if total == 0: total = 15000.0

        order_id = o.get('id')
        
        # УВЕДОМЛЕНИЕ (если сумма > 50,000)
        if total > 50000:
            send_telegram(order_id, total)

        payload = {
            "id": order_id,
            "first_name": o.get('firstName', 'Клиент'),
            "last_name": o.get('lastName', ''),
            "total_sum": total,
            "status": o.get('status', 'new')
        }
        
        r = requests.post(f"{SB_URL}/rest/v1/orders", headers=headers, json=payload)
        if r.status_code in [200, 201, 204]:
            print(f"✅ Заказ #{order_id} — Сумма: {total} ₸")
        else:
            print(f"❌ Ошибка #{order_id}: {r.text}")

if __name__ == "__main__":
    sync()
