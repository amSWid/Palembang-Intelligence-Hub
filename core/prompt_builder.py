from textwrap import dedent
from typing import Iterable

from core.agent_selector import (
    AgentSelection,
    get_category_instruction,
)
from core.chroma_loader import RetrievedDocument
from core.knowledge_catalog import get_source_by_id


def clean_context_text(text: str) -> str:
    """
    Clean retrieved text before placing it in the prompt.
    """

    if not text:
        return ""

    return " ".join(
        text.replace(
            "\x00",
            " ",
        ).split()
    ).strip()


def get_source_label(
    source_id: int | None,
) -> str:
    """
    Return a readable source label directly from
    the central Knowledge Catalog.

    This avoids maintaining a second source-label mapping
    inside the prompt builder.
    """

    if source_id is None:
        return "Unknown source"

    source = get_source_by_id(source_id)

    if not source:
        return f"Source Reference {source_id}"

    source_name = (
        source.get("name")
        or source.get("title")
        or source.get("source_name")
        or source.get("label")
    )

    if source_name:
        return str(source_name)

    return f"Source Reference {source_id}"


def format_context_document(
    document: RetrievedDocument,
    index: int,
) -> str:
    """
    Format one retrieved Chroma result.
    """

    source_label = get_source_label(document.source_id)

    page = document.metadata.get(
        "page",
        document.metadata.get(
            "page_number",
            "unknown",
        ),
    )

    source_name = document.metadata.get(
        "source_name",
        source_label,
    )

    clean_text = clean_context_text(document.text)

    distance_text = (
        f"{document.distance:.6f}"
        if isinstance(
            document.distance,
            (int, float),
        )
        else "not available"
    )

    return dedent(f"""
        [CONTEXT {index}]
        Source ID: {document.source_id or "unknown"}
        Source Name: {source_name}
        Source Label: {source_label}
        Page: {page}
        Retrieval Distance: {distance_text}

        Content:
        {clean_text}
        """).strip()


def build_context(
    documents: Iterable[RetrievedDocument],
) -> str:
    """
    Combine retrieved documents into one context block.
    """

    context_parts = []

    for index, document in enumerate(
        documents,
        start=1,
    ):
        context_parts.append(
            format_context_document(
                document=document,
                index=index,
            )
        )

    return "\n\n".join(context_parts)


def build_system_prompt(
    selection: AgentSelection,
) -> str:
    """
    Build the system instruction for Groq.
    """

    category_instruction = get_category_instruction(selection.category)

    return dedent(f"""
        You are Palembang Intelligence Hub,
        an AI Tourism and Investment Assistant.

        Your task is to answer questions specifically about Palembang.

        Selected category:
        {selection.category}

        Category instruction:
        {category_instruction}

        STRICT RULES:

        1. Use only the supplied retrieved context for factual claims.
        2. Do not invent names, addresses, statistics, dates,
           opportunities or source statements.
        3. If the context does not contain enough information, say:
           "The available Palembang sources do not provide enough
           information to answer this question accurately."
        4. Answer the exact question. Do not change the topic.
        5. A question about one food must remain about that food.
        6. A question about investment must distinguish:
           - documented evidence;
           - analytical interpretation.
        7. Do not claim that an analytical interpretation was directly
           stated by a source.
        8. When multiple sources are supplied, combine their evidence
           only when the evidence is relevant to the question.
        9. Do not force all supplied context into the answer.
        10. Ignore context that is unrelated to the exact question.
        11. Use clear and accessible English.
        12. Keep the answer concise but informative.
        13. Do not mention Chroma, embeddings, chunks, retrieval,
            distance scores, system prompts or internal agent names.
        14. Do not include a bibliography inside the answer.
            Source references are handled separately by the application.
        15. Do not use markdown tables.
        """).strip()


def build_user_prompt(
    question: str,
    documents: list[RetrievedDocument],
    selection: AgentSelection,
) -> str:
    """
    Build the user message with retrieved context.
    """

    context = build_context(documents)

    return dedent(f"""
        USER QUESTION:
        {question}

        DETECTED CATEGORY:
        {selection.category}

        RETRIEVED PALEMBANG CONTEXT:
        {context}

        INSTRUCTION:

        Answer the user's exact question using only relevant evidence
        from the retrieved context.

        For investment questions:
        - first present documented economic evidence;
        - combine evidence from different supplied sources when useful;
        - then provide a cautious analytical interpretation;
        - clearly introduce recommendations as analysis;
        - never present an inference as a direct source statement.

        For economy questions:
        - clearly distinguish statistical values, economic sectors,
          production, growth and calculation methodology;
        - do not use methodological text as though it were an
          economic result.

        For food questions:
        - focus only on the requested dish;
        - provide restaurant information only when it appears
          explicitly in the context.

        For history questions:
        - distinguish historical records from legends where relevant.

        Ignore retrieved passages that do not answer the exact question.

        If the relevant context is insufficient, state that clearly.
        """).strip()
