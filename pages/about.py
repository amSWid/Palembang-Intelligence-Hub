import base64
import random
from pathlib import Path
from textwrap import dedent

import streamlit as st

from config import IMAGE_DIR

# =========================================================
# ABOUT PAGE CONTENT
# =========================================================

PIH_QUOTES = [
    (
        "Technology becomes meaningful when it amplifies "
        "human purpose, not when it replaces human presence."
    ),
    "Technology serves purpose.",
    "Purpose protects identity.",
    "Identity creates opportunity.",
    "Intelligence connects them.",
    "Local knowledge becomes stronger when it is accessible.",
]


PIH_PILLARS = [
    {
        "icon": "✦",
        "title": "Human-Centered Technology",
        "description": (
            "Technology should amplify human curiosity, "
            "knowledge and purpose — not replace human presence."
        ),
    },
    {
        "icon": "🏛️",
        "title": "Local Identity",
        "description": (
            "PIH connects Palembang's heritage, culture, food "
            "and local identity through digital discovery."
        ),
    },
    {
        "icon": "📈",
        "title": "Local Opportunity",
        "description": (
            "The platform helps connect local knowledge, "
            "business visibility and economic opportunity."
        ),
    },
    {
        "icon": "🧠",
        "title": "Intelligent Discovery",
        "description": (
            "AI and trusted knowledge sources help people "
            "explore Palembang with greater context."
        ),
    },
]


# =========================================================
# IMAGE HELPERS
# =========================================================


def file_to_base64(
    file_path: Path,
) -> str:
    """
    Convert a local file to Base64.
    """

    if not file_path.exists():
        return ""

    return base64.b64encode(file_path.read_bytes()).decode("utf-8")


def image_to_data_url(
    image_path: Path,
) -> str:
    """
    Convert a local image to a Base64 data URL.
    """

    if not image_path.exists():
        return ""

    mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }

    mime_type = mime_types.get(
        image_path.suffix.lower(),
        "image/png",
    )

    encoded_image = file_to_base64(image_path)

    if not encoded_image:
        return ""

    return f"data:{mime_type};" f"base64,{encoded_image}"


def find_first_existing_image(
    filenames: list[str],
) -> Path | None:
    """
    Return the first available image from IMAGE_DIR.
    """

    for filename in filenames:
        image_path = IMAGE_DIR / filename

        if image_path.exists():
            return image_path

    return None


# =========================================================
# SESSION STATE
# =========================================================


def initialise_about_state():
    """
    Prepare About page interaction state.
    """

    if "about_robot_paused" not in st.session_state:
        st.session_state.about_robot_paused = False

    if "about_quote" not in st.session_state:
        st.session_state.about_quote = PIH_QUOTES[0]


def toggle_about_robot():
    """
    Pause or restart the robot.

    A new quote appears whenever the robot is paused.
    """

    current_status = st.session_state.about_robot_paused

    st.session_state.about_robot_paused = not current_status

    if not current_status:
        available_quotes = [
            quote for quote in PIH_QUOTES if quote != st.session_state.about_quote
        ]

        st.session_state.about_quote = random.choice(available_quotes)


# =========================================================
# SHARED CSS
# =========================================================


def render_about_styles():
    """
    Render CSS used by the About page.
    """

    about_css = dedent("""
        <style>
            /* ==============================================
               ABOUT HERO
               ============================================== */

            .about-hero {
                position: relative;
                min-height: 520px;
                margin: 38px 34px 28px 34px;
                overflow: hidden;
                border: 1px solid #dce8f4;
                border-radius: 26px;
                background: #f6faff;
                box-shadow:
                    0 18px 48px
                    rgba(42, 84, 126, 0.07);
            }

            .about-hero-background {
                position: absolute;
                inset: 0;
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                transform: scale(1.02);
            }

            .about-hero-overlay {
                position: absolute;
                inset: 0;
                background:
                    linear-gradient(
                        90deg,
                        rgba(247, 251, 255, 0.99) 0%,
                        rgba(247, 251, 255, 0.96) 38%,
                        rgba(240, 248, 255, 0.75) 68%,
                        rgba(231, 243, 255, 0.58) 100%
                    );
            }

            .about-hero-light {
                position: absolute;
                top: -150px;
                right: -120px;
                width: 520px;
                height: 520px;
                border-radius: 50%;
                background:
                    radial-gradient(
                        circle,
                        rgba(80, 156, 235, 0.18),
                        rgba(80, 156, 235, 0)
                    );
                filter: blur(12px);
            }

            .about-hero-content {
                position: relative;
                z-index: 4;
                display: grid;
                grid-template-columns:
                    minmax(0, 1.15fr)
                    minmax(300px, 0.85fr);
                min-height: 520px;
                padding: 60px 58px 48px 58px;
            }

            .about-hero-copy {
                display: flex;
                flex-direction: column;
                justify-content: center;
                max-width: 680px;
            }

            .about-eyebrow {
                color: #3277c8;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 1.3px;
                text-transform: uppercase;
            }

            .about-hero-title {
                margin: 14px 0 19px 0;
                color: #173f6b;
                font-family: Georgia, serif;
                font-size: clamp(52px, 5.2vw, 76px);
                line-height: 0.98;
                letter-spacing: -2px;
            }

            .about-hero-title span {
                display: block;
                color: #2e73cb;
            }

            .about-hero-description {
                max-width: 630px;
                color: #647d98;
                font-size: 14px;
                line-height: 1.85;
            }

            .about-quote {
                max-width: 610px;
                margin-top: 30px;
                padding: 4px 0 4px 22px;
                border-left: 3px solid #3a7fd1;
            }

            .about-quote-text {
                color: #174d85;
                font-family: Georgia, serif;
                font-size: 19px;
                font-style: italic;
                line-height: 1.6;
            }

            /* ==============================================
               ROBOT AREA
               ============================================== */

            .about-robot-area {
                position: relative;
                min-height: 400px;
            }

            .about-robot-image {
                position: absolute;
                right: -34px;
                bottom: -48px;
                z-index: 4;

                width: 275px;
                max-height: 580px;
                object-fit: contain;

                transform-origin: center bottom;

                filter:
                    drop-shadow(
                        0 16px 15px
                        rgba(20, 55, 95, 0.24)
                    )
                    drop-shadow(
                        0 34px 28px
                        rgba(20, 55, 95, 0.18)
                    );

                transition:
                    transform 0.3s ease,
                    filter 0.3s ease;
            }

            .about-robot-moving {
                animation:
                    aboutRobotFloat
                    3.5s ease-in-out
                    infinite;
            }

            .about-robot-paused {
                animation: none;
                transform: translateY(0) rotate(0deg);
            }

            .about-robot-glow {
                position: absolute;
                right: -48px;
                bottom: -55px;
                z-index: 2;

                width: 315px;
                height: 95px;
                border-radius: 50%;

                background:
                    radial-gradient(
                        ellipse,
                        rgba(20, 59, 98, 0.28) 0%,
                        rgba(38, 101, 166, 0.14) 43%,
                        rgba(38, 101, 166, 0) 76%
                    );

                filter: blur(11px);
                transform: perspective(500px) rotateX(68deg);
            }

            @keyframes aboutRobotFloat {
                0%,
                100% {
                    transform:
                        perspective(700px)
                        translateY(0)
                        rotateY(-4deg)
                        rotateZ(-0.5deg)
                        scale(1);
                }

                50% {
                    transform:
                        perspective(700px)
                        translateY(-10px)
                        rotateY(4deg)
                        rotateZ(0.5deg)
                        scale(1.015);
                }
            }

            /* ==============================================
               OTHER ABOUT SECTIONS
               ============================================== */

            .about-section-label {
                color: #3477c8;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 1.25px;
                text-transform: uppercase;
            }

            .about-serif {
                font-family: Georgia, serif;
            }

            .about-soft-card {
                border: 1px solid #dce8f4;
                border-radius: 24px;
                background: rgba(255, 255, 255, 0.88);
                box-shadow:
                    0 16px 45px
                    rgba(55, 92, 135, 0.07);
                backdrop-filter: blur(12px);
            }

            .about-pillar-card {
                min-height: 190px;
                padding: 24px;
                border: 1px solid #dce8f4;
                border-radius: 21px;
                background: rgba(255, 255, 255, 0.92);
                box-shadow:
                    0 12px 30px
                    rgba(55, 92, 135, 0.05);
                transition:
                    transform 0.25s ease,
                    box-shadow 0.25s ease,
                    border-color 0.25s ease;
            }

            .about-pillar-card:hover {
                transform: translateY(-5px);
                border-color: #b9d4f2;
                box-shadow:
                    0 18px 38px
                    rgba(55, 92, 135, 0.10);
            }

            .about-mini-icon {
                width: 43px;
                height: 43px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 17px;
                border-radius: 14px;
                background: #edf5ff;
                font-size: 19px;
            }

            .about-purpose-line {
                margin: 9px 0;
                color: #174d85;
                font-family: Georgia, serif;
                font-size: clamp(22px, 2.2vw, 31px);
                font-style: italic;
                line-height: 1.35;
            }

            @media (max-width: 850px) {
                .about-hero-content {
                    grid-template-columns: 1fr;
                    padding: 45px 30px 25px 30px;
                }

                .about-robot-area {
                    min-height: 280px;
                }

                .about-robot-image {
                    right: 50%;
                    bottom: -35px;
                    width: 220px;
                    transform: translateX(50%);
                }

                .about-robot-glow {
                    right: 50%;
                    bottom: -42px;
                    transform:
                        translateX(50%)
                        perspective(500px)
                        rotateX(68deg);
                }

                .about-exists-grid,
                .about-purpose-grid {
                    grid-template-columns: 1fr !important;
                }
            }
                    </style>
                    """).strip()

    st.html(about_css)


# =========================================================
# SECTION 1 — HERO
# =========================================================


def render_about_hero():
    """
    Render the About hero using the Ampera Bridge
    as a subtle background and PIH as a moving guide.
    """

    ampera_candidates = [
        IMAGE_DIR / "ampera_bridge.png",
        IMAGE_DIR / "ampera_bridge.jpg",
        IMAGE_DIR / "ampera_bridge.jpeg",
        IMAGE_DIR / "ampera_bridge.webp",
    ]

    ampera_path = next(
        (image_path for image_path in ampera_candidates if image_path.exists()),
        None,
    )

    robot_path = IMAGE_DIR / "robot_palembang.png"

    ampera_data = image_to_data_url(ampera_path) if ampera_path is not None else ""

    robot_data = image_to_data_url(robot_path)

    if ampera_data:
        background_style = f"background-image:url('{ampera_data}');"
    else:
        background_style = (
            "background:" "linear-gradient(" "135deg," "#f9fcff," "#eaf4ff" ");"
        )

    robot_class = (
        "about-robot-paused"
        if st.session_state.about_robot_paused
        else "about-robot-moving"
    )

    if robot_data:
        robot_visual = dedent(f"""
            <img
                src="{robot_data}"
                alt="Palembang Intelligence Hub robot"
                class="
                    about-robot-image
                    {robot_class}
                "
            >
            """).strip()

    else:
        robot_visual = dedent(f"""
            <div
                class="{robot_class}"
                style="
                    position:relative;
                    z-index:3;
                    margin:0 55px 55px 0;
                    font-size:140px;
                "
            >
                🤖
            </div>
            """).strip()

    hero_html = dedent(f"""
        <section class="about-hero">

            <div
                class="about-hero-background"
                style="{background_style}"
            ></div>

            <div class="about-hero-overlay"></div>
            <div class="about-hero-light"></div>

            <div class="about-hero-content">

                <div class="about-hero-copy">

                    <div class="about-eyebrow">
                        Why Palembang Intelligence Hub (PIH)
                    </div>

                    <h1 class="about-hero-title">
                        Technology

                        <span>
                            With Purpose
                        </span>
                    </h1>

                    <div class="about-hero-description">
                        Palembang Intelligence Hub is a
                        human-centered digital platform designed
                        to make Palembang's heritage, culture,
                        food, local businesses and economic
                        identity easier to discover, understand
                        and connect with opportunity.
                    </div>

                    <div class="about-quote">
                        <div class="about-quote-text">
                            “{st.session_state.about_quote}”
                        </div>
                    </div>

                </div>

                <div class="about-robot-area">

                    <div class="about-robot-glow"></div>

                    {robot_visual}

                </div>

            </div>

        </section>
        """).strip()

    st.html(hero_html)

# =========================================================
# SECTION 2 — WHY PIH EXISTS
# =========================================================


def render_why_pih_exists():
    """
    Render the Why PIH Exists section.
    """

    section_html = dedent("""
        <section
            class="about-page"
            style="
                margin:72px 66px 28px 66px;
            "
        >
            <div
                class="about-exists-grid"
                style="
                    display:grid;
                    grid-template-columns:0.75fr 1.25fr;
                    gap:60px;
                    align-items:start;
                "
            >
                <div>
                    <div class="about-section-label">
                        The reason behind the platform
                    </div>

                    <h2
                        class="about-serif"
                        style="
                            margin:13px 0 0 0;
                            color:#173f6b;
                            font-size:42px;
                            line-height:1.08;
                        "
                    >
                        Why PIH Exists
                    </h2>
                </div>

                <div
                    style="
                        padding-top:5px;
                    "
                >
                    <p
                        style="
                            margin:0;
                            color:#607993;
                            font-size:16px;
                            line-height:1.95;
                        "
                    >
                        Palembang is more than a destination.
                        It is a city shaped by history, rivers,
                        culture, food, people and economic
                        potential. Palembang Intelligence Hub
                        was created to connect these pieces
                        through accessible digital technology.
                        The goal is not simply to provide
                        information, but to help people discover
                        more, understand better and see new
                        possibilities within a local place.
                    </p>
                </div>
            </div>
        </section>
        """).strip()

    st.html(section_html)


# =========================================================
# SECTION 3 — FOUR PILLARS
# =========================================================


def render_pih_pillars():
    """
    Render four PIH principle cards.
    """

    st.html(dedent("""
            <section
                class="about-page"
                style="
                    margin:72px 40px 20px 40px;
                "
            >
                <div
                    style="
                        text-align:center;
                        margin-bottom:30px;
                    "
                >
                    <div class="about-section-label">
                        What guides PIH
                    </div>

                    <h2
                        class="about-serif"
                        style="
                            margin:11px 0 0 0;
                            color:#173f6b;
                            font-size:39px;
                        "
                    >
                        Built Around People and Place
                    </h2>
                </div>
            </section>
            """).strip())

    columns = st.columns(4)

    for column, pillar in zip(
        columns,
        PIH_PILLARS,
    ):
        with column:
            pillar_html = dedent(f"""
                <div class="about-pillar-card">
                    <div class="about-mini-icon">
                        {pillar["icon"]}
                    </div>

                    <div
                        style="
                            color:#204a76;
                            font-size:15px;
                            font-weight:800;
                            line-height:1.4;
                        "
                    >
                        {pillar["title"]}
                    </div>

                    <div
                        style="
                            margin-top:11px;
                            color:#69819a;
                            font-size:11px;
                            line-height:1.75;
                        "
                    >
                        {pillar["description"]}
                    </div>
                </div>
                """).strip()

            st.html(pillar_html)


# =========================================================
# SECTION 4 — PURPOSE STATEMENT
# =========================================================


def render_purpose_statement():
    """
    Render the PIH philosophy statement.
    """

    statement_html = dedent("""
        <section
            class="about-page"
            style="
                margin:78px 66px;
                padding:56px 20px;
                border-top:1px solid #d9e6f3;
                border-bottom:1px solid #d9e6f3;
                text-align:center;
            "
        >
            <div class="about-purpose-line">
                Technology serves Purpose.
            </div>

            <div class="about-purpose-line">
                Purpose protects Identity.
            </div>

            <div class="about-purpose-line">
                Identity creates Opportunity.
            </div>

            <div class="about-purpose-line">
                Intelligence connects them.
            </div>
        </section>
        """).strip()

    st.html(statement_html)


# =========================================================
# SECTION 5 — MISSION, VISION & PRINCIPLES
# =========================================================


def render_mission_and_principles():
    """
    Render final Mission, Vision and Core Principles section.
    """

    final_html = dedent("""
        <section
            class="about-page"
            style="
                margin:24px 66px 70px 66px;
            "
        >
            <div
                class="about-purpose-grid"
                style="
                    display:grid;
                    grid-template-columns:1fr 1fr;
                    gap:18px;
                "
            >
                <div
                    class="about-soft-card"
                    style="
                        padding:32px;
                    "
                >
                    <h3
                        style="
                            margin:0 0 20px 0;
                            color:#174a7b;
                            font-size:19px;
                            font-weight:800;
                        "
                    >
                        Mission &amp; Vision
                    </h3>

                    <div
                        style="
                            color:#3472b3;
                            font-size:11px;
                            font-weight:800;
                        "
                    >
                        Mission
                    </div>

                    <p
                        style="
                            margin:7px 0 23px 0;
                            color:#69819a;
                            font-size:12px;
                            line-height:1.75;
                        "
                    >
                        To make Palembang more visible, more
                        connected and more economically active
                        through human-centered digital technology.
                    </p>

                    <div
                        style="
                            color:#3472b3;
                            font-size:11px;
                            font-weight:800;
                        "
                    >
                        Vision
                    </div>

                    <p
                        style="
                            margin:7px 0 0 0;
                            color:#69819a;
                            font-size:12px;
                            line-height:1.75;
                        "
                    >
                        To grow PIH into a trusted and scalable
                        intelligence platform that begins with
                        Palembang and expands to other Indonesian
                        cities.
                    </p>
                </div>

                <div
                    class="about-soft-card"
                    style="
                        padding:32px;
                    "
                >
                    <h3
                        style="
                            margin:0 0 20px 0;
                            color:#174a7b;
                            font-size:19px;
                            font-weight:800;
                        "
                    >
                        Core Principles
                    </h3>

                    <div style="
                        margin-bottom:18px;
                    ">
                        <div style="
                            color:#3472b3;
                            font-size:11px;
                            font-weight:800;
                        ">
                            Human-Centered Technology
                        </div>

                        <div style="
                            margin-top:5px;
                            color:#69819a;
                            font-size:11px;
                        ">
                            Technology should serve human purpose.
                        </div>
                    </div>

                    <div style="
                        margin-bottom:18px;
                    ">
                        <div style="
                            color:#3472b3;
                            font-size:11px;
                            font-weight:800;
                        ">
                            Local Economic Empowerment
                        </div>

                        <div style="
                            margin-top:5px;
                            color:#69819a;
                            font-size:11px;
                        ">
                            Digital visibility should create opportunity.
                        </div>
                    </div>

                    <div style="
                        margin-bottom:18px;
                    ">
                        <div style="
                            color:#3472b3;
                            font-size:11px;
                            font-weight:800;
                        ">
                            Cultural Preservation
                        </div>

                        <div style="
                            margin-top:5px;
                            color:#69819a;
                            font-size:11px;
                        ">
                            Local identity should remain visible
                            and accessible.
                        </div>
                    </div>

                    <div>
                        <div style="
                            color:#3472b3;
                            font-size:11px;
                            font-weight:800;
                        ">
                            Practical Innovation
                        </div>

                        <div style="
                            margin-top:5px;
                            color:#69819a;
                            font-size:11px;
                        ">
                            Innovation should create meaningful value.
                        </div>
                    </div>
                </div>
            </div>

            <div
                style="
                    margin-top:54px;
                    text-align:center;
                "
            >
                <div
                    class="about-serif"
                    style="
                        color:#173f6b;
                        font-size:31px;
                    "
                >
                    Explore Palembang with greater context.
                </div>

                <a
                    href="?page=home"
                    target="_self"
                    style="
                        display:inline-flex;
                        align-items:center;
                        justify-content:center;
                        margin-top:20px;
                        padding:12px 24px;
                        border-radius:999px;
                        background:#2f73ca;
                        color:#ffffff;
                        font-size:12px;
                        font-weight:800;
                        text-decoration:none;
                        box-shadow:
                            0 10px 25px
                            rgba(47, 115, 202, 0.19);
                    "
                >
                    Start Exploring →
                </a>
            </div>
                    
           
            <div
                style="
                    margin-top:60px;
                    padding-top:28px;
                    border-top:1px solid #e6edf5;
                    text-align:center;
                    color:#7A8797;
                    font-size:11px;
                    line-height:1.8;
                "
            >

                <div
                    style="
                        color:#4f6780;
                        font-size:12px;
                        font-weight:700;
                        margin-bottom:10px;
                    "
                >
                    Creative Credits
                </div>

                <div>
                    Original robot, visual design, background images,
                    and music by <strong>S. Widjaja</strong>.
                </div>

                <div
                    style="
                        margin-top:10px;
                        font-size:10px;
                        color:#9AA8B6;
                    "
                >
                    © 2026 S. Widjaja. All rights reserved.
                </div>

            </div>


        </section>
        """).strip()

    st.html(final_html)


# =========================================================
# MAIN PAGE
# =========================================================


def render_about_page():
    """
    Render the complete About page.
    """

    initialise_about_state()
    render_about_styles()

    # Section 1
    render_about_hero()

    # Section 2
    render_why_pih_exists()

    # Section 3
    render_pih_pillars()

    # Section 4
    render_purpose_statement()

    # Section 5
    render_mission_and_principles()
