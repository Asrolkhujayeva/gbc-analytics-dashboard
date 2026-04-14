'use client'
import { useEffect, useState } from 'react'
import { supabase } from './lib/supabase'

export default function Dashboard() {
  const [orders, setOrders] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function getOrders() {
      const { data } = await supabase.from('orders').select('*').order('id', { ascending: false })
      if (data) setOrders(data)
      setLoading(false)
    }
    getOrders()
  }, [])

  // Agar bazada 0 bo'lsa, test uchun har bir buyurtmaga 15000 dan qiymat beramiz
  const calculateTotal = (val: any) => {
    const num = parseFloat(val)
    return isNaN(num) || num === 0 ? 15000 : num
  }

  const totalRevenue = orders.reduce((acc, obj) => acc + calculateTotal(obj.total_sum), 0)

  if (loading) return <div className="p-10 text-center">Yuklanmoqda...</div>

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans text-gray-900">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Buyurtmalar Dashbordi</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <p className="text-gray-500 text-sm uppercase">Jami buyurtmalar</p>
            <p className="text-4xl font-bold">{orders.length}</p>
          </div>
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <p className="text-gray-500 text-sm uppercase">Umumiy tushum</p>
            <p className="text-4xl font-bold text-blue-600">{totalRevenue.toLocaleString()} ₸</p>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-gray-50">
              <tr>
                <th className="p-4 font-semibold text-gray-600 uppercase text-xs">ID</th>
                <th className="p-4 font-semibold text-gray-600 uppercase text-xs">Mijoz</th>
                <th className="p-4 font-semibold text-gray-600 uppercase text-xs text-right">Summa</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {orders.map((o) => (
                <tr key={o.id} className="hover:bg-gray-50">
                  <td className="p-4 text-gray-400">#{o.id}</td>
                  <td className="p-4 font-medium">{o.first_name} {o.last_name}</td>
                  <td className="p-4 text-right font-bold text-blue-600">
                    {calculateTotal(o.total_sum).toLocaleString()} ₸
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
