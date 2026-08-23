import hashlib
import json
from datetime import datetime
from pathlib import Path
from .schemas import AgentAuditRecord

AUDIT_FILE = Path("audit_log.jsonl")
AUDIT_FILE.touch(exist_ok=True)

def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]

def log_audit(record: AgentAuditRecord):
    # In prod: write to Postgres append-only table for Part 11
    with open(AUDIT_FILE, "a") as f:
        f.write(record.model_dump_json() + "\n")
    print(f"[AUDIT] {record.timestamp} - {record.output_type} - tools: {len(record.tool_calls)}")

def create_audit_record(prompt: str, model_name: str, tool_calls: list, output_type: str, output_text: str, doc_versions: dict):
    return AgentAuditRecord(
        prompt=prompt,
        prompt_hash=hash_text(prompt),
        model_name=model_name,
        model_version=model_name,
        tool_calls=tool_calls,
        output_type=output_type,
        output_hash=hash_text(output_text),
        doc_versions=doc_versions
    )
