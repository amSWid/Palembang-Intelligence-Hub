from __future__ import annotations

from typing import Any

# =========================================================
# CENTRAL KNOWLEDGE CATALOG
# =========================================================
#
# ID 1–99   : local PDF/document sources
# ID 101+   : URL/live web sources
#
# Add every new PDF or URL here.
# Other modules will read this catalog automatically.
# =========================================================

KNOWLEDGE_CATALOG: dict[str, dict[str, Any]] = {
    "palembang_ebook": {
        "id": 1,
        "title": ("Palembang Tourism, History, " "Culture and Culinary Ebook"),
        "type": "pdf",
        "filename": "palembang01_ebook.pdf",
        "topics": [
            "general",
            "history",
            "culture",
            "food",
            "tourism",
            "geography",
            "attractions",
            "shopping",
        ],
        "authority": "local_reference",
        "enabled": True,
    },
    "palembang_gdp": {
        "id": 2,
        "title": ("Palembang GDP and " "Regional Economic Report"),
        "type": "pdf",
        "filename": "palembang02_gdp.pdf",
        "topics": [
            "economy",
            "gdp",
            "grdp",
            "agriculture",
            "production",
            "income",
            "employment",
            "trade",
        ],
        "authority": "government",
        "enabled": True,
    },
    "palembang_bi": {
        "id": 3,
        "title": ("Bank Indonesia Economic " "and Investment Report"),
        "type": "pdf",
        "filename": "palembang03_BankIndonesia.pdf",
        "topics": [
            "economy",
            "investment",
            "inflation",
            "growth",
            "business",
            "finance",
            "market",
        ],
        "authority": "government",
        "enabled": True,
    },
    "palembang_foodarticle": {
        "id": 4,
        "title": "Palembang Culinary Article",
        "type": "pdf",
        "filename": "palembang04_foodarticle.pdf",
        "topics": [
            "food",
            "culinary",
            "restaurant",
            "pempek",
            "tekwan",
            "mie celor",
        ],
        "authority": "reference_article",
        "enabled": True,
    },
    # =====================================================
    # URL EXAMPLE — KEEP DISABLED UNTIL TAVILY IS ADDED
    # =====================================================
    # "palembang_tourism_web": {
    #     "id": 101,
    #     "title": "Official Palembang Tourism Website",
    #     "type": "url",
    #     "url": "https://example.com",
    #     "topics": [
    #         "tourism",
    #         "events",
    #         "hotel",
    #         "restaurant",
    #         "attractions",
    #     ],
    #     "authority": "official",
    #     "enabled": False,
    # },
}


# =========================================================
# VALID VALUES
# =========================================================

VALID_SOURCE_TYPES = {
    "pdf",
    "url",
}

VALID_AUTHORITIES = {
    "official",
    "government",
    "academic",
    "local_reference",
    "reference_article",
    "news",
    "community",
    "blog",
}


# =========================================================
# CATALOG HELPERS
# =========================================================


def get_enabled_sources() -> dict[str, dict[str, Any]]:
    """
    Return all enabled knowledge sources.
    """

    return {
        source_key: source
        for source_key, source in KNOWLEDGE_CATALOG.items()
        if source.get("enabled", True)
    }


def get_sources_by_type(
    source_type: str,
    enabled_only: bool = True,
) -> dict[str, dict[str, Any]]:
    """
    Return PDF or URL sources.
    """

    source_type = source_type.strip().lower()

    sources = get_enabled_sources() if enabled_only else KNOWLEDGE_CATALOG

    return {
        source_key: source
        for source_key, source in sources.items()
        if source.get("type") == source_type
    }


def get_pdf_sources(
    enabled_only: bool = True,
) -> dict[str, dict[str, Any]]:
    """
    Return PDF sources.
    """

    return get_sources_by_type(
        source_type="pdf",
        enabled_only=enabled_only,
    )


def get_url_sources(
    enabled_only: bool = True,
) -> dict[str, dict[str, Any]]:
    """
    Return URL sources.
    """

    return get_sources_by_type(
        source_type="url",
        enabled_only=enabled_only,
    )


def get_source_by_key(
    source_key: str,
) -> dict[str, Any] | None:
    """
    Return one source using its catalog key.
    """

    return KNOWLEDGE_CATALOG.get(source_key)


def get_source_by_id(
    source_id: int | None,
) -> dict[str, Any] | None:
    """
    Return one source using its numeric ID.
    """

    if source_id is None:
        return None

    for source in KNOWLEDGE_CATALOG.values():
        try:
            catalog_id = int(source["id"])
        except (KeyError, TypeError, ValueError):
            continue

        if catalog_id == int(source_id):
            return source

    return None


def get_source_key_by_id(
    source_id: int | None,
) -> str | None:
    """
    Return catalog key using its numeric ID.
    """

    if source_id is None:
        return None

    for source_key, source in KNOWLEDGE_CATALOG.items():
        try:
            catalog_id = int(source["id"])
        except (KeyError, TypeError, ValueError):
            continue

        if catalog_id == int(source_id):
            return source_key

    return None


def get_source_id_map(
    source_type: str | None = None,
    enabled_only: bool = True,
) -> dict[str, int]:
    """
    Return:
        catalog key -> source ID
    """

    sources = get_enabled_sources() if enabled_only else KNOWLEDGE_CATALOG

    source_id_map: dict[str, int] = {}

    for source_key, source in sources.items():
        if source_type is not None and source.get("type") != source_type:
            continue

        source_id_map[source_key] = int(source["id"])

    return source_id_map


def get_source_name_to_id() -> dict[str, int]:
    """
    Create flexible source-name aliases for retrieval.

    Examples:
        palembang04_foodarticle.pdf -> 4
        palembang_foodarticle       -> 4
    """

    aliases: dict[str, int] = {}

    for source_key, source in get_enabled_sources().items():
        source_id = int(source["id"])

        aliases[source_key.lower()] = source_id

        filename = source.get("filename")

        if filename:
            filename_lower = str(filename).lower()

            aliases[filename_lower] = source_id
            aliases[filename_lower.removesuffix(".pdf")] = source_id

        title = source.get("title")

        if title:
            aliases[str(title).lower()] = source_id

    return aliases


def get_topics_for_source(
    source_key: str,
) -> list[str]:
    """
    Return topics for one source.
    """

    source = get_source_by_key(source_key)

    if not source:
        return []

    topics = source.get("topics", [])

    return [str(topic).strip().lower() for topic in topics if str(topic).strip()]


def validate_knowledge_catalog() -> list[str]:
    """
    Validate the complete catalog.

    Returns:
        List of validation errors.
    """

    errors: list[str] = []
    seen_ids: set[int] = set()

    for source_key, source in KNOWLEDGE_CATALOG.items():
        if not source_key.strip():
            errors.append("A knowledge source has an empty key.")

        source_id = source.get("id")

        try:
            source_id = int(source_id)
        except (TypeError, ValueError):
            errors.append(f"{source_key}: invalid source ID.")
            continue

        if source_id in seen_ids:
            errors.append(f"{source_key}: duplicate source ID {source_id}.")

        seen_ids.add(source_id)

        source_type = source.get("type")

        if source_type not in VALID_SOURCE_TYPES:
            errors.append(f"{source_key}: invalid type {source_type!r}.")

        if not source.get("title"):
            errors.append(f"{source_key}: missing title.")

        authority = source.get("authority")

        if authority not in VALID_AUTHORITIES:
            errors.append(f"{source_key}: invalid authority " f"{authority!r}.")

        topics = source.get("topics")

        if not isinstance(topics, list) or not topics:
            errors.append(f"{source_key}: topics must be " "a non-empty list.")

        if source_type == "pdf" and not source.get("filename"):
            errors.append(f"{source_key}: PDF filename is missing.")

        if source_type == "url" and not source.get("url"):
            errors.append(f"{source_key}: URL is missing.")

    return errors


def assert_valid_knowledge_catalog() -> None:
    """
    Raise an error when the catalog is invalid.
    """

    errors = validate_knowledge_catalog()

    if not errors:
        return

    formatted_errors = "\n".join(f"- {error}" for error in errors)

    raise ValueError("Knowledge catalog validation failed:\n" f"{formatted_errors}")
