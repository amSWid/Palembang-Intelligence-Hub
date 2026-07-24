from textwrap import dedent
import base64
from pathlib import Path

import streamlit as st

from config import FOOD_IMAGE_DIR
from hero import render_hero

from search import (
    get_submitted_question,
    clear_submitted_question,
    render_search,
)

from result import(
    render_ai_result,
    render_loading_result,
    render_error_result
)

from core.rag_agent import generate_rag_answer

def image_to_base64(image_path: Path) -> str:
    """
    Convert a local image file into a Base64 data URL.
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


def render_ecosystem():
    """
    Render the Palembang Travel Ecosystem section.
    """

    ecosystem_items = [
        ("🏨", "Hotels"),
        ("🍴", "Restaurants"),
        ("🚌", "Transportation"),
        ("🎡", "Attractions"),
        ("🛍️", "Shopping"),
        ("🧑‍💼", "Tour Guide"),
        ("♡", "Health"),
        ("•••", "More"),
    ]

    ecosystem_html = "".join(dedent(f"""
            <div class="ecosystem-item">
                <div class="ecosystem-icon">
                    {icon}
                </div>

                <div class="ecosystem-label">
                    {label}
                </div>
            </div>
            """).strip() for icon, label in ecosystem_items)

    section_html = dedent(f"""
        <section class="section-container">

            <div class="section-header">

                <div>
                    <h2 class="section-title">
                        Palembang Travel Ecosystem
                    </h2>

                    <div class="section-subtitle">
                        Essential city services for visitors,
                        residents and investors.
                    </div>
                </div>

                <div class="section-link">
                    Explore all →
                </div>

            </div>

            <div class="ecosystem-grid">
                {ecosystem_html}
            </div>

        </section>
        """).strip()

    st.html(section_html)


def restaurant_image_html(
    filename: str,
    alt_text: str,
) -> str:
    """
    Return an HTML image element for a restaurant item.
    """

    image_path = FOOD_IMAGE_DIR / filename

    image_data = image_to_base64(image_path)

    if image_data:
        return dedent(f"""
            <img
                src="{image_data}"
                alt="{alt_text}"
            >
            """).strip()

    return dedent("""
        <div style="
            width:100%;
            height:100%;
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:20px;
        ">
            🍽️
        </div>
        """).strip()


def render_restaurant_item(
    filename: str,
    name: str,
    details: str,
    distance: str,
) -> str:
    """
    Build one restaurant recommendation item.
    """

    image_html = restaurant_image_html(
        filename=filename,
        alt_text=name,
    )

    return dedent(f"""
        <div class="restaurant-item">

            <div class="restaurant-thumb">
                {image_html}
            </div>

            <div>
                <div class="restaurant-name">
                    {name}
                </div>

                <div class="restaurant-details">
                    {details}
                </div>

                <div class="restaurant-rating">
                    ★ 4.8 &nbsp; • &nbsp; Local favorite
                </div>
            </div>

            <div class="restaurant-distance">
                {distance}
            </div>

        </div>
        """).strip()


def render_lower_content():
    """
    Render welcome and restaurant recommendation cards.
    """

    restaurants_html = "".join(
        [
            render_restaurant_item(
                filename="pempek.png",
                name="Pempek Nony 168",
                details=("Pempek, tekwan and traditional " "Palembang dishes."),
                distance="2.1 km",
            ),
            render_restaurant_item(
                filename="mie_celor.png",
                name="Mie Celor 26 Ilir",
                details=("Traditional thick noodle soup " "with a rich shrimp broth."),
                distance="2.8 km",
            ),
            render_restaurant_item(
                filename="tekwan.png",
                name="Tekwan Local Kitchen",
                details=(
                    "Fresh fish dumpling soup served " "with mushrooms and vermicelli."
                ),
                distance="3.1 km",
            ),
        ]
    )

    lower_html = dedent(f"""
        <section class="content-grid">

            <div class="info-card">

                <div class="info-card-title">
                    Welcome!
                </div>

                
            </div>

            <div class="recommendation-card">

                <div class="section-header">

                    <div>
                        <h2 class="section-title">
                            Best Traditional Food in Palembang
                        </h2>

                        <div class="section-subtitle">
                            Recommended places for authentic
                            Palembang cuisine.
                        </div>
                    </div>

                    <div class="section-link">
                        See more →
                    </div>

                </div>

                <div class="recommendation-layout">

                    <div class="restaurant-list">
                        {restaurants_html}
                    </div>

                    <div class="map-panel">

                        <div class="map-grid"></div>

                        <div
                            class="map-road"
                            style="
                                width:230px;
                                left:15px;
                                top:44px;
                                transform:rotate(20deg);
                            "
                        ></div>

                        <div
                            class="map-road"
                            style="
                                width:210px;
                                left:25px;
                                top:102px;
                                transform:rotate(-18deg);
                            "
                        ></div>

                        <div
                            class="map-road"
                            style="
                                width:180px;
                                left:80px;
                                top:27px;
                                transform:rotate(73deg);
                            "
                        ></div>

                        <div
                            class="map-marker"
                            style="
                                left:53px;
                                top:42px;
                            "
                        >
                            <span>1</span>
                        </div>

                        <div
                            class="map-marker"
                            style="
                                left:145px;
                                top:74px;
                            "
                        >
                            <span>2</span>
                        </div>

                        <div
                            class="map-marker"
                            style="
                                right:45px;
                                top:35px;
                            "
                        >
                            <span>3</span>
                        </div>

                        <div class="map-estimate">

                            <div class="estimate-title">
                                Estimated Budget Per Person
                            </div>

                            <div class="estimate-row">
                                <span>Meals</span>
                                <strong>IDR 150,000</strong>
                            </div>

                            <div class="estimate-row">
                                <span>Transportation</span>
                                <strong>IDR 80,000</strong>
                            </div>

                            <div class="estimate-row">
                                <span>Attractions</span>
                                <strong>IDR 100,000</strong>
                            </div>

                            <div class="estimate-row">
                                <span>Total estimate</span>
                                <strong>IDR 330,000</strong>
                            </div>

                        </div>

                    </div>

                </div>

            </div>

        </section>
        """).strip()

    st.html(lower_html)


def render_home_page():
    """
    Main homepage with AI RAG.
    """

    render_hero()

    render_search()

    question = get_submitted_question()

    if question:

        with st.spinner("Searching Palembang knowledge..."):

            try:

                result = generate_rag_answer(question)

                render_ai_result(
                    question=question,
                    answer=result.answer,
                    source_id=result.source_id,
                    documents=result.documents,
                )

            except Exception as error:

                render_error_result(str(error))

        clear_submitted_question()

    render_ecosystem()

    render_lower_content()
