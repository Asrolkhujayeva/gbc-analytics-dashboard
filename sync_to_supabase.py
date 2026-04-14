import os
import requests
from dotenv import load_dotenv

load_dotenv()

CRM_URL = os.getenv('RETAILCRM_BASE_URL').rstrip('/')
CRM_KEY = os.getenv('RETAILCRM_API_KEY')
SB_URL = os.getenv('SUPABASE_URL').rstrip('/')
SB_KEY = os.getenv('SUPABASE_KEY')

# Данные Telegram
TG_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TG_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_telegram(order_id, total_sum):
    """Функция отправки уведомления в Telegram"""
    text = f"💰 Крупный заказ!\nID: {order_id}\nСумма: {total_sum} ₸"
    url = f"https://telegram.org{TG_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TG_CHAT_ID, "text": text})
        print(f"✈️ Уведомление в Telegram отправлено!")
    except Exception as e:
        print(f"⚠️ Ошибка Telegram: {e}")

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

    for o in orders:
        total = float(o.get('totalSum', 0))
        order_id = o.get('id')

        # --- ШАГ 5: ПРОВЕРКА СУММЫ ---
        if total > 50000:
            send_telegram(order_id, total)
        # -----------------------------

        payload = {
            "id": order_id,
            "external_id": o.get('externalId'),
            "first_name": o.get('firstName'),
            "last_name": o.get('lastName'),
            "total_sum": total,
            "status": o.get('status')
        }
        
        requests.post(f"{SB_URL}/rest/v1/orders", headers=headers, json=payload)
        print(f"✅ Заказ {order_id} синхронизирован.")

if __name__ == "__main__":
    sync()
