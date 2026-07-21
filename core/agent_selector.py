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
# SOURCE ROUTING
# =========================================================

CATEGORY_SOURCE_MAP = {
    "food": (4, 1),
    "culture": (1, 4),
    "history": (1,),
    "economy": (2, 3),
    "investment": (3, 2),
    "general": (1, 2, 3, 4),
}


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
    Match a complete word or a multi-word phrase.
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
    Detect a request to summarize Source 4.
    """

    return contains_any(question, SUMMARY_PHRASES) and contains_any(
        question, ARTICLE_PHRASES
    )


def select_category(
    question: str,
) -> str:
    """
    Select a category using a small set of intent rules.

    Intent has priority over subject words.

    Examples:

        agriculture contribution to GDP
        -> economy

        agriculture opportunities
        -> investment

        food processing output
        -> economy

        food processing opportunities
        -> investment
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
    Select category and allowed sources.

    The original cleaned question is used directly as the
    semantic retrieval query. No long query expansion is added.
    """

    cleaned_question = normalise_question(question)

    if not cleaned_question:
        return AgentSelection(
            category="general",
            source_ids=CATEGORY_SOURCE_MAP["general"],
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
        source_ids=CATEGORY_SOURCE_MAP[category],
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
            "Answer only about the requested Palembang food, "
            "its characteristics, ingredients, preparation, origin, "
            "cultural meaning or documented restaurant information. "
            "Food processing and the food industry are economic topics."
        ),
        "culture": (
            "Answer about Palembang traditions, arts, music, dance, "
            "language, customs or cultural identity. Keep the response "
            "focused on the requested cultural subject."
        ),
        "history": (
            "Answer about Palembang history, legends, heritage or "
            "geography. Distinguish documented history from legend "
            "when the source makes that distinction."
        ),
        "economy": (
            "Answer using documented economic evidence such as GDP, "
            "production, agriculture, commodities, income, inflation, "
            "employment or sector performance. Do not invent statistics "
            "or unsupported business opportunities."
        ),
        "investment": (
            "Evaluate the requested subject using documented economic "
            "and investment evidence. A sector mentioned by the user is "
            "a subject for analysis, not automatic proof that it is a "
            "good investment. Clearly separate source facts, analysis "
            "and recommendations."
        ),
        "general": (
            "Answer the exact Palembang question using only relevant "
            "retrieved information. State clearly when the available "
            "sources are insufficient."
        ),
    }

    return instructions.get(
        category,
        instructions["general"],
    )
