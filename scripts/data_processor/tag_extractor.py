# scripts/data_processor/scripts/tag_extractor.py

TAG_RULES = {
    "IPO": [
        "ipo", "drhp", "draft red herring",
        "price band", "issue opens", "issue closes",
        "anchor investor", "public issue"
    ],

    "RESULTS": [
        "q1 results", "q2 results", "q3 results", "q4 results",
        "earnings", "net profit", "profit rose", "profit fell",
        "revenue grew", "revenue declined"
    ],

    "CORPORATE_ACTION": [
        "dividend", "buyback", "share buyback",
        "stock split", "bonus issue"
    ],

    "DEAL_MA": [
        "acquire", "acquisition", "merger",
        "stake buy", "stake sale", "strategic investment"
    ],

    "ORDER_CONTRACT": [
        "order", "contract", "bagged order",
        "wins order", "order worth", "order value"
    ],

    "GUIDANCE": [
        "guidance", "outlook", "expects", "forecast",
        "management said", "company expects"
    ],

    "REGULATORY": [
        "sebi", "rbi", "government approval",
        "regulatory approval", "nod", "clearance"
    ]
}


def extract_tags(title: str, content: str):
    """
    Rule-based event tag extraction.
    Returns list of tags or None.
    """

    text = f"{title} {content}".lower()
    matched_tags = set()

    for tag, keywords in TAG_RULES.items():
        for kw in keywords:
            if kw in text:
                matched_tags.add(tag)
                break

    return list(matched_tags) if matched_tags else None
