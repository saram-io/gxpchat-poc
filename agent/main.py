from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
import os, asyncio
from dotenv import load_dotenv

load_dotenv()

from .agent import run_gxp_agent
from .audit import log_audit, create_audit_record, hash_text

app = FastAPI(title="GxPChat Agent - Pydantic AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str
    output_type: str = "CFRAnswer"  # or DeviationDraft
    user_id: str = "demo_user"

@app.get("/")
async def root():
    return {"status": "GxPChat Agent running", "model": os.getenv("MODEL_NAME"), "mock": os.getenv("MOCK_MODE")}

@app.post("/agent/stream")
async def stream_agent(req: ChatRequest):
    async def gen():
        tool_calls = []
        try:
            output = await run_gxp_agent(req.prompt, req.output_type)

            # Convert Pydantic model to text + structured data
            if hasattr(output, "model_dump_json"):
                json_data = output.model_dump_json(indent=2)
                text_output = f"{output.answer if hasattr(output, 'answer') else output.description}\n\nCitations:\n"
                for ref in output.cfr_refs:
                    text_output += f"- {ref.title} CFR {ref.section}: {ref.text_snippet} ({ref.url})\n"

                # Audit
                audit_rec = create_audit_record(
                    prompt=req.prompt,
                    model_name=os.getenv("MODEL_NAME", "mock"),
                    tool_calls=tool_calls,
                    output_type=output.__class__.__name__,
                    output_text=json_data,
                    doc_versions={"ecfr": "2024-12-01", "ich": "2024-01-01"}
                )
                log_audit(audit_rec)

                # Stream text in chunks for Vercel AI SDK compatibility
                for i in range(0, len(text_output), 40):
                    chunk = text_output[i:i+40]
                    # Vercel AI SDK expects plain text chunks, we yield as SSE
                    yield chunk
                    await asyncio.sleep(0.02)

                # Finally yield structured JSON for UI to parse refs
                yield f"\n\n__STRUCTURED__{json_data}"
            else:
                yield str(output)

        except Exception as e:
            yield f"Error: {str(e)}"

    return StreamingResponse(gen(), media_type="text/plain; charset=utf-8")

@app.post("/agent/run")
async def run_agent_sync(req: ChatRequest):
    output = await run_gxp_agent(req.prompt, req.output_type)
    return JSONResponse(output.model_dump() if hasattr(output, "model_dump") else {"output": str(output)})
