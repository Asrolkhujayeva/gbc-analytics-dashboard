'use client'
import { useEffect, useState } from 'react'
import { supabase } from './lib/supabase'

export default function Dashboard() {
  const [orders, setOrders] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function getOrders() {
      const { data, error } = await supabase
        .from('orders') // Название таблицы
        .select('*')
        .order('id', { ascending: false })
      
      if (data) setOrders(data)
      setLoading(false)
    }
    getOrders()
  }, [])

  // Считаем сумму, принудительно превращая строку из базы в число
  const totalRevenue = orders.reduce((acc, obj) => {
    const sum = obj.total_sum || 0 
    return acc + parseFloat(sum.toString())
  }, 0)

  if (loading) return <div className="p-10 text-center">Загрузка данных...</div>

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 p-4 md:p-10">
      <div className="max-w-6xl mx-auto">
        <header className="mb-10">
          <h1 className="text-3xl font-extrabold tracking-tight">Дашборд заказов</h1>
          <p className="text-gray-500 mt-2">Мониторинг из таблицы orders</p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <p className="text-sm font-medium text-gray-500 uppercase">Всего заказов</p>
            <p className="text-3xl font-bold mt-2">{orders.length}</p>
          </div>
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <p className="text-sm font-medium text-gray-500 uppercase">Общая выручка</p>
            <p className="text-3xl font-bold mt-2 text-indigo-600">
              {totalRevenue.toLocaleString()} ₸
            </p>
          </div>
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <p className="text-sm font-medium text-gray-500 uppercase">Средний чек</p>
            <p className="text-3xl font-bold mt-2">
              {Math.round(totalRevenue / (orders.length || 1)).toLocaleString()} ₸
            </p>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <table className="w-full text-left">
            <thead>
              <tr className="bg-gray-50 border-b border-gray-100">
                <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase">ID</th>
                <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Клиент</th>
                <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase text-right">Сумма</th>
                <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase text-center">Статус</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {orders.map((order) => (
                <tr key={order.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 text-sm text-gray-400">#{order.id}</td>
                  <td className="px-6 py-4 font-medium">{order.first_name} {order.last_name}</td>
                  <td className="px-6 py-4 text-sm font-bold text-right">
                    {/* Используем parseFloat для работы с типом decimal */}
                    {parseFloat(order.total_sum || 0).toLocaleString()} ₸
                  </td>
                  <td className="px-6 py-4 text-center">
                    <span className="px-3 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-700">
                      {order.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
