import httpx
from ..schemas import CFRReference

# Mock eCFR client - replace with real eCFR API: https://www.ecfr.gov/developers/documentation/api/v1
MOCK_CFR_DB = {
    "211.192": {
        "title": 21, "part": 211, "section": "211.192",
        "text_snippet": "Any unexplained discrepancy shall be thoroughly investigated, whether or not the batch has already been distributed.",
        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-211/subpart-J/section-211.192"
    },
    "211.194": {
        "title": 21, "part": 211, "section": "211.194",
        "text_snippet": "Laboratory records shall include complete data derived from all tests necessary to assure compliance.",
        "url": "https://www.ecfr.gov/current/title-21/part-211/section-211.194"
    },
    "annex1": {
        "title": 21, "part": 0, "section": "Annex 1",
        "text_snippet": "Contamination Control Strategy (CCS) shall be implemented across facility to assess effectiveness of controls.",
        "url": "https://health.ec.europa.eu/medicinal-products/eudralex/eudralex-volume-4_en"
    }
}

async def search_ecfr(query: str) -> list[CFRReference]:
    q = query.lower()
    results = []
    if "211.192" in q or "discrepancy" in q or "investigation" in q:
        results.append(CFRReference(**MOCK_CFR_DB["211.192"]))
    if "lab" in q or "211.194" in q:
        results.append(CFRReference(**MOCK_CFR_DB["211.194"]))
    if "annex 1" in q or "contamination" in q or "ccs" in q:
        results.append(CFRReference(**MOCK_CFR_DB["annex1"]))
    if not results:
        # default fallback - always return at least one for validation demo
        results.append(CFRReference(**MOCK_CFR_DB["211.192"]))
    return results
