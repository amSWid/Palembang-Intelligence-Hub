from __future__ import annotations

from pathlib import Path
import shutil
import sys
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


import chromadb
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)
from sentence_transformers import (
    SentenceTransformer,
)

from config import (
    CHROMA_DIR,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
)
from core.knowledge_catalog import (
    assert_valid_knowledge_catalog,
    get_source_by_key,
)
from core.pdf_loader import (
    load_all_pdfs,
)

BATCH_SIZE = 64


# =========================================================
# CATEGORY HELPERS
# =========================================================

CATEGORY_KEYWORDS = {
    "food": {
        "pempek",
        "tekwan",
        "mie celor",
        "laksan",
        "burgo",
        "celimpungan",
        "kuliner",
        "makanan",
        "restaurant",
        "restoran",
        "food",
        "culinary",
    },
    "culture": {
        "culture",
        "budaya",
        "tradition",
        "tradisi",
        "music",
        "musik",
        "dance",
        "tarian",
        "songket",
        "custom",
        "adat",
    },
    "history": {
        "history",
        "sejarah",
        "sriwijaya",
        "srivijaya",
        "ampera",
        "heritage",
        "warisan",
        "legend",
        "legenda",
        "musi river",
        "sungai musi",
    },
    "economy": {
        "economy",
        "ekonomi",
        "gdp",
        "grdp",
        "pdrb",
        "agriculture",
        "pertanian",
        "production",
        "produksi",
        "income",
        "pendapatan",
        "inflation",
        "inflasi",
    },
    "investment": {
        "investment",
        "investasi",
        "investor",
        "opportunity",
        "opportunities",
        "peluang",
        "growth",
        "pertumbuhan",
        "business",
        "bisnis",
        "infrastructure",
        "logistics",
    },
    "tourism": {
        "tourism",
        "wisata",
        "hotel",
        "attraction",
        "destination",
        "destinasi",
        "museum",
        "shopping",
        "transportation",
    },
}


def normalise_text(
    text: str,
) -> str:
    """
    Normalise extracted PDF text.
    """

    return " ".join(str(text).replace("\x00", " ").split())


def classify_chunk(
    text: str,
    source_key: str,
) -> str:
    """
    Assign one primary category to a chunk.

    The complete multi-topic list is still
    stored separately in metadata.
    """

    cleaned_text = normalise_text(text).lower()

    scores = {
        category: sum(1 for keyword in keywords if keyword in cleaned_text)
        for category, keywords in CATEGORY_KEYWORDS.items()
    }

    highest_score = max(
        scores.values(),
        default=0,
    )

    if highest_score > 0:
        priority_order = [
            "food",
            "investment",
            "economy",
            "culture",
            "history",
            "tourism",
        ]

        for category in priority_order:
            if scores.get(category) == highest_score:
                return category

    source = get_source_by_key(source_key)

    if source:
        topics = source.get(
            "topics",
            [],
        )

        for category in (
            "food",
            "investment",
            "economy",
            "culture",
            "history",
            "tourism",
        ):
            if category in topics:
                return category

    return "general"


# =========================================================
# CHUNK PREPARATION
# =========================================================


def create_text_splitter():
    """
    Create the document text splitter.
    """

    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )


def prepare_chunks():
    """
    Load, clean and split every configured PDF.
    """

    source_documents = load_all_pdfs()

    splitter = create_text_splitter()

    split_documents = splitter.split_documents(source_documents)

    prepared_chunks = []

    source_chunk_counts: dict[str, int] = {}

    for global_index, document in enumerate(split_documents):
        cleaned_text = normalise_text(document.page_content)

        if len(cleaned_text) < 40:
            continue

        metadata: dict[str, Any] = dict(document.metadata)

        source_key = str(
            metadata.get(
                "source_key",
                metadata.get(
                    "source_name",
                    "unknown",
                ),
            )
        )

        source_chunk_index = source_chunk_counts.get(
            source_key,
            0,
        )

        source_chunk_counts[source_key] = source_chunk_index + 1

        source_config = get_source_by_key(source_key)

        if source_config:
            topics = source_config.get(
                "topics",
                [],
            )

            metadata["topics"] = ",".join(str(topic) for topic in topics)

            metadata["authority"] = str(
                source_config.get(
                    "authority",
                    "unknown",
                )
            )

            metadata["source_title"] = str(
                source_config.get(
                    "title",
                    source_key,
                )
            )

            metadata["source_id"] = int(source_config["id"])

        metadata.update(
            {
                "chunk_index": (source_chunk_index),
                "global_chunk_index": (global_index),
                "category": classify_chunk(
                    text=cleaned_text,
                    source_key=source_key,
                ),
            }
        )

        prepared_chunks.append(
            {
                "id": (f"{source_key}_" f"{source_chunk_index:06d}"),
                "text": cleaned_text,
                "metadata": metadata,
            }
        )

    return prepared_chunks


# =========================================================
# CHROMA BUILD
# =========================================================


def reset_chroma_collection(
    client: chromadb.PersistentClient,
):
    """
    Delete the old collection and create a new one.
    """

    existing_names = {collection.name for collection in client.list_collections()}

    if COLLECTION_NAME in existing_names:
        print("Deleting old collection: " f"{COLLECTION_NAME}")

        client.delete_collection(name=COLLECTION_NAME)

    return client.create_collection(
        name=COLLECTION_NAME,
        metadata={
            "hnsw:space": "cosine",
        },
    )


def build_chroma_database():
    """
    Build the complete persistent Chroma database.
    """

    print("=" * 70)
    print("BUILDING PALEMBANG CHROMA DATABASE")
    print("=" * 70)

    assert_valid_knowledge_catalog()

    chunks = prepare_chunks()

    print(f"Total chunks prepared: {len(chunks)}")

    if not chunks:
        raise RuntimeError("No valid chunks were prepared.")

    print("Loading embedding model:")
    print(EMBEDDING_MODEL)

    embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    CHROMA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    collection = reset_chroma_collection(client)

    total_batches = (len(chunks) + BATCH_SIZE - 1) // BATCH_SIZE

    for batch_number, batch_start in enumerate(
        range(
            0,
            len(chunks),
            BATCH_SIZE,
        ),
        start=1,
    ):
        batch = chunks[batch_start : batch_start + BATCH_SIZE]

        texts = [chunk["text"] for chunk in batch]

        embeddings = (
            embedding_model.encode(
                texts,
                normalize_embeddings=True,
                show_progress_bar=False,
            )
            .astype(float)
            .tolist()
        )

        collection.add(
            ids=[chunk["id"] for chunk in batch],
            documents=texts,
            metadatas=[chunk["metadata"] for chunk in batch],
            embeddings=embeddings,
        )

        print(f"Batch {batch_number}/" f"{total_batches} completed")

    print("=" * 70)
    print("CHROMA BUILD COMPLETED")
    print(f"Collection : {collection.name}")
    print(f"Documents  : {collection.count()}")
    print(f"Location   : {CHROMA_DIR}")
    print("=" * 70)


if __name__ == "__main__":
    build_chroma_database()
