import base64
from pathlib import Path
from textwrap import dedent

import streamlit as st

from config import FOOD_IMAGE_DIR
from ui.page_ai import (
    queue_page_question,
    render_page_ai,
)

FOOD_ITEMS = [
    {
        "name": "Pempek",
        "filename": "pempek.png",
        "icon": "🐟",
        "description": (
            "Palembang's famous fish cake, commonly served "
            "with a dark sweet, sour and spicy cuko sauce."
        ),
        "question": ("What makes pempek special in Palembang?"),
    },
    {
        "name": "Tekwan",
        "filename": "tekwan.png",
        "icon": "🍲",
        "description": (
            "A light fish dumpling soup usually served "
            "with mushrooms, vermicelli and savory broth."
        ),
        "question": ("What is tekwan and how is it served?"),
    },
    {
        "name": "Mie Celor",
        "filename": "mie_celor.png",
        "icon": "🍜",
        "description": (
            "Thick noodles served in a rich shrimp-based "
            "coconut broth with egg and fresh toppings."
        ),
        "question": ("What makes mie celor unique in Palembang?"),
    },
]


def image_to_base64(
    image_path: Path,
) -> str:
    """
    Convert a local image into a Base64 data URL.
    """

    if not image_path.exists():
        return ""

    extension = image_path.suffix.lower()

    mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }

    mime_type = mime_types.get(
        extension,
        "image/png",
    )

    encoded_image = base64.b64encode(image_path.read_bytes()).decode("utf-8")

    return f"data:{mime_type};" f"base64,{encoded_image}"


def set_food_question(
    question: str,
):
    """
    Queue a food question on the Food page.
    """

    queue_page_question(
        page_key="food",
        question=question,
    )


def render_food_card(
    food: dict,
    index: int,
):
    """
    Render one traditional food card.
    """

    image_path = FOOD_IMAGE_DIR / food["filename"]

    image_data = image_to_base64(image_path)

    if image_data:
        visual_html = dedent(f"""
            <img
                src="{image_data}"
                alt="{food["name"]}"
                style="
                    width:100%;
                    height:210px;
                    object-fit:cover;
                    display:block;
                "
            >
            """).strip()

    else:
        visual_html = dedent(f"""
            <div style="
                width:100%;
                height:210px;
                display:flex;
                align-items:center;
                justify-content:center;
                background:#edf4fb;
                font-size:60px;
            ">
                {food["icon"]}
            </div>
            """).strip()

    with st.container(border=True):
        card_html = dedent(f"""
            <div style="
                overflow:hidden;
                border-radius:15px;
                background:#ffffff;
            ">
                <div style="
                    overflow:hidden;
                    border-radius:13px;
                ">
                    {visual_html}
                </div>

                <div style="
                    padding:17px 5px 9px 5px;
                ">
                    <div style="
                        color:#284d72;
                        font-size:18px;
                        font-weight:800;
                    ">
                        {food["name"]}
                    </div>

                    <div style="
                        color:#77899c;
                        font-size:11px;
                        line-height:1.65;
                        margin-top:8px;
                        min-height:58px;
                    ">
                        {food["description"]}
                    </div>
                </div>
            </div>
            """).strip()

        st.html(card_html)

        if st.button(
            f'Ask about {food["name"]}',
            key=f"food_item_{index}",
            use_container_width=True,
        ):
            set_food_question(food["question"])
            st.rerun()


def render_food_header():
    """
    Render the Food page header.
    """

    header_html = dedent("""
        <section style="
            padding:58px 46px 25px 46px;
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
                Taste the city
            </div>

            <h1 style="
                margin:0;
                font-family:Georgia, serif;
                font-size:48px;
                color:#1d416b;
            ">
                Palembang Food Gallery
            </h1>

            <p style="
                max-width:690px;
                margin:16px auto 0 auto;
                color:#74869a;
                font-size:14px;
                line-height:1.7;
            ">
                Discover traditional Palembang dishes,
                their characteristics and restaurant
                information through the AI assistant.
            </p>
        </section>
        """).strip()

    st.html(header_html)


def render_restaurant_assistant():
    """
    Render restaurant assistant information.
    """

    assistant_html = dedent("""
        <section style="
            margin:36px 46px 20px 46px;
            padding:24px;
            border:1px solid #dce8f4;
            border-radius:18px;
            background:#f7fbff;
        ">
            <div style="
                color:#294d72;
                font-size:18px;
                font-weight:800;
                margin-bottom:9px;
            ">
                Restaurant Address Assistant
            </div>

            <div style="
                color:#74869a;
                font-size:12px;
                line-height:1.75;
            ">
                The food assistant answers questions about
                specific dishes and provides restaurant addresses
                only when that information is supported by the
                Palembang knowledge sources.
            </div>
        </section>
        """).strip()

    st.html(assistant_html)


def render_extra_food_questions():
    """
    Render extra Food question buttons.
    """

    extra_questions = [
        (
            "Food Recommendation",
            ("What traditional Palembang food should " "a first-time visitor try?"),
        ),
        (
            "Restaurant Address",
            ("Where can I find traditional food " "restaurants in Palembang?"),
        ),
        (
            "Food Culture",
            ("How does traditional food reflect " "Palembang culture?"),
        ),
    ]

    question_columns = st.columns(3)

    for index, (
        column,
        item,
    ) in enumerate(
        zip(
            question_columns,
            extra_questions,
        )
    ):
        title, question = item

        with column:
            if st.button(
                title,
                key=f"extra_food_question_{index}",
                use_container_width=True,
            ):
                set_food_question(question)
                st.rerun()

def render_did_you_know():
    """
    Render a dynamic 'Did You Know?' panel
    based on the retrieved Food documents.
    """

    result = st.session_state.get(
        "food_ai_result"
    )

    if result is None:
        return

    documents = getattr(
        result,
        "documents",
        [],
    )

    if not documents:
        return

    text = documents[0].text

    text = " ".join(
        text.split()
    )

    if len(text) > 320:
        text = (
            text[:320]
            .rsplit(" ", 1)[0]
            + "..."
        )

    st.markdown(
        dedent(
            f"""
            <div style="
                margin-top:35px;
                padding:22px;
                border-radius:18px;
                background:linear-gradient(
                    135deg,
                    #ffffff,
                    #f6fbff
                );
                border:1px solid #dce8f4;
            ">

                <div style="
                    font-size:20px;
                    font-weight:700;
                    color:#1f4f7a;
                    margin-bottom:12px;
                ">
                    💡 Did You Know?
                </div>

                <div style="
                    color:#5f7184;
                    line-height:1.8;
                    font-size:14px;
                ">
                    {text}
                </div>

            </div>
            """
        ),
        unsafe_allow_html=True,
    )


def render_food_page():
    """
    Render the complete Palembang Food page.
    """

    render_food_header()

    columns = st.columns(3)

    for index, food in enumerate(FOOD_ITEMS):
        with columns[index]:
            render_food_card(
                food=food,
                index=index,
            )

    # AI answer stays on the Food page.
    render_page_ai(
        page_key="food",
    )

    render_restaurant_assistant()
    render_extra_food_questions()
    render_did_you_know()
