import streamlit as st
import os
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)
from langchain_groq import ChatGroq

from config import (
    LLM_MODEL,
    LLM_TEMPERATURE,
)
from core.agent_selector import (
    AgentSelection,
    select_agent,
)


from core.chroma_loader import (
    RetrievedDocument,
    retrieve_relevant_documents,
    retrieve_source_summary_documents,
)


from core.prompt_builder import (
    build_system_prompt,
    build_user_prompt,
)

load_dotenv()


@dataclass
class RAGResponse:
    """
    Final result returned to the Streamlit UI.
    """

    question: str
    answer: str
    category: str
    source_id: int | None
    source_ids: tuple[int, ...]
    documents: list[RetrievedDocument]
    metadata: dict[str, Any]


def validate_api_key():
    """
    Ensure GROQ_API_KEY is available.
    """

    api_key = os.getenv(
        "GROQ_API_KEY",
        "",
    ).strip()

    if not api_key:
        raise RuntimeError("GROQ_API_KEY was not found. " "Add it to the .env file.")


@st.cache_resource(show_spinner=False)
def create_llm() -> ChatGroq:
    """
    Create and cache the Groq chat model.

    The same ChatGroq client is reused across
    Streamlit reruns for faster responses.
    """

    validate_api_key()

    return ChatGroq(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        max_retries=1,
        timeout=45,
    )


def determine_primary_source(
    documents: list[RetrievedDocument],
    preferred_source_ids: tuple[int, ...],
) -> int | None:
    """
    Select one main source reference for the UI.
    """

    retrieved_source_ids = [
        document.source_id for document in documents if document.source_id is not None
    ]

    for preferred_source_id in preferred_source_ids:
        if preferred_source_id in (retrieved_source_ids):
            return preferred_source_id

    if retrieved_source_ids:
        return retrieved_source_ids[0]

    return None


def remove_duplicate_documents(
    documents: list[RetrievedDocument],
) -> list[RetrievedDocument]:
    """
    Remove duplicate or nearly identical retrieved chunks.
    """

    unique_documents = []
    seen_texts = set()

    for document in documents:
        normalised_text = " ".join(document.text.lower().split())

        comparison_key = normalised_text[:500]

        if not comparison_key:
            continue

        if comparison_key in seen_texts:
            continue

        seen_texts.add(comparison_key)
        unique_documents.append(document)

    return unique_documents



def is_document_summary_request(
    question: str,
) -> bool:
    """
    Detect requests to summarize an entire document.
    """

    cleaned_question = question.lower().strip()

    summary_phrases = (
        "summarize the food article",
        "summarise the food article",
        "summarize the culinary article",
        "summarise the culinary article",
        "summary of the food article",
        "ringkas artikel makanan",
        "ringkas artikel kuliner",
        "rangkum artikel makanan",
        "rangkum artikel kuliner",
    )

    return any(phrase in cleaned_question for phrase in summary_phrases)


def retrieve_context(
    question: str,
    selection: AgentSelection,
) -> list[RetrievedDocument]:
    """
    Retrieve focused context for normal questions and broader
    context for document-summary requests.
    """

    if is_document_summary_request(question) and selection.source_ids:
        documents = retrieve_source_summary_documents(
            source_id=selection.source_ids[0],
            max_chunks=8,
        )

        documents = remove_duplicate_documents(documents)

        return documents[:8]

    documents = retrieve_relevant_documents(
        question=selection.search_query,
        allowed_source_ids=selection.source_ids,
        top_k=4,
    )

    documents = remove_duplicate_documents(documents)

    return documents[:3]


def generate_rag_answer(
    question: str,
) -> RAGResponse:
    """
    Run the complete Palembang RAG pipeline.

    Flow:
        question
        -> agent selector
        -> Chroma retrieval
        -> prompt builder
        -> Groq
        -> RAGResponse
    """

    cleaned_question = question.strip()

    if not cleaned_question:
        raise ValueError("Question cannot be empty.")

    selection = select_agent(cleaned_question)

    documents = retrieve_context(
        question=cleaned_question,
        selection=selection,
    )

    if not documents:
        return RAGResponse(
            question=cleaned_question,
            answer=(
                "The Palembang knowledge database "
                "did not return relevant information "
                "for this question."
            ),
            category=selection.category,
            source_id=None,
            source_ids=(),
            documents=[],
            metadata={
                "retrieved_count": 0,
                "model": None,
            },
        )

    system_prompt = build_system_prompt(selection)

    user_prompt = build_user_prompt(
        question=cleaned_question,
        documents=documents,
        selection=selection,
    )

    llm = create_llm()

    response = llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
    )

    answer = (
        response.content.strip()
        if isinstance(response.content, str)
        else str(response.content).strip()
    )

    if not answer:
        answer = "The AI did not return a usable answer."

    primary_source_id = determine_primary_source(
        documents=documents,
        preferred_source_ids=(selection.source_ids),
    )

    unique_source_ids = tuple(
        dict.fromkeys(
            document.source_id
            for document in documents
            if document.source_id is not None
        )
    )

    response_metadata = (
        getattr(
            response,
            "response_metadata",
            {},
        )
        or {}
    )

    return RAGResponse(
        question=cleaned_question,
        answer=answer,
        category=selection.category,
        source_id=primary_source_id,
        source_ids=unique_source_ids,
        documents=documents,
        metadata={
            "retrieved_count": len(documents),
            "model": LLM_MODEL,
            "response_metadata": (response_metadata),
        },
    )
