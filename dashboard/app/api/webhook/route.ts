import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  try {
    const order = await req.json();
    const totalSum = Number(order.totalSum || order.total_sum);

    // Условие по заданию: сумма > 50,000 ₸
    if (totalSum > 50000) {
      const token = process.env.TELEGRAM_BOT_TOKEN;
      const chatId = process.env.TELEGRAM_CHAT_ID;
      const text = `💰 Крупный заказ!\nID: ${order.id}\nСумма: ${totalSum.toLocaleString()} ₸\nКлиент: ${order.firstName || 'Клиент'}`;

      await fetch(`https://telegram.org{token}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: chatId, text }),
      });
    }
    return NextResponse.json({ ok: true });
  } catch (err) {
    return NextResponse.json({ ok: false }, { status: 500 });
  }
}
