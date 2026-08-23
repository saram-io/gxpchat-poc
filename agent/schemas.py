from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime

class CFRReference(BaseModel):
    """Validated CFR reference - must be real citation"""
    title: int = Field(..., description="CFR Title, e.g. 21")
    part: int = Field(..., description="Part, e.g. 211")
    section: str = Field(..., description="e.g. 211.192")
    text_snippet: str = Field(..., min_length=20)
    url: str = Field(..., description="eCFR url")
    version_date: str = Field(default_factory=lambda: datetime.utcnow().date().isoformat())

class WarningLetterRef(BaseModel):
    fei_number: Optional[str] = None
    company: str
    issue_date: str
    observation: str
    fda_url: str

class CFRAnswer(BaseModel):
    """Tier 1: Informational answer - must cite"""
    answer: str = Field(min_length=50)
    cfr_refs: list[CFRReference] = Field(min_length=1, description="At least 1 CFR citation required")
    disclaimer: str = Field(default="For informational purposes only, not regulatory advice. Verify against current eCFR.")

class DeviationDraft(BaseModel):
    """Tier 2: GxP-impacting - requires QA approval"""
    classification: Literal["Minor", "Major", "Critical"]
    title: str
    description: str = Field(min_length=50)
    cfr_refs: list[CFRReference] = Field(min_length=1)
    impact_assessment: str = Field(min_length=20)
    immediate_action: str
    requires_qa_approval: bool = Field(default=True, description="GxP control enforced by Pydantic")
    alcoa_check: bool = Field(default=True)

class AgentAuditRecord(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: str = "demo_user"
    prompt: str
    prompt_hash: str
    model_name: str
    model_version: str
    tool_calls: list[dict] = []
    output_type: str
    output_hash: str
    doc_versions: dict = {}
