import streamlit as st

EXAMPLE_QUESTIONS = [
    "What makes pempek special in Palembang?",
    "What is the history of Ampera Bridge?",
    "What are Palembang's investment opportunities?",
    "Tell me about Palembang culture and music.",
]


def initialise_search_state():
    """
    Create search session state.
    """

    defaults = {
        "question_input": "",
        "submitted_question": "",
        "pending_question": "",
        "auto_run": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def apply_pending_question():
    """
    Apply queued question before the input widget is created.
    """

    pending_question = st.session_state.get(
        "pending_question",
        "",
    ).strip()

    if not pending_question:
        return

    st.session_state.question_input = pending_question
    st.session_state.submitted_question = pending_question
    st.session_state.auto_run = True
    st.session_state.pending_question = ""


def submit_question():
    """
    Submit the current question.
    """

    question = st.session_state.get(
        "question_input",
        "",
    ).strip()

    if not question:
        return

    st.session_state.submitted_question = question
    st.session_state.auto_run = True


def queue_question(question: str):
    """
    Queue an example question.
    """

    st.session_state.pending_question = question


def render_question_chips():
    """
    Render four example-question buttons.
    """

    columns = st.columns(4)

    for index, question in enumerate(EXAMPLE_QUESTIONS):
        with columns[index]:
            if st.button(
                question,
                key=f"example_question_{index}",
                use_container_width=True,
            ):
                queue_question(question)
                st.rerun()


def render_search():
    """
    Render one unified AI search bar.
    """

    initialise_search_state()
    apply_pending_question()

    st.html("""
        <div class="unified-search-start"></div>
        """)

    input_column, language_column, button_column = st.columns(
        [12, 0.7, 0.9],
        vertical_alignment="center",
        gap="small",
    )

    with input_column:
        st.text_input(
            label="Ask Palembang Intelligence",
            placeholder="⌕  Ask Palembang Intelligence",
            key="question_input",
            on_change=submit_question,
            label_visibility="collapsed",
        )

    with language_column:
        st.html("""
            <div class="unified-search-language">
                EN
            </div>
            """)

    with button_column:
        if st.button(
            "➤",
            key="search_submit_button",
            use_container_width=True,
            help="Ask Palembang Intelligence",
        ):
            submit_question()
            st.rerun()

    st.html("""
        <div class="search-helper-row">
            <span>✦ Try an example question below</span>
            <span>Private local knowledge assistant</span>
        </div>
        """)

    render_question_chips()


def get_submitted_question() -> str:
    """
    Return the latest submitted question.
    """

    initialise_search_state()

    return st.session_state.get(
        "submitted_question",
        "",
    )


def clear_submitted_question():
    """
    Clear submitted question after processing.
    """

    st.session_state.submitted_question = ""
    st.session_state.auto_run = False
