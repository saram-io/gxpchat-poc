from ..schemas import WarningLetterRef

MOCK_WARNINGS = [
    {
        "fei_number": "300123456",
        "company": "Example Pharma LLC",
        "issue_date": "2023-08-15",
        "observation": "Failure to thoroughly investigate unexplained discrepancies per 21 CFR 211.192",
        "fda_url": "https://www.fda.gov/ICECI/EnforcementActions/WarningLetters/default.htm"
    }
]

async def search_warning_letters(keyword: str) -> list[WarningLetterRef]:
    return [WarningLetterRef(**w) for w in MOCK_WARNINGS if keyword.lower() in w["observation"].lower() or True]
