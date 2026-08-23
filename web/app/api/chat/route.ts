import { NextRequest } from 'next/server'

export const runtime = 'edge'

export async function POST(req: NextRequest) {
  const { messages, outputType } = await req.json()
  const lastMessage = messages[messages.length - 1]?.content || ''

  const agentUrl = process.env.AGENT_URL || 'http://localhost:8000'

  try {
    // Call Pydantic AI agent backend
    const backendRes = await fetch(`${agentUrl}/agent/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt: lastMessage,
        output_type: outputType || 'CFRAnswer',
        user_id: 'web_user'
      })
    })

    if (!backendRes.ok || !backendRes.body) {
      // Fallback mock if backend not running
      const mockText = `GxPChat Agent (mock mode - backend not reachable at ${agentUrl})\n\nFor query: ${lastMessage}\n\nPer 21 CFR 211.192: Any unexplained discrepancy shall be thoroughly investigated, whether or not the batch has already been distributed.\n\nCitation: 21 CFR 211.192 - https://www.ecfr.gov/current/title-21/part-211/section-211.192\n\n[Start backend: cd agent && uvicorn main:app --reload]`;

      const encoder = new TextEncoder()
      const stream = new ReadableStream({
        async start(controller) {
          for (let i = 0; i < mockText.length; i += 30) {
            controller.enqueue(encoder.encode(mockText.slice(i, i+30)))
            await new Promise(r => setTimeout(r, 20))
          }
          controller.close()
        }
      })
      return new Response(stream, {
        headers: { 'Content-Type': 'text/plain; charset=utf-8' }
      })
    }

    // Proxy streaming response from Pydantic AI to Vercel AI SDK
    // Vercel AI SDK useChat expects plain text stream by default
    return new Response(backendRes.body, {
      headers: {
        'Content-Type': 'text/plain; charset=utf-8',
        'Cache-Control': 'no-cache',
      }
    })

  } catch (e) {
    return new Response(`Error connecting to agent: ${e}`, { status: 500 })
  }
}
