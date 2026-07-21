import streamlit as st

from core.rag_agent import (
    RAGResponse,
    generate_rag_answer,
)
from result import (
    render_ai_result,
    render_error_result,
)


def initialise_page_ai_state(
    page_key: str,
):
    """
    Prepare separate AI state for one page.
    """

    defaults = {
        f"{page_key}_ai_question": "",
        f"{page_key}_ai_result": None,
        f"{page_key}_ai_run": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def queue_page_question(
    page_key: str,
    question: str,
):
    """
    Queue a question for the active page.
    """

    initialise_page_ai_state(page_key)

    st.session_state[f"{page_key}_ai_question"] = question

    st.session_state[f"{page_key}_ai_result"] = None

    st.session_state[f"{page_key}_ai_run"] = True


def get_page_question(
    page_key: str,
) -> str:
    """
    Return the queued question for one page.
    """

    initialise_page_ai_state(page_key)

    return st.session_state.get(
        f"{page_key}_ai_question",
        "",
    )


def clear_page_ai(
    page_key: str,
):
    """
    Clear one page's AI state.
    """

    st.session_state[f"{page_key}_ai_question"] = ""

    st.session_state[f"{page_key}_ai_result"] = None

    st.session_state[f"{page_key}_ai_run"] = False


def run_page_ai(
    page_key: str,
) -> RAGResponse | None:
    """
    Run RAG once for the active page.
    """

    initialise_page_ai_state(page_key)

    question = get_page_question(page_key)

    should_run = st.session_state.get(
        f"{page_key}_ai_run",
        False,
    )

    cached_result = st.session_state.get(f"{page_key}_ai_result")

    if not question:
        return None

    if cached_result is not None:
        return cached_result

    if not should_run:
        return None

    with st.spinner("Searching trusted Palembang knowledge..."):
        result = generate_rag_answer(question)

    st.session_state[f"{page_key}_ai_result"] = result

    st.session_state[f"{page_key}_ai_run"] = False

    return result


def render_page_ai(
    page_key: str,
):
    """
    Run and display the AI answer on the active page.
    """

    initialise_page_ai_state(page_key)

    question = get_page_question(page_key)

    if not question:
        return

    try:
        result = run_page_ai(page_key)

        if result is None:
            return

        render_ai_result(
            question=result.question,
            answer=result.answer,
            source_id=result.source_id,
            documents=result.documents,
        )

    except Exception as error:
        render_error_result(str(error))
