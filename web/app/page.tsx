'use client'
import { useChat } from 'ai/react'
import { useState } from 'react'

export default function GxPChatPage() {
  const [outputType, setOutputType] = useState('CFRAnswer')
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat',
    body: { outputType }
  })

  return (
    <div className="min-h-screen flex flex-col max-w-4xl mx-auto p-6">
      <header className="mb-8 border-b border-zinc-800 pb-6">
        <h1 className="text-3xl font-bold">GxPChat</h1>
        <p className="text-zinc-400 mt-2">Open source ChatGPT for Life Sciences - FDA 21 CFR, EU Annex 1, ICH Q7-Q10</p>
        <div className="mt-4 flex gap-2 text-xs">
          <span className="px-2 py-1 bg-zinc-900 rounded">Pydantic AI Agent</span>
          <span className="px-2 py-1 bg-zinc-900 rounded">Vercel AI SDK UI</span>
          <span className="px-2 py-1 bg-zinc-900 rounded">Part 11 Audit</span>
        </div>
      </header>

      <div className="flex gap-2 mb-4">
        <button 
          onClick={() => setOutputType('CFRAnswer')}
          className={`px-3 py-1 rounded text-sm ${outputType==='CFRAnswer' ? 'bg-white text-black' : 'bg-zinc-800'}`}
        >
          Informational
        </button>
        <button 
          onClick={() => setOutputType('DeviationDraft')}
          className={`px-3 py-1 rounded text-sm ${outputType==='DeviationDraft' ? 'bg-white text-black' : 'bg-zinc-800'}`}
        >
          Deviation Draft (GxP)
        </button>
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto mb-6">
        {messages.length === 0 && (
          <div className="grid grid-cols-2 gap-2 text-sm">
            <button onClick={() => {}} className="p-3 bg-zinc-900 rounded text-left hover:bg-zinc-800">
              What does 21 CFR 211.192 require for investigations?
            </button>
            <button className="p-3 bg-zinc-900 rounded text-left hover:bg-zinc-800">
              Explain EU GMP Annex 1 CCS requirements
            </button>
            <button className="p-3 bg-zinc-900 rounded text-left hover:bg-zinc-800">
              Draft a minor deviation for freezer excursion
            </button>
            <button className="p-3 bg-zinc-900 rounded text-left hover:bg-zinc-800">
              What are the 6 systems in ICH Q10?
            </button>
          </div>
        )}
        {messages.map(m => (
          <div key={m.id} className={`p-4 rounded ${m.role==='user' ? 'bg-zinc-900 ml-12' : 'bg-zinc-800 mr-12'}`}>
            <div className="text-xs text-zinc-500 mb-1">{m.role}</div>
            <div className="whitespace-pre-wrap text-sm leading-relaxed">{m.content}</div>
          </div>
        ))}
        {isLoading && <div className="text-zinc-500 text-sm animate-pulse">GxP Agent validating citations...</div>}
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2 border-t border-zinc-800 pt-4">
        <input
          value={input}
          onChange={handleInputChange}
          placeholder={outputType==='DeviationDraft' ? 'Describe deviation to draft...' : 'Ask about CFR, Annex 1, ICH...'}
          className="flex-1 bg-zinc-900 border border-zinc-800 rounded px-4 py-3 text-sm focus:outline-none focus:border-zinc-600"
        />
        <button type="submit" className="bg-white text-black px-6 py-3 rounded text-sm font-medium">
          Send
        </button>
      </form>

      <p className="text-[11px] text-zinc-600 mt-4 text-center">
        For informational purposes only, not regulatory advice. All responses validated via Pydantic schemas with CFR citations.
      </p>
    </div>
  )
}
