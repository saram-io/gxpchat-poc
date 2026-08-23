from ..schemas import CFRReference

async def search_ich(query: str) -> list[CFRReference]:
    q = query.lower()
    if "q10" in q:
        return [CFRReference(
            title=0, part=10, section="ICH Q10",
            text_snippet="ICH Q10 describes Pharmaceutical Quality System with 6 elements: process performance, CAPA, change management, management review...",
            url="https://www.ich.org/page/q10",
            version_date="2024-01-01"
        )]
    return []
