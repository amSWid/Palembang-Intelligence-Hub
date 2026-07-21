from textwrap import dedent

import streamlit as st

DISCOVER_CARDS = [
    {
        "icon": "🏛️",
        "title": "History",
        "description": (
            "Explore Palembang's long history, legends, kingdoms, "
            "heritage buildings and geographic identity."
        ),
        "question": "Tell me about the history of Palembang.",
    },
    {
        "icon": "🎭",
        "title": "Culture",
        "description": (
            "Discover traditional customs, clothing, language, "
            "arts, dance and local music."
        ),
        "question": "What makes Palembang culture unique?",
    },
    {
        "icon": "🍜",
        "title": "Food",
        "description": (
            "Learn about pempek, tekwan, mie celor and other "
            "traditional Palembang dishes."
        ),
        "question": ("What traditional food should I try in Palembang?"),
    },
    {
        "icon": "📍",
        "title": "Geography",
        "description": (
            "Understand the Musi River, city location, districts "
            "and Palembang's geographic character."
        ),
        "question": ("How does the Musi River influence Palembang?"),
    },
]


def set_discover_question(question: str):
    """
    Queue a Discover question and return to Home.
    """

    st.session_state.pending_question = question
    st.query_params["page"] = "home"


def render_discover_card(
    item: dict,
    index: int,
):
    """
    Render one Discover card.
    """

    with st.container(border=True):
        card_html = dedent(f"""
            <div style="
                min-height:180px;
                padding:8px 5px;
            ">
                <div style="
                    width:44px;
                    height:44px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    margin-bottom:14px;
                    border-radius:13px;
                    background:#edf5ff;
                    font-size:21px;
                ">
                    {item["icon"]}
                </div>

                <div style="
                    color:#254b73;
                    font-size:17px;
                    font-weight:800;
                    margin-bottom:8px;
                ">
                    {item["title"]}
                </div>

                <div style="
                    color:#75879b;
                    font-size:12px;
                    line-height:1.65;
                ">
                    {item["description"]}
                </div>
            </div>
            """).strip()

        st.html(card_html)

        if st.button(
            f'Explore {item["title"]}',
            key=f"discover_card_{index}",
            use_container_width=True,
        ):
            set_discover_question(item["question"])
            st.rerun()


def render_discover_page():
    """
    Render the Discover Palembang page.
    """

    header_html = dedent("""
        <section style="
            padding:58px 46px 20px 46px;
            text-align:center;
        ">
            <div style="
                color:#3978c3;
                font-size:11px;
                font-weight:800;
                text-transform:uppercase;
                letter-spacing:1.2px;
                margin-bottom:12px;
            ">
                Explore the city
            </div>

            <h1 style="
                margin:0;
                font-family:Georgia, serif;
                font-size:48px;
                color:#1d416b;
            ">
                Discover Palembang
            </h1>

            <p style="
                max-width:680px;
                margin:16px auto 0 auto;
                color:#74869a;
                font-size:14px;
                line-height:1.7;
            ">
                Explore the stories, culture, cuisine and geography
                that shape one of Indonesia's oldest cities.
            </p>
        </section>
        """).strip()

    st.html(header_html)

    columns = st.columns(4)

    for index, item in enumerate(DISCOVER_CARDS):
        with columns[index]:
            render_discover_card(
                item=item,
                index=index,
            )

    fact_html = dedent("""
        <section style="
            margin:38px 46px 50px 46px;
            padding:25px;
            border:1px solid #dce8f4;
            border-radius:18px;
            background:
                linear-gradient(
                    135deg,
                    #f4f9ff,
                    #ffffff
                );
        ">
            <div style="
                color:#284d73;
                font-size:18px;
                font-weight:800;
                margin-bottom:8px;
            ">
                ✦ Did You Know?
            </div>

            <div style="
                color:#6f8297;
                font-size:13px;
                line-height:1.75;
            ">
                Palembang developed around the Musi River,
                which has played an important role in transportation,
                trade, settlement and local culture.
            </div>
        </section>
        """).strip()

    st.html(fact_html)
