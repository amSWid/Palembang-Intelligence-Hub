from dataclasses import dataclass
from typing import Any

import chromadb
import streamlit as st
from sentence_transformers import SentenceTransformer

from config import (
    CHROMA_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    RETRIEVAL_CANDIDATES_PER_SOURCE,
)
from core.knowledge_catalog import (
    get_source_by_id,
    get_source_name_to_id,
)


@dataclass
class RetrievedDocument:
    """
    One document retrieved from Chroma.
    """

    text: str
    metadata: dict[str, Any]
    distance: float | None
    source_id: int | None


SOURCE_NAME_TO_ID = get_source_name_to_id()


@st.cache_resource(show_spinner=False)
def load_embedding_model() -> SentenceTransformer:
    """
    Load the embedding model once.
    """

    return SentenceTransformer(EMBEDDING_MODEL)


def get_chroma_client():
    """
    Open a fresh local Chroma client.

    The client is intentionally not cached because the collection
    can be deleted and rebuilt while developing the project.
    """

    if not CHROMA_DIR.exists():
        raise FileNotFoundError(f"Chroma directory was not found: {CHROMA_DIR}")

    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def get_collection():
    """
    Return the current configured Chroma collection.
    """

    client = get_chroma_client()

    available_collections = client.list_collections()

    available_names = {collection.name for collection in available_collections}

    if COLLECTION_NAME not in available_names:
        names_text = ", ".join(sorted(available_names)) if available_names else "none"

        raise ValueError(
            f'Collection "{COLLECTION_NAME}" was not found. '
            f"Available collections: {names_text}"
        )

    return client.get_collection(name=COLLECTION_NAME)


def infer_source_id(
    metadata: dict[str, Any],
) -> int | None:
    """
    Infer source ID from document metadata.
    """

    direct_source_id = metadata.get("source_id")

    if direct_source_id is not None:
        try:
            source_id = int(direct_source_id)

            if get_source_by_id(source_id):
                return source_id

        except (TypeError, ValueError):
            pass

    metadata_values = " ".join(
        str(value).lower() for value in metadata.values() if value is not None
    )

    for alias, source_id in SOURCE_NAME_TO_ID.items():
        if alias.lower() in metadata_values:
            return source_id

    return None


def convert_query_results(
    results: dict[str, Any],
) -> list[RetrievedDocument]:
    """
    Convert raw Chroma results into RetrievedDocument objects.
    """

    documents = (
        results.get(
            "documents",
            [[]],
        )[0]
        or []
    )

    metadatas = (
        results.get(
            "metadatas",
            [[]],
        )[0]
        or []
    )

    distances = (
        results.get(
            "distances",
            [[]],
        )[0]
        or []
    )

    retrieved_documents: list[RetrievedDocument] = []

    for index, document_text in enumerate(documents):
        metadata = (
            metadatas[index] if index < len(metadatas) and metadatas[index] else {}
        )

        raw_distance = distances[index] if index < len(distances) else None

        try:
            distance = float(raw_distance) if raw_distance is not None else None
        except (TypeError, ValueError):
            distance = None

        retrieved_documents.append(
            RetrievedDocument(
                text=document_text or "",
                metadata=metadata,
                distance=distance,
                source_id=infer_source_id(metadata),
            )
        )

    return retrieved_documents


def query_collection(
    question: str,
    top_k: int = 6,
    source_id: int | None = None,
) -> list[RetrievedDocument]:
    """
    Search Chroma using semantic similarity.

    When source_id is provided, the search is restricted
    directly to that source inside Chroma.
    """

    cleaned_question = question.strip()

    if not cleaned_question:
        return []

    embedding_model = load_embedding_model()

    question_embedding = (
        embedding_model.encode(
            cleaned_question,
            normalize_embeddings=True,
        )
        .astype(float)
        .tolist()
    )

    collection = get_collection()

    available_count = collection.count()

    if available_count == 0:
        return []

    result_count = min(
        top_k,
        available_count,
    )

    query_arguments: dict[str, Any] = {
        "query_embeddings": [question_embedding],
        "n_results": result_count,
        "include": [
            "documents",
            "metadatas",
            "distances",
        ],
    }

    if source_id is not None:
        query_arguments["where"] = {"source_id": int(source_id)}

    results = collection.query(**query_arguments)

    return convert_query_results(results)


def document_sort_key(
    document: RetrievedDocument,
) -> float:
    """
    Return a sortable numeric distance.

    Documents without a distance are placed last.
    """

    if document.distance is None:
        return float("inf")

    return document.distance


def remove_duplicate_retrievals(
    documents: list[RetrievedDocument],
) -> list[RetrievedDocument]:
    """
    Remove duplicated retrieval candidates.

    This protects the final context from repeated chunks
    returned from overlapping source content.
    """

    unique_documents: list[RetrievedDocument] = []
    seen_keys: set[str] = set()

    for document in documents:
        normalised_text = " ".join(document.text.lower().split())

        comparison_key = normalised_text[:500]

        if not comparison_key:
            continue

        if comparison_key in seen_keys:
            continue

        seen_keys.add(comparison_key)
        unique_documents.append(document)

    return unique_documents


def select_balanced_documents(
    candidates_by_source: dict[
        int,
        list[RetrievedDocument],
    ],
    source_priority: tuple[int, ...],
    top_k: int,
) -> list[RetrievedDocument]:
    """
    Select high-quality documents while preserving
    evidence from more than one allowed source.

    Selection flow:
        1. reserve the best accepted chunk from each source;
        2. combine all remaining accepted chunks;
        3. rank remaining chunks by distance;
        4. fill the available context positions.
    """

    selected_documents: list[RetrievedDocument] = []
    remaining_candidates: list[RetrievedDocument] = []

    for source_id in source_priority:
        source_candidates = candidates_by_source.get(
            source_id,
            [],
        )

        if not source_candidates:
            continue

        ordered_source_candidates = sorted(
            source_candidates,
            key=document_sort_key,
        )

        selected_documents.append(ordered_source_candidates[0])

        remaining_candidates.extend(ordered_source_candidates[1:])

        if len(selected_documents) >= top_k:
            return selected_documents[:top_k]

    remaining_candidates = sorted(
        remaining_candidates,
        key=document_sort_key,
    )

    for document in remaining_candidates:
        if len(selected_documents) >= top_k:
            break

        selected_documents.append(document)

    return selected_documents[:top_k]


def retrieve_relevant_documents(
    question: str,
    allowed_source_ids: tuple[int, ...],
    top_k: int = 5,
) -> list[RetrievedDocument]:
    """
    Retrieve candidates from every allowed source.

    The retrieval process is intentionally generic:

        1. search each allowed source;
        2. combine all candidates;
        3. remove duplicates;
        4. rank globally by semantic distance;
        5. return the best documents.

    No domain-specific keyword rule or static distance
    threshold is used here.
    """

    cleaned_question = question.strip()

    if not cleaned_question:
        return []

    if top_k <= 0:
        return []

    all_candidates: list[RetrievedDocument] = []

    if allowed_source_ids:
        for source_id in allowed_source_ids:
            source_candidates = query_collection(
                question=cleaned_question,
                top_k=RETRIEVAL_CANDIDATES_PER_SOURCE,
                source_id=source_id,
            )

            valid_source_candidates = [
                document
                for document in source_candidates
                if (document.text.strip() and document.source_id == source_id)
            ]

            all_candidates.extend(valid_source_candidates)

    else:
        all_candidates = query_collection(
            question=cleaned_question,
            top_k=max(
                top_k,
                RETRIEVAL_CANDIDATES_PER_SOURCE,
            ),
        )

        all_candidates = [
            document for document in all_candidates if document.text.strip()
        ]

    if not all_candidates:
        return []

    unique_candidates = remove_duplicate_retrievals(all_candidates)

    unique_candidates.sort(key=document_sort_key)

    return unique_candidates[:top_k]


def collection_status() -> dict[str, Any]:
    """
    Return Chroma status information.
    """

    collection = get_collection()

    return {
        "collection_name": collection.name,
        "document_count": collection.count(),
        "database_path": str(CHROMA_DIR),
        "embedding_model": EMBEDDING_MODEL,
        "candidates_per_source": (RETRIEVAL_CANDIDATES_PER_SOURCE),
    }



def is_reference_chunk(text: str) -> bool:
    """
    Detect chunks that mostly contain references,
    publication metadata, or journal promotion.
    """

    cleaned_text = " ".join(text.lower().split())

    strong_reference_markers = (
        "references",
        "bibliography",
        "reference list",
    )

    publication_markers = (
        "received:",
        "accepted:",
        "author contributions",
        "competing interests",
        "publisher's note",
        "publisher’s note",
        "submit your manuscript",
        "online submission",
        "peer review",
        "rapid publication",
        "doi:",
        "available from:",
    )

    link_markers = (
        "http://",
        "https://",
    )

    if any(marker in cleaned_text for marker in strong_reference_markers):
        return True

    publication_marker_count = sum(
        1 for marker in publication_markers if marker in cleaned_text
    )

    link_marker_count = sum(1 for marker in link_markers if marker in cleaned_text)

    return publication_marker_count >= 2 or (
        publication_marker_count >= 1 and link_marker_count >= 1
    )


def retrieve_source_summary_documents(
    source_id: int,
    max_chunks: int = 8,
) -> list[RetrievedDocument]:
    """
    Retrieve representative chunks across an entire source.

    This is used for requests such as:
    'Summarize the food article.'

    It does not use semantic top-k alone because a document
    summary needs information from multiple pages.
    """

    if max_chunks <= 0:
        return []

    collection = get_collection()

    results = collection.get(
        where={
            "source_id": int(source_id),
        },
        include=[
            "documents",
            "metadatas",
        ],
    )

    documents = (
        results.get(
            "documents",
            [],
        )
        or []
    )

    metadatas = (
        results.get(
            "metadatas",
            [],
        )
        or []
    )

    page_documents: dict[
        int,
        RetrievedDocument,
    ] = {}

    for index, document_text in enumerate(documents):
        text = document_text or ""

        if len(text.strip()) < 200:
            continue

        if is_reference_chunk(text):
            continue

        metadata = (
            metadatas[index] if index < len(metadatas) and metadatas[index] else {}
        )

        try:
            page_number = int(
                metadata.get(
                    "page",
                    metadata.get(
                        "page_number",
                        999999,
                    ),
                )
            )
        except (TypeError, ValueError):
            page_number = 999999

        document = RetrievedDocument(
            text=text,
            metadata=metadata,
            distance=None,
            source_id=infer_source_id(metadata),
        )

        existing_document = page_documents.get(page_number)

        if existing_document is None or len(document.text) > len(
            existing_document.text
        ):
            page_documents[page_number] = document

    ordered_documents = [
        page_documents[page_number] for page_number in sorted(page_documents)
    ]

    if len(ordered_documents) <= max_chunks:
        return ordered_documents

    if max_chunks == 1:
        middle_position = len(ordered_documents) // 2

        return [ordered_documents[middle_position]]

    selected_documents: list[RetrievedDocument] = []

    for index in range(max_chunks):
        position = round(index * (len(ordered_documents) - 1) / (max_chunks - 1))

        document = ordered_documents[position]

        if document not in selected_documents:
            selected_documents.append(document)

    return selected_documents
