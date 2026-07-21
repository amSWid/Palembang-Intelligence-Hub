import html
from pathlib import Path
from textwrap import dedent
from typing import Any

import streamlit as st

from config import (
    PDF_FILES,
)
from core.knowledge_catalog import (
    get_source_by_id,
    get_source_key_by_id,
)


def get_document_value(
    document: Any,
    attribute: str,
    default: Any = None,
) -> Any:
    """
    Read a field from an object or dictionary.
    """

    if isinstance(document, dict):
        return document.get(
            attribute,
            default,
        )

    return getattr(
        document,
        attribute,
        default,
    )


def get_document_metadata(
    document: Any,
) -> dict:
    """
    Return metadata safely.
    """

    metadata = get_document_value(
        document,
        "metadata",
        {},
    )

    return metadata if isinstance(metadata, dict) else {}


def get_source_title(
    source_id: int | None,
) -> str:
    """
    Return source title from Knowledge Catalog.
    """

    source = get_source_by_id(source_id)

    if source:
        return str(source["title"])

    if source_id is None:
        return "Palembang Knowledge Source"

    return f"Source Reference {source_id}"


def get_source_filename(
    source_id: int | None,
) -> str | None:
    """
    Return source PDF filename.
    """

    source = get_source_by_id(source_id)

    if not source:
        return None

    filename = source.get("filename")

    return str(filename) if filename else None


def get_pdf_path(
    source_id: int | None,
) -> Path | None:
    """
    Return local PDF path from catalog ID.
    """

    source_key = get_source_key_by_id(source_id)

    if source_key is None:
        return None

    pdf_path = PDF_FILES.get(source_key)

    return pdf_path if isinstance(pdf_path, Path) else None


def get_page_number(
    metadata: dict,
) -> str:
    """
    Return user-facing page number.
    """

    page_value = metadata.get(
        "page",
        metadata.get(
            "page_number",
        ),
    )

    if page_value is None:
        return "Not specified"

    try:
        return str(int(page_value) + 1)

    except (TypeError, ValueError):
        return str(page_value)


def create_excerpt(
    text: str,
    maximum_length: int = 850,
) -> str:
    """
    Create readable source evidence.
    """

    cleaned_text = " ".join(str(text).replace("\x00", " ").split())

    if not cleaned_text:
        return "No source excerpt is available."

    if len(cleaned_text) <= maximum_length:
        return cleaned_text

    return cleaned_text[:maximum_length].rsplit(" ", 1)[0] + "..."


def deduplicate_documents(
    documents: list | None,
) -> list:
    """
    Remove duplicate evidence chunks.
    """

    if not documents:
        return []

    unique_documents = []
    seen_keys = set()

    for document in documents:
        source_id = get_document_value(
            document,
            "source_id",
        )

        text = get_document_value(
            document,
            "text",
            "",
        )

        metadata = get_document_metadata(document)

        page = get_page_number(metadata)

        text_key = " ".join(str(text).lower().split())[:350]

        document_key = (
            source_id,
            page,
            text_key,
        )

        if document_key in seen_keys:
            continue

        seen_keys.add(document_key)

        unique_documents.append(document)

    return unique_documents


def render_pdf_actions(
    source_id: int | None,
    index: int,
):
    """
    Render Preview and Download controls.
    """

    pdf_path = get_pdf_path(source_id)

    filename = get_source_filename(source_id)

    if pdf_path is None or filename is None or not pdf_path.exists():
        st.warning("The source PDF file " "is not available.")
        return

    preview_state_key = f"source_pdf_preview_" f"{source_id}_{index}"

    if preview_state_key not in st.session_state:
        st.session_state[preview_state_key] = False

    preview_column, download_column = st.columns(
        [1, 1],
        gap="small",
    )

    with preview_column:
        preview_label = (
            "Close Preview" if st.session_state[preview_state_key] else "Preview PDF"
        )

        if st.button(
            preview_label,
            key=(f"toggle_preview_" f"{source_id}_{index}"),
            use_container_width=True,
        ):
            st.session_state[preview_state_key] = not st.session_state[
                preview_state_key
            ]

            st.rerun()

    with download_column:
        st.download_button(
            label="Download PDF",
            data=pdf_path.read_bytes(),
            file_name=filename,
            mime="application/pdf",
            key=(f"download_source_" f"{source_id}_{index}"),
            on_click="ignore",
            use_container_width=True,
        )

    if st.session_state[preview_state_key]:
        st.pdf(
            pdf_path,
            height=650,
            key=(f"pdf_viewer_" f"{source_id}_{index}"),
        )


def render_source_document(
    document: Any,
    index: int,
):
    """
    Render one source evidence panel.
    """

    source_id = get_document_value(
        document,
        "source_id",
    )

    text = get_document_value(
        document,
        "text",
        "",
    )

    metadata = get_document_metadata(document)

    source_title = get_source_title(source_id)

    page_number = get_page_number(metadata)

    excerpt = create_excerpt(text)

    expander_title = (
        f"Reference {source_id or '—'}" f" · Page {page_number}" f" · {source_title}"
    )

    with st.expander(
        expander_title,
        expanded=index == 1,
    ):
        st.markdown(f"**{source_title}**")

        authority = metadata.get("authority")

        if authority:
            st.caption(f"Source authority: {authority}")

        st.caption(f"Relevant PDF page: {page_number}")

        st.markdown("##### Relevant evidence")

        st.write(excerpt)

        render_pdf_actions(
            source_id=source_id,
            index=index,
        )


def render_source_evidence(
    documents: list | None,
):
    """
    Render all retrieved references.
    """

    unique_documents = deduplicate_documents(documents)

    if not unique_documents:
        return

    st.html(dedent("""
            <section style="
                margin:18px 46px 8px 46px;
            ">
                <div style="
                    color:#284d73;
                    font-size:15px;
                    font-weight:800;
                ">
                    📚 Source Evidence
                </div>

                <div style="
                    margin-top:5px;
                    color:#8192a5;
                    font-size:10px;
                    line-height:1.5;
                ">
                    Open a reference to inspect
                    the evidence, preview the PDF
                    or download the original document.
                </div>
            </section>
            """).strip())

    for index, document in enumerate(
        unique_documents,
        start=1,
    ):
        render_source_document(
            document=document,
            index=index,
        )


def render_ai_result(
    question: str,
    answer: str,
    source_id: int | None = None,
    documents: list | None = None,
):
    """
    Render AI answer and evidence.
    """

    safe_question = html.escape(question)

    safe_answer = html.escape(answer).replace(
        "\n",
        "<br>",
    )

    source_html = ""

    if source_id is not None:
        source_title = html.escape(get_source_title(source_id))

        source_html = dedent(f"""
            <div class="source-badge">
                📚 Reference {source_id}
                &nbsp;·&nbsp;
                {source_title}
            </div>
            """).strip()

    answer_html = dedent(f"""
        <div class="answer-card">
            <div class="answer-header">
                <div class="answer-icon">
                    ✦
                </div>

                <div>
                    <div class="answer-title">
                        Palembang Intelligence Answer
                    </div>

                    <div style="
                        color:#8a9bad;
                        font-size:9px;
                        margin-top:2px;
                    ">
                        Question: {safe_question}
                    </div>
                </div>
            </div>

            <div class="answer-text">
                {safe_answer}
            </div>

            {source_html}
        </div>
        """).strip()

    st.html(answer_html)

    render_source_evidence(documents)


def render_loading_result():
    """
    Render loading card.
    """

    st.html(dedent("""
            <div class="answer-card">
                <div class="answer-header">
                    <div class="answer-icon">
                        ⏳
                    </div>

                    <div class="answer-title">
                        Palembang Intelligence
                        is thinking...
                    </div>
                </div>

                <div class="answer-text">
                    Searching trusted Palembang
                    knowledge and preparing the
                    most relevant answer.
                </div>
            </div>
            """).strip())


def render_error_result(
    message: str,
):
    """
    Render safe error card.
    """

    safe_message = html.escape(message)

    st.html(dedent(f"""
            <div class="answer-card">
                <div class="answer-header">
                    <div class="answer-icon">
                        ⚠
                    </div>

                    <div class="answer-title">
                        The answer could not
                        be generated
                    </div>
                </div>

                <div class="answer-text">
                    {safe_message}
                </div>
            </div>
            """).strip())


def render_placeholder_result(
    question: str,
):
    """
    Backward-compatible placeholder.
    """

    render_ai_result(
        question=question,
        answer=("The question has been received."),
        source_id=None,
        documents=None,
    )
