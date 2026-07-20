from dataclasses import dataclass


@dataclass(frozen=True)
class AgentSelection:
    """
    Result of question classification.
    """

    category: str
    source_ids: tuple[int, ...]
    search_query: str


CATEGORY_SOURCE_MAP = {
    "food": (4, 1),
    "culture": (1, 4),
    "history": (1,),
    "economy": (2, 3),
    "investment": (3, 2),
    "general": (1, 2, 3, 4),
}


CATEGORY_WEIGHTS = {
    "food": {
        "pempek": 10,
        "tekwan": 10,
        "mie celor": 10,
        "model": 8,
        "laksan": 8,
        "celimpungan": 8,
        "burgo": 8,
        "restaurant": 7,
        "restoran": 7,
        "where to eat": 7,
        "tempat makan": 7,
        "culinary": 5,
        "cuisine": 5,
        "dish": 5,
        "meal": 4,
        "makanan": 3,
        "kuliner": 5,
        "food": 2,
        "eat": 3,
    },
    "culture": {
        "culture": 6,
        "cultural": 6,
        "tradition": 6,
        "traditional": 4,
        "custom": 5,
        "dance": 6,
        "music": 6,
        "song": 5,
        "art": 4,
        "clothing": 5,
        "language": 5,
        "adat": 6,
        "budaya": 6,
        "musik": 6,
        "tarian": 6,
        "kesenian": 6,
    },
    "history": {
        "history": 7,
        "historical": 7,
        "legend": 7,
        "kingdom": 7,
        "srivijaya": 10,
        "sriwijaya": 10,
        "heritage": 6,
        "ampera": 6,
        "musi river": 7,
        "sungai musi": 7,
        "geography": 6,
        "oldest city": 8,
        "sejarah": 7,
        "legenda": 7,
        "kerajaan": 7,
        "geografi": 6,
    },
    "economy": {
        "economy": 7,
        "economic": 7,
        "gdp": 10,
        "grdp": 10,
        "pdrb": 10,
        "agriculture": 9,
        "agricultural": 9,
        "harvest": 8,
        "production": 7,
        "commodity": 7,
        "income": 7,
        "inflation": 8,
        "employment": 7,
        "trade": 6,
        "industry": 7,
        "processing": 6,
        "food processing": 10,
        "agroindustry": 10,
        "agro-industry": 10,
        "ekonomi": 7,
        "pertanian": 9,
        "panen": 8,
        "produksi": 7,
        "komoditas": 7,
        "pendapatan": 7,
        "industri": 7,
        "pengolahan makanan": 10,
    },
    "investment": {
        "investment": 10,
        "investor": 9,
        "opportunity": 8,
        "opportunities": 8,
        "business potential": 10,
        "business opportunity": 10,
        "growth potential": 9,
        "market opportunity": 9,
        "recommended sector": 9,
        "manufacturing": 8,
        "infrastructure": 8,
        "logistics": 8,
        "digital economy": 8,
        "investment opportunity": 10,
        "sector opportunity": 9,
        "investasi": 10,
        "peluang usaha": 10,
        "peluang bisnis": 10,
        "potensi bisnis": 9,
        "sektor potensial": 9,
    },
}


CATEGORY_PRIORITY = {
    "investment": 5,
    "economy": 4,
    "food": 3,
    "history": 2,
    "culture": 1,
    "general": 0,
}


def normalise_question(question: str) -> str:
    """
    Normalise a question before classification.
    """

    return " ".join(question.lower().strip().split())


def calculate_category_score(
    question: str,
    category: str,
) -> int:
    """
    Calculate weighted keyword score for one category.
    """

    weighted_keywords = CATEGORY_WEIGHTS.get(
        category,
        {},
    )

    score = 0

    for keyword, weight in weighted_keywords.items():
        if keyword in question:
            score += weight

    return score


def contains_any(
    question: str,
    phrases: tuple[str, ...],
) -> bool:
    """
    Return True when at least one phrase is found.
    """

    return any(phrase in question for phrase in phrases)


def build_search_query(
    question: str,
    category: str,
) -> str:
    """
    Build a focused semantic search query.
    """

    query_prefixes = {
        "food": (
            "Palembang traditional food culinary dish restaurant "
            "ingredients preparation cultural meaning"
        ),
        "culture": (
            "Palembang culture traditions arts music dance language "
            "customs cultural identity"
        ),
        "history": (
            "Palembang history heritage Srivijaya legends geography "
            "Musi River historical development"
        ),
        "economy": (
            "Palembang economy GDP GRDP agriculture production "
            "commodity industry income inflation employment"
        ),
        "investment": (
            "Palembang investment opportunities growth sectors "
            "market potential industry infrastructure logistics"
        ),
        "general": (
            "Palembang local knowledge tourism economy culture "
            "history food investment"
        ),
    }

    prefix = query_prefixes.get(
        category,
        query_prefixes["general"],
    )

    return f"{prefix}. User question: {question}"


def select_agent(
    question: str,
) -> AgentSelection:
    """
    Select the best category and source order.

    Uses weighted matching so broad words such as "food"
    do not override stronger economic or investment intent.
    """

    cleaned_question = normalise_question(question)

    if not cleaned_question:
        return AgentSelection(
            category="general",
            source_ids=CATEGORY_SOURCE_MAP["general"],
            search_query="Palembang local knowledge",
        )

    food_article_phrases = (
        "food article",
        "culinary article",
        "article about food",
        "summarize the food article",
        "summarise the food article",
        "summary of the food article",
        "artikel makanan",
        "artikel kuliner",
        "ringkas artikel makanan",
        "ringkas artikel kuliner",
        "rangkum artikel makanan",
        "rangkum artikel kuliner",
    )

    if contains_any(
        cleaned_question,
        food_article_phrases,
    ):
        return AgentSelection(
            category="food",
            source_ids=(4,),
            search_query=(
                "Palembang culinary article traditional foods "
                "culinary identity history dishes preservation"
            ),
        )

    food_processing_phrases = (
        "food processing",
        "food industry",
        "agricultural processing",
        "agriculture processing",
        "agroindustry",
        "agro-industry",
        "pengolahan makanan",
        "industri makanan",
        "industri pangan",
        "agroindustri",
    )

    investment_phrases = (
        "investment opportunity",
        "investment opportunities",
        "business opportunity",
        "business opportunities",
        "market opportunity",
        "growth potential",
        "recommended sector",
        "peluang investasi",
        "peluang usaha",
        "peluang bisnis",
        "potensi bisnis",
    )

    agriculture_phrases = (
        "agriculture",
        "agricultural",
        "harvest",
        "commodity",
        "crop",
        "farming",
        "pertanian",
        "panen",
        "komoditas",
    )

    if contains_any(cleaned_question, food_processing_phrases) and contains_any(
        cleaned_question, investment_phrases
    ):
        return AgentSelection(
            category="investment",
            source_ids=(3, 2),
            search_query=(
                "Palembang agriculture food processing investment "
                "opportunities agroindustry market potential "
                f"user question: {cleaned_question}"
            ),
        )

    if contains_any(cleaned_question, agriculture_phrases) and contains_any(
        cleaned_question, investment_phrases
    ):
        return AgentSelection(
            category="investment",
            source_ids=(3, 2),
            search_query=(
                "Palembang agriculture investment opportunities "
                "production commodities growth sectors "
                f"user question: {cleaned_question}"
            ),
        )

    category_scores = {
        category: calculate_category_score(
            cleaned_question,
            category,
        )
        for category in CATEGORY_WEIGHTS
    }

    highest_score = max(
        category_scores.values(),
        default=0,
    )

    if highest_score <= 0:
        selected_category = "general"
    else:
        matching_categories = [
            category
            for category, score in category_scores.items()
            if score == highest_score
        ]

        selected_category = max(
            matching_categories,
            key=lambda category: CATEGORY_PRIORITY.get(
                category,
                0,
            ),
        )

    return AgentSelection(
        category=selected_category,
        source_ids=CATEGORY_SOURCE_MAP[selected_category],
        search_query=build_search_query(
            cleaned_question,
            selected_category,
        ),
    )


def get_category_instruction(
    category: str,
) -> str:
    """
    Return a strict instruction for the selected agent.
    """

    instructions = {
        "food": (
            "Answer only about the requested Palembang food, "
            "its characteristics, ingredients, preparation, cultural "
            "meaning or documented restaurant information. A question "
            "about the food industry or food processing is economic, "
            "not a request for culinary dish information."
        ),
        "culture": (
            "Answer about Palembang traditions, arts, music, language, "
            "customs or cultural identity. Keep the answer focused on "
            "the cultural subject requested."
        ),
        "history": (
            "Answer about Palembang history, legends, heritage or "
            "geography. Distinguish documented history from legend "
            "when the source makes that distinction."
        ),
        "economy": (
            "Answer using documented economic information such as GDP, "
            "agriculture, production, commodities, income, inflation, "
            "employment, industry or food processing. Do not invent "
            "statistics or unsupported opportunities."
        ),
        "investment": (
            "Answer using documented growth, market conditions, sector "
            "performance and investment opportunities. Combine economic "
            "evidence from source 2 with investment context from source 3 "
            "when relevant. Clearly separate source facts from analytical "
            "recommendations."
        ),
        "general": (
            "Answer the exact Palembang question using only relevant "
            "retrieved information. Avoid unrelated details and do not "
            "force an answer when the sources are insufficient."
        ),
    }

    return instructions.get(
        category,
        instructions["general"],
    )
