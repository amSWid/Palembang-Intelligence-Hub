from dataclasses import dataclass


@dataclass(frozen=True)
class AgentSelection:
    """
    Result of question classification.
    """

    category: str
    source_ids: tuple[int, ...]
    search_query: str


# =========================================================
# SOURCE ACCESS
# =========================================================

# Every normal Palembang question may search all references.
# Retrieval will decide which chunks are truly relevant.
ALL_SOURCE_IDS = (1, 2, 3, 4)


# =========================================================
# PHRASE GROUPS
# =========================================================

SUMMARY_PHRASES = (
    "summarize",
    "summarise",
    "summary",
    "overview",
    "main findings",
    "ringkas",
    "rangkum",
)


ARTICLE_PHRASES = (
    "food article",
    "culinary article",
    "artikel makanan",
    "artikel kuliner",
)


INVESTMENT_INTENT_PHRASES = (
    "investment",
    "invest",
    "investor",
    "opportunity",
    "opportunities",
    "business potential",
    "market potential",
    "growth potential",
    "promising sector",
    "recommended sector",
    "recommend",
    "recommendation",
    "business prospect",
    "investment prospect",
    "worth investing",
    "should i invest",
    "where to invest",
    "peluang",
    "potensi bisnis",
    "potensi usaha",
    "sektor potensial",
    "sektor menjanjikan",
    "prospek bisnis",
    "rekomendasi investasi",
    "layak investasi",
)


FOOD_PHRASES = (
    "pempek",
    "tekwan",
    "mie celor",
    "model",
    "laksan",
    "celimpungan",
    "burgo",
    "pindang",
    "cuko",
    "restaurant",
    "where to eat",
    "traditional food",
    "local food",
    "culinary",
    "cuisine",
    "dish",
    "makanan",
    "kuliner",
    "restoran",
    "tempat makan",
)


FOOD_INDUSTRY_PHRASES = (
    "food processing",
    "food industry",
    "food manufacturing",
    "agroindustry",
    "agro-industry",
    "processed food",
    "pengolahan makanan",
    "pengolahan pangan",
    "industri makanan",
    "industri pangan",
    "agroindustri",
)


HISTORY_PHRASES = (
    "history",
    "historical",
    "legend",
    "kingdom",
    "srivijaya",
    "sriwijaya",
    "heritage",
    "ampera",
    "musi river",
    "geography",
    "inscription",
    "oldest city",
    "sejarah",
    "legenda",
    "kerajaan",
    "warisan",
    "sungai musi",
    "geografi",
    "prasasti",
)


CULTURE_PHRASES = (
    "culture",
    "cultural",
    "tradition",
    "custom",
    "dance",
    "music",
    "song",
    "art",
    "traditional clothing",
    "language",
    "adat",
    "budaya",
    "tradisi",
    "tarian",
    "musik",
    "kesenian",
    "pakaian adat",
    "bahasa",
)


ECONOMY_PHRASES = (
    "economy",
    "economic",
    "gdp",
    "grdp",
    "pdrb",
    "economic growth",
    "growth rate",
    "sector contribution",
    "contribution",
    "income",
    "inflation",
    "employment",
    "unemployment",
    "production",
    "harvest",
    "commodity",
    "agriculture",
    "agricultural",
    "farming",
    "industry",
    "manufacturing",
    "trade",
    "ekonomi",
    "pertumbuhan ekonomi",
    "kontribusi",
    "pendapatan",
    "inflasi",
    "tenaga kerja",
    "produksi",
    "panen",
    "komoditas",
    "pertanian",
    "industri",
)


# =========================================================
# TEXT HELPERS
# =========================================================


def normalise_question(question: str) -> str:
    """
    Normalise a question before classification.
    """

    return " ".join(question.lower().strip().split())


def contains_phrase(
    text: str,
    phrase: str,
) -> bool:
    """
    Match a complete word or multi-word phrase.
    """

    phrase = phrase.lower().strip()

    if not phrase:
        return False

    if " " in phrase:
        return phrase in text

    padded_text = f" {text} "

    return f" {phrase} " in padded_text


def contains_any(
    text: str,
    phrases: tuple[str, ...],
) -> bool:
    """
    Return True when any phrase exists in the text.
    """

    return any(contains_phrase(text, phrase) for phrase in phrases)


# =========================================================
# CLASSIFICATION
# =========================================================


def is_food_article_summary(
    question: str,
) -> bool:
    """
    Detect a request specifically asking for
    a summary of Reference 4.
    """

    return contains_any(question, SUMMARY_PHRASES) and contains_any(
        question, ARTICLE_PHRASES
    )


def select_category(
    question: str,
) -> str:
    """
    Select the question category.

    Category controls the prompt only.
    It no longer blocks access to references.
    """

    if contains_any(
        question,
        INVESTMENT_INTENT_PHRASES,
    ):
        return "investment"

    if contains_any(
        question,
        FOOD_INDUSTRY_PHRASES,
    ):
        return "economy"

    if contains_any(
        question,
        FOOD_PHRASES,
    ):
        return "food"

    if contains_any(
        question,
        HISTORY_PHRASES,
    ):
        return "history"

    if contains_any(
        question,
        CULTURE_PHRASES,
    ):
        return "culture"

    if contains_any(
        question,
        ECONOMY_PHRASES,
    ):
        return "economy"

    return "general"


# =========================================================
# MAIN SELECTOR
# =========================================================


def select_agent(
    question: str,
) -> AgentSelection:
    """
    Classify the question and provide source access.

    Normal questions:
        search References 1, 2, 3 and 4.

    Explicit culinary article summaries:
        summarize Reference 4 only.
    """

    cleaned_question = normalise_question(question)

    if not cleaned_question:
        return AgentSelection(
            category="general",
            source_ids=ALL_SOURCE_IDS,
            search_query="Palembang",
        )

    if is_food_article_summary(cleaned_question):
        return AgentSelection(
            category="food",
            source_ids=(4,),
            search_query=cleaned_question,
        )

    category = select_category(cleaned_question)

    return AgentSelection(
        category=category,
        source_ids=ALL_SOURCE_IDS,
        search_query=cleaned_question,
    )


# =========================================================
# PROMPT INSTRUCTIONS
# =========================================================


def get_category_instruction(
    category: str,
) -> str:
    """
    Return strict instructions for the selected category.
    """

    instructions = {
        "food": (
            "Answer only about the requested Palembang dish. "
            "Use evidence directly connected to that dish. "
            "Do not mix information about another dish unless the "
            "question explicitly requests a comparison. "
            "Restaurant information may be included only when it is "
            "documented in the retrieved evidence."
        ),
        "culture": (
            "Answer only about the requested Palembang tradition, "
            "art, music, dance, language, custom or cultural identity. "
            "Do not introduce unrelated historical or economic claims."
        ),
        "history": (
            "Answer only about the requested Palembang historical, "
            "heritage, legendary or geographical subject. "
            "Distinguish documented history from legend."
        ),
        "economy": (
            "Answer using documented economic evidence such as GDP, "
            "production, agriculture, commodities, income, inflation, "
            "employment or sector performance. "
            "Do not invent statistics or opportunities."
        ),
        "investment": (
            "Evaluate the requested subject using documented economic "
            "and investment evidence. Clearly separate source facts, "
            "analysis and recommendations. Do not claim that a sector "
            "is attractive without supporting evidence."
        ),
        "general": (
            "Answer the exact Palembang question using only directly "
            "relevant retrieved evidence. If the sources do not contain "
            "the requested information, clearly say that the local "
            "knowledge base does not provide enough evidence."
        ),
    }

    return instructions.get(
        category,
        instructions["general"],
    )
