'use client'

import { useState } from 'react'
import { Send, Wallet, CreditCard, DollarSign } from 'lucide-react'

export default function TransfersPanel() {
  const [transferType, setTransferType] = useState('bank')
  const [amount, setAmount] = useState('')
  const [loading, setLoading] = useState(false)

  const handleTransfer = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const endpoint = 
        transferType === 'bank' ? '/api/v1/transfers/bank' :
        transferType === 'crypto' ? '/api/v1/transfers/crypto' :
        '/api/v1/transfers/paypal'

      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount: parseFloat(amount) })
      })

      const data = await response.json()
      alert(`Transfer initiated: ${data.transaction_id}`)
      setAmount('')
    } catch (error) {
      alert('Transfer failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-gradient-to-br from-blue-900/40 to-blue-900/20 border border-blue-500/30 p-6 rounded-lg">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold">Bank Transfer</h3>
            <CreditCard className="w-5 h-5 text-blue-400" />
          </div>
          <p className="text-2xl font-bold">$0.00</p>
          <p className="text-xs text-slate-400 mt-2">Total transferred</p>
        </div>

        <div className="bg-gradient-to-br from-orange-900/40 to-orange-900/20 border border-orange-500/30 p-6 rounded-lg">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold">Crypto Transfer</h3>
            <Wallet className="w-5 h-5 text-orange-400" />
          </div>
          <p className="text-2xl font-bold">0 ETH</p>
          <p className="text-xs text-slate-400 mt-2">Total transferred</p>
        </div>

        <div className="bg-gradient-to-br from-purple-900/40 to-purple-900/20 border border-purple-500/30 p-6 rounded-lg">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold">PayPal Transfer</h3>
            <DollarSign className="w-5 h-5 text-purple-400" />
          </div>
          <p className="text-2xl font-bold">$0.00</p>
          <p className="text-xs text-slate-400 mt-2">Total transferred</p>
        </div>
      </div>

      {/* Transfer Form */}
      <div className="bg-slate-900 p-6 rounded-lg border border-slate-700">
        <h2 className="text-2xl font-bold mb-6">Execute Transfer</h2>
        
        <form onSubmit={handleTransfer} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Transfer Type</label>
            <div className="grid grid-cols-3 gap-3">
              {[
                { id: 'bank', label: 'Bank Transfer', icon: '🏦' },
                { id: 'crypto', label: 'Crypto', icon: '₿' },
                { id: 'paypal', label: 'PayPal', icon: '🅿️' }
              ].map((type) => (
                <button
                  key={type.id}
                  type="button"
                  onClick={() => setTransferType(type.id)}
                  className={`p-3 rounded-lg border transition-all ${
                    transferType === type.id
                      ? 'bg-blue-600/20 border-blue-500 text-blue-300'
                      : 'bg-slate-800 border-slate-600 text-slate-300 hover:border-slate-500'
                  }`}
                >
                  <div className="text-2xl mb-1">{type.icon}</div>
                  <div className="text-xs font-medium">{type.label}</div>
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Amount</label>
            <div className="relative">
              <span className="absolute left-3 top-3 text-slate-400">$</span>
              <input
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="0.00"
                className="w-full pl-8 pr-4 py-2 bg-slate-800 border border-slate-600 rounded-lg focus:outline-none focus:border-blue-500"
                required
              />
            </div>
          </div>

          <div className="bg-blue-900/20 border border-blue-500/30 p-4 rounded-lg text-sm">
            <p className="text-slate-300">
              <span className="font-medium">Owner Approval Required:</span> Transfers over $500 require owner approval
            </p>
          </div>

          <button
            type="submit"
            disabled={loading || !amount}
            className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 disabled:cursor-not-allowed text-white font-bold py-3 px-4 rounded-lg transition-colors"
          >
            <Send className="w-4 h-4" />
            {loading ? 'Processing...' : 'Execute Transfer'}
          </button>
        </form>
      </div>

      {/* Recent Transfers */}
      <div className="bg-slate-900 p-6 rounded-lg border border-slate-700">
        <h3 className="text-lg font-bold mb-4">Recent Transfers</h3>
        <div className="text-center py-8 text-slate-400">
          <p>No transfers yet</p>
          <p className="text-sm mt-2">As revenue is generated, transfers will appear here</p>
        </div>
      </div>
    </div>
  )
}
