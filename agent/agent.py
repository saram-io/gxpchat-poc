import os
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "openai:gpt-4o-mini")
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true" or not os.getenv("OPENAI_API_KEY")

from .schemas import CFRAnswer, DeviationDraft, CFRReference
from .tools import ecfr, openfda, ich

# System prompt enforces GxP controls
SYSTEM_PROMPT = """
You are GxPChat - an AI assistant for life sciences GxP compliance.

Rules:
1. Always cite 21 CFR Part 11, 210, 211, EU GMP Annex 1, Annex 11, or ICH Q7-Q10 with exact section numbers.
2. Never fabricate a CFR citation. Use tools to search.
3. For informational questions, return CFRAnswer type.
4. For drafting deviations, CAPAs, SOPs, return DeviationDraft and set requires_qa_approval=true.
5. Add disclaimer: For informational purposes only, not regulatory advice.
6. If unsure, say you don't know and suggest verifying against current eCFR.
"""

def _register_tools(agent: Agent) -> None:
    """Register the shared search tools on an agent (called per output type)."""

    @agent.tool
    async def search_ecfr_tool(ctx: RunContext, query: str) -> list[dict]:
        """Search eCFR for FDA regulations. Use for all CFR questions."""
        results = await ecfr.search_ecfr(query)
        return [r.model_dump() for r in results]

    @agent.tool
    async def search_warning_letters_tool(ctx: RunContext, keyword: str) -> list[dict]:
        """Search FDA warning letters for precedent."""
        results = await openfda.search_warning_letters(keyword)
        return [r.model_dump() for r in results]

    @agent.tool
    async def search_ich_tool(ctx: RunContext, query: str) -> list[dict]:
        """Search ICH guidelines Q7-Q10."""
        results = await ich.search_ich(query)
        return [r.model_dump() for r in results]


# Agents are created lazily on first real (non-mock) run: pydantic-ai 2.x
# requires an API key when constructing an OpenAI-backed agent, and mock mode
# must work without one. output_type is fixed at construction in 2.x (the old
# `override(output_type=...)` API was removed), so cache one agent per type.
_agents: dict[str, Agent] = {}

def _get_agent(output_type: str) -> Agent:
    """Build (and cache) the agent for the requested output type."""
    if output_type not in _agents:
        agent = Agent(
            MODEL_NAME,
            instructions=SYSTEM_PROMPT,
            output_type=DeviationDraft if output_type == "DeviationDraft" else CFRAnswer,
        )
        _register_tools(agent)
        _agents[output_type] = agent
    return _agents[output_type]

# Mock agent for demo without API key
class MockAgentResult:
    def __init__(self, output):
        self.output = output
    async def stream_text(self, delta=False):
        text = self.output if isinstance(self.output, str) else str(self.output)
        for chunk in [text[i:i+50] for i in range(0, len(text), 50)]:
            yield chunk

async def run_gxp_agent(prompt: str, output_type: str = "CFRAnswer"):
    if MOCK_MODE:
        # Return validated mock data without LLM call - still validates via Pydantic
        refs = await ecfr.search_ecfr(prompt)
        if "deviation" in prompt.lower() or "excursion" in prompt.lower():
            mock = DeviationDraft(
                classification="Minor",
                title="Deviation - Temperature Excursion",
                description=f"Freezer excursion observed: {prompt}. Investigated per 21 CFR 211.192.",
                cfr_refs=refs,
                impact_assessment="No impact to product quality based on stability data. Batch remains within spec.",
                immediate_action="Quarantine units, review monitoring data, notify QA.",
                requires_qa_approval=True
            )
            return mock
        else:
            mock = CFRAnswer(
                answer=f"Per your query '{prompt}', FDA requires thorough investigation of discrepancies. See citation.",
                cfr_refs=refs
            )
            return mock

    # Real LLM path
    result = await _get_agent(output_type).run(prompt)
    return result.output
