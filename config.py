from pathlib import Path

from core.knowledge_catalog import (
    assert_valid_knowledge_catalog,
    get_pdf_sources,
    get_source_id_map,
    get_url_sources,
)

# =========================================================
# BASE DIRECTORIES
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
RAW_PDF_DIR = DATA_DIR / "raw_pdf"
CLEANED_DIR = DATA_DIR / "cleaned"

ASSETS_DIR = BASE_DIR / "assets"
IMAGE_DIR = ASSETS_DIR / "images"
FOOD_IMAGE_DIR = ASSETS_DIR / "food"
MUSIC_DIR = ASSETS_DIR / "music"

CHROMA_DIR = BASE_DIR / "chroma_db"


# =========================================================
# VALIDATE KNOWLEDGE CATALOG
# =========================================================

assert_valid_knowledge_catalog()


# =========================================================
# KNOWLEDGE SOURCES
# =========================================================

PDF_SOURCE_CONFIG = get_pdf_sources(enabled_only=True)

URL_SOURCE_CONFIG = get_url_sources(enabled_only=True)


PDF_FILES = {
    source_key: RAW_PDF_DIR / str(source["filename"])
    for source_key, source in PDF_SOURCE_CONFIG.items()
}


OFFICIAL_URLS = {
    source_key: str(source["url"]) for source_key, source in URL_SOURCE_CONFIG.items()
}


SOURCE_ID_MAP = get_source_id_map(
    source_type="pdf",
    enabled_only=True,
)


# =========================================================
# CLEANING AND VECTOR DATABASE
# =========================================================

CLEANED_TEXT_FILE = CLEANED_DIR / "palembang_cleaned.txt"

EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 120

COLLECTION_NAME = "palembang_intelligence"


# =========================================================
# RETRIEVAL SETTINGS
# =========================================================

# Number of candidates retrieved from each allowed source.
RETRIEVAL_CANDIDATES_PER_SOURCE = 6


# =========================================================
# LANGUAGE MODEL
# =========================================================

LLM_MODEL = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0.2
