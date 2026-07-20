from __future__ import annotations

import json
import py_compile
import statistics
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

# =========================================================
# PROJECT PATH
# =========================================================

ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# =========================================================
# PROJECT IMPORTS
# =========================================================

from config import (  # noqa: E402
    CHROMA_DIR,
    CLEANED_TEXT_FILE,
    COLLECTION_NAME,
    PDF_FILES,
)

from core.agent_selector import (  # noqa: E402
    select_agent,
)

from core.chroma_loader import (  # noqa: E402
    collection_status,
    get_collection,
    retrieve_relevant_documents,
)

from core.pdf_loader import (  # noqa: E402
    load_all_pdfs,
)

# =========================================================
# OUTPUT FILES
# =========================================================

TEXT_REPORT_FILE = ROOT_DIR / "audit_report.txt"
JSON_REPORT_FILE = ROOT_DIR / "audit_report.json"


# =========================================================
# TEST QUESTIONS
# =========================================================

TEST_QUESTIONS = [
    "What makes pempek special in Palembang?",
    "What is tekwan and how is it served?",
    "What makes mie celor unique in Palembang?",
    "What is the history of Ampera Bridge?",
    "Why is the Musi River important to Palembang?",
    "Tell me about Palembang culture and music.",
    "What is Palembang's regional GDP?",
    "What agricultural commodities are produced in Palembang?",
    "What are Palembang's investment opportunities?",
    "What sectors have growth potential in Palembang?",
]


# =========================================================
# REPORT HELPERS
# =========================================================


class AuditReport:
    """
    Store audit information in text and JSON formats.
    """

    def __init__(self) -> None:
        self.lines: list[str] = []
        self.data: dict[str, Any] = {
            "audit_time": datetime.now().isoformat(timespec="seconds"),
            "project_root": str(ROOT_DIR),
            "sections": {},
        }

    def heading(
        self,
        title: str,
    ) -> None:
        separator = "=" * 72

        self.lines.extend(
            [
                "",
                separator,
                title,
                separator,
            ]
        )

        print()
        print(separator)
        print(title)
        print(separator)

    def line(
        self,
        message: str,
    ) -> None:
        self.lines.append(message)
        print(message)

    def save(self) -> None:
        TEXT_REPORT_FILE.write_text(
            "\n".join(self.lines),
            encoding="utf-8",
        )

        JSON_REPORT_FILE.write_text(
            json.dumps(
                self.data,
                indent=2,
                ensure_ascii=False,
                default=str,
            ),
            encoding="utf-8",
        )


# =========================================================
# GENERAL HELPERS
# =========================================================


def safe_preview(
    text: str,
    maximum_length: int = 300,
) -> str:
    """
    Create a single-line text preview.
    """

    cleaned_text = " ".join(str(text).replace("\x00", " ").split())

    if len(cleaned_text) <= maximum_length:
        return cleaned_text

    return cleaned_text[:maximum_length].rsplit(" ", 1)[0] + "..."


def safe_average(
    values: list[int | float],
) -> float:
    """
    Return average value safely.
    """

    if not values:
        return 0.0

    return float(statistics.mean(values))


def safe_minimum(
    values: list[int | float],
) -> int | float:
    if not values:
        return 0

    return min(values)


def safe_maximum(
    values: list[int | float],
) -> int | float:
    if not values:
        return 0

    return max(values)


def metadata_source_id(
    metadata: dict[str, Any],
) -> int | None:
    """
    Read source_id safely from Chroma metadata.
    """

    value = metadata.get("source_id")

    if value is None:
        return None

    try:
        return int(value)

    except (TypeError, ValueError):
        return None


# =========================================================
# AUDIT 1 — PROJECT STRUCTURE
# =========================================================


def audit_project_structure(
    report: AuditReport,
) -> None:
    """
    Check important project files and directories.
    """

    report.heading("1. PROJECT STRUCTURE AUDIT")

    required_paths = [
        ROOT_DIR / "app.py",
        ROOT_DIR / "config.py",
        ROOT_DIR / "requirements.txt",
        ROOT_DIR / ".env",
        ROOT_DIR / "core",
        ROOT_DIR / "pages",
        ROOT_DIR / "ui",
        ROOT_DIR / "data",
        ROOT_DIR / "assets",
        CHROMA_DIR,
    ]

    structure_results = []

    for path in required_paths:
        exists = path.exists()

        status = "OK" if exists else "MISSING"

        report.line(f"[{status:7}] {path.relative_to(ROOT_DIR)}")

        structure_results.append(
            {
                "path": str(path),
                "exists": exists,
            }
        )

    report.data["sections"]["project_structure"] = structure_results


# =========================================================
# AUDIT 2 — PYTHON SYNTAX
# =========================================================


def audit_python_syntax(
    report: AuditReport,
) -> None:
    """
    Compile important Python files.
    """

    report.heading("2. PYTHON SYNTAX AUDIT")

    python_files = [
        ROOT_DIR / "app.py",
        ROOT_DIR / "config.py",
        ROOT_DIR / "hero.py",
        ROOT_DIR / "navbar.py",
        ROOT_DIR / "result.py",
        ROOT_DIR / "search.py",
    ]

    python_files.extend(sorted((ROOT_DIR / "core").glob("*.py")))

    python_files.extend(sorted((ROOT_DIR / "pages").glob("*.py")))

    python_files.extend(sorted((ROOT_DIR / "ui").glob("*.py")))

    syntax_results = []

    for file_path in python_files:
        if not file_path.exists():
            continue

        try:
            py_compile.compile(
                str(file_path),
                doraise=True,
            )

            report.line(f"[OK     ] " f"{file_path.relative_to(ROOT_DIR)}")

            syntax_results.append(
                {
                    "file": str(file_path),
                    "status": "ok",
                }
            )

        except Exception as error:
            report.line(f"[ERROR  ] " f"{file_path.relative_to(ROOT_DIR)}")

            report.line(f"          {error}")

            syntax_results.append(
                {
                    "file": str(file_path),
                    "status": "error",
                    "error": str(error),
                }
            )

    report.data["sections"]["python_syntax"] = syntax_results


# =========================================================
# AUDIT 3 — PDF FILES
# =========================================================


def audit_pdf_files(
    report: AuditReport,
) -> None:
    """
    Check PDF existence and file sizes.
    """

    report.heading("3. PDF SOURCE AUDIT")

    pdf_results = []

    for source_name, pdf_path in PDF_FILES.items():
        exists = pdf_path.exists()

        if exists:
            file_size_mb = pdf_path.stat().st_size / 1024 / 1024

            report.line(f"[OK     ] {source_name}")

            report.line(f"          File : {pdf_path.name}")

            report.line(f"          Size : {file_size_mb:.2f} MB")

        else:
            file_size_mb = 0.0

            report.line(f"[MISSING] {source_name}")

            report.line(f"          Path : {pdf_path}")

        pdf_results.append(
            {
                "source_name": source_name,
                "path": str(pdf_path),
                "exists": exists,
                "file_size_mb": round(
                    file_size_mb,
                    3,
                ),
            }
        )

    report.data["sections"]["pdf_sources"] = pdf_results


# =========================================================
# AUDIT 4 — PDF LOADER
# =========================================================


def audit_pdf_loader(
    report: AuditReport,
) -> None:
    """
    Load PDFs and inspect extracted page text.
    """

    report.heading("4. PDF LOADER AUDIT")

    try:
        documents = load_all_pdfs()

    except Exception as error:
        report.line(f"[ERROR] PDF loading failed: {error}")

        report.data["sections"]["pdf_loader"] = {
            "status": "error",
            "error": str(error),
        }

        return

    source_counts = Counter()
    empty_pages = 0
    short_pages = 0
    page_lengths = []

    for document in documents:
        source_name = document.metadata.get(
            "source_name",
            "unknown",
        )

        source_counts[source_name] += 1

        text = document.page_content or ""
        text_length = len(text.strip())

        page_lengths.append(text_length)

        if text_length == 0:
            empty_pages += 1

        elif text_length < 100:
            short_pages += 1

    report.line(f"Total PDF pages loaded : {len(documents)}")

    report.line(f"Empty pages            : {empty_pages}")

    report.line(f"Very short pages       : {short_pages}")

    report.line(f"Average characters     : " f"{safe_average(page_lengths):.1f}")

    report.line(f"Minimum characters     : " f"{safe_minimum(page_lengths)}")

    report.line(f"Maximum characters     : " f"{safe_maximum(page_lengths)}")

    report.line("")
    report.line("Pages by source:")

    for source_name, count in sorted(source_counts.items()):
        report.line(f"  - {source_name}: {count}")

    report.line("")
    report.line("First extracted page preview:")

    if documents:
        first_document = documents[0]

        report.line(
            safe_preview(
                first_document.page_content,
                maximum_length=500,
            )
        )

        report.line(f"Metadata: {first_document.metadata}")

    report.data["sections"]["pdf_loader"] = {
        "status": "ok",
        "total_pages": len(documents),
        "empty_pages": empty_pages,
        "short_pages": short_pages,
        "average_characters": round(
            safe_average(page_lengths),
            2,
        ),
        "minimum_characters": safe_minimum(page_lengths),
        "maximum_characters": safe_maximum(page_lengths),
        "pages_by_source": dict(source_counts),
    }


# =========================================================
# AUDIT 5 — CLEANED TEXT
# =========================================================


def audit_cleaned_text(
    report: AuditReport,
) -> None:
    """
    Inspect the optional cleaned text file.
    """

    report.heading("5. CLEANED TEXT AUDIT")

    if not CLEANED_TEXT_FILE.exists():
        report.line("[WARNING] Cleaned text file does not exist.")

        report.line(f"Expected path: {CLEANED_TEXT_FILE}")

        report.data["sections"]["cleaned_text"] = {
            "exists": False,
            "path": str(CLEANED_TEXT_FILE),
        }

        return

    text = CLEANED_TEXT_FILE.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    line_count = len(text.splitlines())

    empty_line_count = sum(1 for line in text.splitlines() if not line.strip())

    suspicious_patterns = {
        "null_characters": text.count("\x00"),
        "replacement_characters": text.count("�"),
        "multiple_spaces": text.count("   "),
        "hyphen_line_breaks": text.count("-\n"),
    }

    report.line(f"File               : {CLEANED_TEXT_FILE.name}")

    report.line(f"Characters         : {len(text):,}")

    report.line(f"Lines              : {line_count:,}")

    report.line(f"Empty lines        : {empty_line_count:,}")

    for label, count in suspicious_patterns.items():
        report.line(f"{label:19}: {count:,}")

    report.line("")
    report.line("Cleaned text preview:")

    report.line(
        safe_preview(
            text,
            maximum_length=700,
        )
    )

    report.data["sections"]["cleaned_text"] = {
        "exists": True,
        "path": str(CLEANED_TEXT_FILE),
        "characters": len(text),
        "lines": line_count,
        "empty_lines": empty_line_count,
        "suspicious_patterns": (suspicious_patterns),
    }


# =========================================================
# AUDIT 6 — CHROMA COLLECTION
# =========================================================


def audit_chroma_collection(
    report: AuditReport,
) -> None:
    """
    Inspect Chroma count, metadata and chunk sizes.
    """

    report.heading("6. CHROMA DATABASE AUDIT")

    try:
        status = collection_status()
        collection = get_collection()

    except Exception as error:
        report.line(f"[ERROR] Chroma audit failed: {error}")

        report.data["sections"]["chroma"] = {
            "status": "error",
            "error": str(error),
        }

        return

    total_count = collection.count()

    report.line(f"Collection name : {status['collection_name']}")

    report.line(f"Document count  : {total_count}")

    report.line(f"Database path   : {status['database_path']}")

    report.line(f"Embedding model : {status['embedding_model']}")

    if total_count == 0:
        report.line("[ERROR] Chroma collection is empty.")

        return

    results = collection.get(
        limit=total_count,
        include=[
            "documents",
            "metadatas",
        ],
    )

    documents = results.get("documents") or []

    metadatas = results.get("metadatas") or []

    source_id_counts = Counter()
    source_name_counts = Counter()
    category_counts = Counter()

    missing_source_id = 0
    missing_source_name = 0
    missing_page = 0
    missing_chunk_index = 0
    missing_category = 0

    chunk_lengths = []

    for index, document_text in enumerate(documents):
        metadata = (
            metadatas[index] if index < len(metadatas) and metadatas[index] else {}
        )

        chunk_lengths.append(len(document_text or ""))

        source_id = metadata_source_id(metadata)

        source_name = metadata.get("source_name")

        category = metadata.get("category")

        if source_id is None:
            missing_source_id += 1
        else:
            source_id_counts[source_id] += 1

        if not source_name:
            missing_source_name += 1
        else:
            source_name_counts[str(source_name)] += 1

        if metadata.get("page") is None:
            missing_page += 1

        if metadata.get("chunk_index") is None:
            missing_chunk_index += 1

        if not category:
            missing_category += 1
        else:
            category_counts[str(category)] += 1

    report.line("")
    report.line("Chunk length statistics:")

    report.line(f"  Average : " f"{safe_average(chunk_lengths):.1f}")

    report.line(f"  Minimum : " f"{safe_minimum(chunk_lengths)}")

    report.line(f"  Maximum : " f"{safe_maximum(chunk_lengths)}")

    report.line("")
    report.line("Chunks by source_id:")

    for source_id, count in sorted(source_id_counts.items()):
        report.line(f"  - Source {source_id}: {count}")

    report.line("")
    report.line("Chunks by source_name:")

    for source_name, count in sorted(source_name_counts.items()):
        report.line(f"  - {source_name}: {count}")

    report.line("")
    report.line("Metadata completeness:")

    report.line(f"  Missing source_id   : {missing_source_id}")

    report.line(f"  Missing source_name : {missing_source_name}")

    report.line(f"  Missing page        : {missing_page}")

    report.line(f"  Missing chunk_index : {missing_chunk_index}")

    report.line(f"  Missing category    : {missing_category}")

    if category_counts:
        report.line("")
        report.line("Chunks by category:")

        for category, count in sorted(category_counts.items()):
            report.line(f"  - {category}: {count}")

    else:
        report.line("")
        report.line(
            "[INFO] Category metadata is not stored "
            "inside the current Chroma collection."
        )

    report.line("")
    report.line("First Chroma chunk preview:")

    if documents:
        report.line(
            safe_preview(
                documents[0],
                maximum_length=500,
            )
        )

        first_metadata = metadatas[0] if metadatas else {}

        report.line(f"Metadata: {first_metadata}")

    report.data["sections"]["chroma"] = {
        "status": "ok",
        "collection_name": COLLECTION_NAME,
        "document_count": total_count,
        "chunk_lengths": {
            "average": round(
                safe_average(chunk_lengths),
                2,
            ),
            "minimum": safe_minimum(chunk_lengths),
            "maximum": safe_maximum(chunk_lengths),
        },
        "chunks_by_source_id": dict(source_id_counts),
        "chunks_by_source_name": dict(source_name_counts),
        "chunks_by_category": dict(category_counts),
        "missing_metadata": {
            "source_id": missing_source_id,
            "source_name": missing_source_name,
            "page": missing_page,
            "chunk_index": missing_chunk_index,
            "category": missing_category,
        },
    }


# =========================================================
# AUDIT 7 — AGENT ROUTING
# =========================================================


def audit_agent_routing(
    report: AuditReport,
) -> None:
    """
    Test question classification.
    """

    report.heading("7. AGENT ROUTING AUDIT")

    routing_results = []

    for question in TEST_QUESTIONS:
        try:
            selection = select_agent(question)

            report.line(f"Question : {question}")

            report.line(f"Category : {selection.category}")

            report.line(f"Sources  : {selection.source_ids}")

            report.line("-" * 72)

            routing_results.append(
                {
                    "question": question,
                    "category": (selection.category),
                    "source_ids": list(selection.source_ids),
                    "search_query": (selection.search_query),
                }
            )

        except Exception as error:
            report.line(f"[ERROR] {question}")

            report.line(f"        {error}")

            routing_results.append(
                {
                    "question": question,
                    "error": str(error),
                }
            )

    report.data["sections"]["agent_routing"] = routing_results


# =========================================================
# AUDIT 8 — RETRIEVAL
# =========================================================


def audit_retrieval(
    report: AuditReport,
) -> None:
    """
    Test Chroma retrieval without calling Groq.
    """

    report.heading("8. CHROMA RETRIEVAL AUDIT")

    retrieval_results = []

    for question in TEST_QUESTIONS:
        try:
            selection = select_agent(question)

            documents = retrieve_relevant_documents(
                question=(selection.search_query),
                allowed_source_ids=(selection.source_ids),
                top_k=3,
            )

            report.line(f"Question  : {question}")

            report.line(f"Category  : {selection.category}")

            report.line(f"Retrieved : {len(documents)}")

            document_results = []

            for index, document in enumerate(
                documents,
                start=1,
            ):
                page = document.metadata.get("page")

                displayed_page = int(page) + 1 if isinstance(page, int) else page

                report.line(
                    f"  Result {index}: "
                    f"source={document.source_id}, "
                    f"page={displayed_page}, "
                    f"distance={document.distance}"
                )

                report.line(
                    "    "
                    + safe_preview(
                        document.text,
                        maximum_length=240,
                    )
                )

                document_results.append(
                    {
                        "source_id": (document.source_id),
                        "page": displayed_page,
                        "distance": (document.distance),
                        "preview": safe_preview(
                            document.text,
                            maximum_length=500,
                        ),
                        "metadata": (document.metadata),
                    }
                )

            report.line("-" * 72)

            retrieval_results.append(
                {
                    "question": question,
                    "category": (selection.category),
                    "allowed_source_ids": list(selection.source_ids),
                    "retrieved_count": len(documents),
                    "documents": document_results,
                }
            )

        except Exception as error:
            report.line(f"[ERROR] Retrieval failed:")

            report.line(f"Question: {question}")

            report.line(f"Error   : {error}")

            report.line("-" * 72)

            retrieval_results.append(
                {
                    "question": question,
                    "error": str(error),
                }
            )

    report.data["sections"]["retrieval"] = retrieval_results


# =========================================================
# AUDIT 9 — SOURCE PDF MAPPING
# =========================================================


def audit_source_mapping(
    report: AuditReport,
) -> None:
    """
    Verify source IDs against the current PDFs.
    """

    report.heading("9. SOURCE REFERENCE MAPPING")

    expected_mapping = {
        1: "palembang_ebook",
        2: "palembang_gdp",
        3: "palembang_bi",
    }

    mapping_results = []

    for source_id, pdf_key in expected_mapping.items():
        pdf_path = PDF_FILES.get(pdf_key)

        exists = pdf_path is not None and pdf_path.exists()

        status = "OK" if exists else "MISSING"

        report.line(f"[{status:7}] " f"Reference {source_id} " f"→ {pdf_key}")

        if pdf_path is not None:
            report.line(f"          {pdf_path.name}")

        mapping_results.append(
            {
                "source_id": source_id,
                "pdf_key": pdf_key,
                "path": (str(pdf_path) if pdf_path else None),
                "exists": exists,
            }
        )

    report.data["sections"]["source_mapping"] = mapping_results


# =========================================================
# FINAL SUMMARY
# =========================================================


def render_final_summary(
    report: AuditReport,
) -> None:
    """
    Print simple automatic recommendations.
    """

    report.heading("10. AUTOMATIC AUDIT SUMMARY")

    sections = report.data["sections"]

    recommendations = []

    syntax_errors = [
        item
        for item in sections.get("python_syntax", [])
        if item.get("status") == "error"
    ]

    if syntax_errors:
        recommendations.append(
            "Fix Python syntax errors before " "adding new PDFs or Tavily."
        )

    missing_pdfs = [
        item for item in sections.get("pdf_sources", []) if not item.get("exists")
    ]

    if missing_pdfs:
        recommendations.append("One or more configured PDF files " "are missing.")

    chroma_data = sections.get("chroma", {})

    if (
        chroma_data.get(
            "document_count",
            0,
        )
        == 0
    ):
        recommendations.append("Rebuild Chroma because the " "collection is empty.")

    missing_metadata = chroma_data.get(
        "missing_metadata",
        {},
    )

    if (
        missing_metadata.get(
            "source_id",
            0,
        )
        > 0
    ):
        recommendations.append(
            "Rebuild Chroma with source_id " "metadata for every chunk."
        )

    if (
        missing_metadata.get(
            "page",
            0,
        )
        > 0
    ):
        recommendations.append(
            "Some chunks do not have page " "metadata, affecting references."
        )

    retrieval_errors = [
        item for item in sections.get("retrieval", []) if item.get("error")
    ]

    if retrieval_errors:
        recommendations.append(
            "Review retrieval errors before " "adding new knowledge sources."
        )

    if not recommendations:
        recommendations.append(
            "The current PDF and Chroma foundation "
            "looks ready for additional sources."
        )

        recommendations.append(
            "Add new PDFs one at a time, rebuild " "Chroma, and run this audit again."
        )

        recommendations.append(
            "Add Tavily only after the local " "knowledge audit remains stable."
        )

    for index, recommendation in enumerate(
        recommendations,
        start=1,
    ):
        report.line(f"{index}. {recommendation}")

    report.data["sections"]["recommendations"] = recommendations


# =========================================================
# MAIN
# =========================================================


def run_full_audit() -> None:
    """
    Run all project audits.
    """

    report = AuditReport()

    report.line("PALEMBANG INTELLIGENCE HUB")

    report.line("LOCAL KNOWLEDGE AND RAG AUDIT")

    report.line(f"Audit time: " f"{report.data['audit_time']}")

    audit_project_structure(report)
    audit_python_syntax(report)
    audit_pdf_files(report)
    audit_pdf_loader(report)
    audit_cleaned_text(report)
    audit_chroma_collection(report)
    audit_agent_routing(report)
    audit_retrieval(report)
    audit_source_mapping(report)
    render_final_summary(report)

    report.save()

    report.heading("AUDIT COMPLETED")

    report.line(f"Text report : {TEXT_REPORT_FILE}")

    report.line(f"JSON report : {JSON_REPORT_FILE}")


if __name__ == "__main__":
    run_full_audit()
