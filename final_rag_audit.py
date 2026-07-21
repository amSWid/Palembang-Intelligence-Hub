from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from statistics import mean
from typing import Any

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
REPORT_FILE = BASE_DIR / "final_rag_audit_report.txt"


def write_line(
    message: str = "",
    report_lines: list[str] | None = None,
) -> None:
    print(message)

    if report_lines is not None:
        report_lines.append(message)


def section(
    title: str,
    report_lines: list[str],
) -> None:
    separator = "=" * 72

    write_line("", report_lines)
    write_line(separator, report_lines)
    write_line(title, report_lines)
    write_line(separator, report_lines)


def safe_run_command(
    command: list[str],
) -> tuple[int, str]:
    try:
        process = subprocess.run(
            command,
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            check=False,
        )

        output = "\n".join(
            part.strip()
            for part in (process.stdout, process.stderr)
            if part and part.strip()
        )

        return process.returncode, output

    except Exception as error:
        return 1, f"{type(error).__name__}: {error}"


def audit_python_files(
    report_lines: list[str],
) -> bool:
    section("1. PYTHON SYNTAX AUDIT", report_lines)

    files_to_check = [
        BASE_DIR / "app.py",
        BASE_DIR / "config.py",
        BASE_DIR / "core" / "agent_selector.py",
        BASE_DIR / "core" / "knowledge_catalog.py",
        BASE_DIR / "core" / "chroma_loader.py",
        BASE_DIR / "core" / "rag_agent.py",
        BASE_DIR / "core" / "prompt_builder.py",
        BASE_DIR / "core" / "build_chroma.py",
        BASE_DIR / "pages" / "home.py",
    ]

    all_passed = True

    for file_path in files_to_check:
        relative_path = file_path.relative_to(BASE_DIR)

        if not file_path.exists():
            write_line(
                f"[FAIL] Missing file: {relative_path}",
                report_lines,
            )
            all_passed = False
            continue

        return_code, output = safe_run_command(
            [
                sys.executable,
                "-m",
                "py_compile",
                str(file_path),
            ]
        )

        if return_code == 0:
            write_line(
                f"[PASS] {relative_path}",
                report_lines,
            )
        else:
            write_line(
                f"[FAIL] {relative_path}",
                report_lines,
            )
            write_line(output, report_lines)
            all_passed = False

    return all_passed


def audit_environment(
    report_lines: list[str],
) -> bool:
    section("2. ENVIRONMENT AND SECURITY AUDIT", report_lines)

    load_dotenv(BASE_DIR / ".env")

    all_passed = True

    env_file = BASE_DIR / ".env"

    if env_file.exists():
        write_line("[PASS] Local .env file exists.", report_lines)
    else:
        write_line("[FAIL] Local .env file was not found.", report_lines)
        all_passed = False

    groq_key = os.getenv("GROQ_API_KEY", "").strip()

    if groq_key:
        write_line(
            "[PASS] GROQ_API_KEY is loaded without displaying its value.",
            report_lines,
        )
    else:
        write_line("[FAIL] GROQ_API_KEY is missing.", report_lines)
        all_passed = False

    return_code, output = safe_run_command(["git", "check-ignore", "-v", ".env"])

    if return_code == 0 and ".env" in output:
        write_line("[PASS] .env is ignored by Git.", report_lines)
        write_line(f"       {output}", report_lines)
    else:
        write_line("[FAIL] .env may not be ignored by Git.", report_lines)
        all_passed = False

    return all_passed


def audit_git(
    report_lines: list[str],
) -> bool:
    section("3. GIT AUDIT", report_lines)

    return_code, output = safe_run_command(["git", "status", "--short"])

    if return_code != 0:
        write_line("[FAIL] Unable to read Git status.", report_lines)
        write_line(output, report_lines)
        return False

    if not output:
        write_line("[PASS] Git working tree is clean.", report_lines)
        return True

    write_line("[WARN] Git working tree contains changes:", report_lines)
    write_line(output, report_lines)

    return True


def audit_catalog_and_config(
    report_lines: list[str],
) -> bool:
    section("4. KNOWLEDGE CATALOG AND CONFIG AUDIT", report_lines)

    try:
        from config import (
            CHROMA_DIR,
            CHUNK_OVERLAP,
            CHUNK_SIZE,
            COLLECTION_NAME,
            EMBEDDING_MODEL,
            LLM_MODEL,
            PDF_SOURCE_CONFIG,
            URL_SOURCE_CONFIG,
        )

        from core.knowledge_catalog import (
            assert_valid_knowledge_catalog,
            get_source_by_id,
        )

        assert_valid_knowledge_catalog()

        write_line("[PASS] Knowledge Catalog validation passed.", report_lines)
        write_line(
            f"[INFO] PDF sources: {len(PDF_SOURCE_CONFIG)}",
            report_lines,
        )
        write_line(
            f"[INFO] URL sources: {len(URL_SOURCE_CONFIG)}",
            report_lines,
        )
        write_line(
            f"[INFO] Chroma directory: {CHROMA_DIR}",
            report_lines,
        )
        write_line(
            f"[INFO] Collection: {COLLECTION_NAME}",
            report_lines,
        )
        write_line(
            f"[INFO] Embedding model: {EMBEDDING_MODEL}",
            report_lines,
        )
        write_line(
            f"[INFO] Chunk size: {CHUNK_SIZE}",
            report_lines,
        )
        write_line(
            f"[INFO] Chunk overlap: {CHUNK_OVERLAP}",
            report_lines,
        )
        write_line(
            f"[INFO] LLM model: {LLM_MODEL}",
            report_lines,
        )

        for source_id in range(1, 10):
            source = get_source_by_id(source_id)

            if source:
                source_name = (
                    source.get("name")
                    or source.get("title")
                    or source.get("source_name")
                    or "Unnamed source"
                )

                write_line(
                    f"[SOURCE {source_id}] {source_name}",
                    report_lines,
                )

        return True

    except Exception as error:
        write_line(
            f"[FAIL] {type(error).__name__}: {error}",
            report_lines,
        )
        return False


def audit_chroma(
    report_lines: list[str],
) -> bool:
    section("5. CHROMA AND CHUNK AUDIT", report_lines)

    try:
        from core.chroma_loader import (
            collection_status,
            get_collection,
            infer_source_id,
            is_reference_chunk,
        )

        status = collection_status()

        write_line(
            f"[PASS] Collection opened: {status['collection_name']}",
            report_lines,
        )
        write_line(
            f"[INFO] Document count: {status['document_count']}",
            report_lines,
        )
        write_line(
            f"[INFO] Database path: {status['database_path']}",
            report_lines,
        )
        write_line(
            f"[INFO] Embedding model: {status['embedding_model']}",
            report_lines,
        )

        collection = get_collection()

        sample_size = min(
            300,
            collection.count(),
        )

        if sample_size == 0:
            write_line("[FAIL] Chroma collection is empty.", report_lines)
            return False

        results = collection.get(
            limit=sample_size,
            include=[
                "documents",
                "metadatas",
            ],
        )

        documents = results.get("documents", []) or []
        metadatas = results.get("metadatas", []) or []

        lengths: list[int] = []
        source_counts: dict[int | None, int] = {}
        reference_count = 0
        empty_count = 0
        missing_page_count = 0

        for index, raw_text in enumerate(documents):
            text = raw_text or ""
            clean_text = " ".join(text.split())

            metadata: dict[str, Any] = (
                metadatas[index] if index < len(metadatas) and metadatas[index] else {}
            )

            if not clean_text:
                empty_count += 1
                continue

            lengths.append(len(clean_text))

            source_id = infer_source_id(metadata)

            source_counts[source_id] = source_counts.get(source_id, 0) + 1

            if is_reference_chunk(clean_text):
                reference_count += 1

            if metadata.get("page") is None and metadata.get("page_number") is None:
                missing_page_count += 1

        write_line(
            f"[INFO] Sampled chunks: {len(documents)}",
            report_lines,
        )
        write_line(
            f"[INFO] Empty chunks: {empty_count}",
            report_lines,
        )
        write_line(
            f"[INFO] Reference-like chunks: {reference_count}",
            report_lines,
        )
        write_line(
            f"[INFO] Missing page metadata: {missing_page_count}",
            report_lines,
        )
        write_line(
            f"[INFO] Source distribution: {source_counts}",
            report_lines,
        )

        if lengths:
            write_line(
                f"[INFO] Minimum chunk characters: {min(lengths)}",
                report_lines,
            )
            write_line(
                f"[INFO] Average chunk characters: {mean(lengths):.1f}",
                report_lines,
            )
            write_line(
                f"[INFO] Maximum chunk characters: {max(lengths)}",
                report_lines,
            )

        passed = True

        if empty_count:
            write_line(
                "[WARN] Empty chunks were found.",
                report_lines,
            )

        if None in source_counts:
            write_line(
                "[WARN] Some chunks have no valid source_id.",
                report_lines,
            )
            passed = False

        if reference_count:
            write_line(
                "[WARN] Reference or bibliography chunks still exist "
                "inside the collection.",
                report_lines,
            )

        return passed

    except Exception as error:
        write_line(
            f"[FAIL] {type(error).__name__}: {error}",
            report_lines,
        )
        return False


def audit_agent_selector(
    report_lines: list[str],
) -> bool:
    section("6. AGENT SELECTOR AUDIT", report_lines)

    try:
        from core.agent_selector import select_agent

        test_cases = [
            (
                "What makes pempek special in Palembang?",
                "food",
            ),
            (
                "Tell me about the history of Sriwijaya.",
                "history",
            ),
            (
                "What is the GDP of Palembang?",
                "economy",
            ),
            (
                "What agriculture and food processing opportunities "
                "exist in Palembang?",
                "investment",
            ),
            (
                "Summarize the food article.",
                "food",
            ),
        ]

        all_passed = True

        for question, expected_category in test_cases:
            selection = select_agent(question)

            passed = selection.category == expected_category

            status = "PASS" if passed else "FAIL"

            write_line(
                f"[{status}] {question}",
                report_lines,
            )
            write_line(
                f"       Expected: {expected_category}",
                report_lines,
            )
            write_line(
                f"       Actual: {selection.category}",
                report_lines,
            )
            write_line(
                f"       Sources: {selection.source_ids}",
                report_lines,
            )
            write_line(
                f"       Search query: {selection.search_query}",
                report_lines,
            )

            if not passed:
                all_passed = False

        return all_passed

    except Exception as error:
        write_line(
            f"[FAIL] {type(error).__name__}: {error}",
            report_lines,
        )
        return False


def audit_retrieval(
    report_lines: list[str],
) -> bool:
    section("7. SEMANTIC RETRIEVAL AUDIT", report_lines)

    try:
        from core.agent_selector import select_agent
        from core.rag_agent import retrieve_context

        questions = [
            "What makes pempek special in Palembang?",
            "Tell me about the history of Sriwijaya.",
            "What is the GDP of Palembang?",
            (
                "What agriculture and food processing opportunities "
                "exist in Palembang?"
            ),
            "Summarize the food article.",
        ]

        all_passed = True

        for question in questions:
            selection = select_agent(question)

            documents = retrieve_context(
                question=question,
                selection=selection,
            )

            write_line("", report_lines)
            write_line(f"QUESTION: {question}", report_lines)
            write_line(
                f"CATEGORY: {selection.category}",
                report_lines,
            )
            write_line(
                f"ALLOWED SOURCES: {selection.source_ids}",
                report_lines,
            )
            write_line(
                f"RETRIEVED CHUNKS: {len(documents)}",
                report_lines,
            )

            if not documents:
                write_line(
                    "[FAIL] No context was retrieved.",
                    report_lines,
                )
                all_passed = False
                continue

            for index, document in enumerate(
                documents,
                start=1,
            ):
                page = document.metadata.get(
                    "page",
                    document.metadata.get(
                        "page_number",
                        "unknown",
                    ),
                )

                preview = " ".join(document.text.split())[:180]

                distance_text = (
                    f"{document.distance:.6f}"
                    if isinstance(document.distance, (int, float))
                    else "not available"
                )

                write_line(
                    (
                        f"  Chunk {index} | "
                        f"Source {document.source_id} | "
                        f"Page {page} | "
                        f"Distance {distance_text}"
                    ),
                    report_lines,
                )
                write_line(
                    f"  Preview: {preview}",
                    report_lines,
                )

                if (
                    document.source_id is not None
                    and selection.source_ids
                    and document.source_id not in selection.source_ids
                ):
                    write_line(
                        "  [WARN] Retrieved source is outside "
                        "the selector's allowed sources.",
                        report_lines,
                    )
                    all_passed = False

        return all_passed

    except Exception as error:
        write_line(
            f"[FAIL] {type(error).__name__}: {error}",
            report_lines,
        )
        return False


def audit_live_rag(
    report_lines: list[str],
) -> bool:
    section("8. OPTIONAL LIVE GROQ RAG AUDIT", report_lines)

    run_live_test = os.getenv(
        "RUN_LIVE_RAG_AUDIT",
        "false",
    ).strip().lower() in {
        "1",
        "true",
        "yes",
    }

    if not run_live_test:
        write_line(
            "[SKIP] Live API test is disabled.",
            report_lines,
        )
        write_line(
            "       Set RUN_LIVE_RAG_AUDIT=true in .env "
            "to test actual Groq answers.",
            report_lines,
        )
        return True

    try:
        from core.rag_agent import generate_rag_answer

        questions = [
            "What makes pempek special in Palembang?",
            (
                "What agriculture and food processing opportunities "
                "exist in Palembang?"
            ),
        ]

        for question in questions:
            response = generate_rag_answer(question)

            write_line("", report_lines)
            write_line(f"QUESTION: {question}", report_lines)
            write_line(
                f"CATEGORY: {response.category}",
                report_lines,
            )
            write_line(
                f"PRIMARY SOURCE: {response.source_id}",
                report_lines,
            )
            write_line(
                f"ALL SOURCES: {response.source_ids}",
                report_lines,
            )
            write_line(
                f"ANSWER: {response.answer}",
                report_lines,
            )

        return True

    except Exception as error:
        write_line(
            f"[FAIL] {type(error).__name__}: {error}",
            report_lines,
        )
        return False


def main() -> None:
    report_lines: list[str] = []

    write_line(
        "PALEMBANG INTELLIGENCE HUB - FINAL RAG AUDIT",
        report_lines,
    )

    checks = {
        "Python syntax": audit_python_files(report_lines),
        "Environment security": audit_environment(report_lines),
        "Git status": audit_git(report_lines),
        "Catalog and config": audit_catalog_and_config(report_lines),
        "Chroma and chunks": audit_chroma(report_lines),
        "Agent selector": audit_agent_selector(report_lines),
        "Semantic retrieval": audit_retrieval(report_lines),
        "Live Groq RAG": audit_live_rag(report_lines),
    }

    section("9. FINAL AUDIT SUMMARY", report_lines)

    passed_count = 0

    for name, passed in checks.items():
        status = "PASS" if passed else "FAIL"

        write_line(
            f"[{status}] {name}",
            report_lines,
        )

        if passed:
            passed_count += 1

    write_line(
        f"\nTOTAL: {passed_count}/{len(checks)} audit sections passed.",
        report_lines,
    )

    if passed_count == len(checks):
        write_line(
            "FINAL STATUS: READY FOR MANUAL REVIEW AND GITHUB PUSH.",
            report_lines,
        )
    else:
        write_line(
            "FINAL STATUS: REVIEW FAILED OR WARNING SECTIONS " "BEFORE GITHUB PUSH.",
            report_lines,
        )

    REPORT_FILE.write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )

    write_line(
        f"\nAudit report saved to:\n{REPORT_FILE}",
    )


if __name__ == "__main__":
    main()
