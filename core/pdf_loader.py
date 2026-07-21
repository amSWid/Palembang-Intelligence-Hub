from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from langchain_community.document_loaders import PyPDFLoader

from config import PDF_FILES
from core.knowledge_catalog import (
    get_source_by_key,
)


def load_single_pdf(
    pdf_path: Path,
    source_key: str,
):
    """
    Load one PDF and attach catalog metadata.
    """

    if not pdf_path.exists():
        print(f"[ERROR] File tidak ditemukan: " f"{pdf_path}")
        return []

    source_config = get_source_by_key(source_key)

    if source_config is None:
        print(f"[ERROR] Sumber tidak ditemukan " f"di Knowledge Catalog: {source_key}")
        return []

    loader = PyPDFLoader(str(pdf_path))

    documents = loader.load()

    source_id = int(source_config["id"])

    title = str(source_config["title"])

    authority = str(
        source_config.get(
            "authority",
            "unknown",
        )
    )

    topics = [
        str(topic)
        for topic in source_config.get(
            "topics",
            [],
        )
    ]

    topics_text = ",".join(topics)

    for document in documents:
        document.metadata.update(
            {
                "source_id": source_id,
                "source_key": source_key,
                "source_name": source_key,
                "source_title": title,
                "source_type": "pdf",
                "source_filename": pdf_path.name,
                "source_path": str(pdf_path),
                "authority": authority,
                "topics": topics_text,
            }
        )

    return documents


def load_all_pdfs():
    """
    Load every enabled PDF from the catalog.
    """

    all_documents = []

    for source_key, pdf_path in PDF_FILES.items():
        print(f"Loading PDF: {source_key}")

        documents = load_single_pdf(
            pdf_path=pdf_path,
            source_key=source_key,
        )

        all_documents.extend(documents)

    print("=" * 60)
    print("Total halaman PDF terbaca: " f"{len(all_documents)}")
    print("=" * 60)

    return all_documents


if __name__ == "__main__":
    docs = load_all_pdfs()

    for document in docs[:3]:
        print(document.metadata)

        print(document.page_content[:500])

        print("-" * 60)
