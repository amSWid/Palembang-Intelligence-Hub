"""
=========================================================
Palembang Intelligence Hub
About Page

Purpose:
- Explain the philosophy behind PIH
- Present the PIH framework
- Connect technology with local identity and opportunity
- Provide interactive explanation popups

Author  : S. Widjaja
Version : 1.0
=========================================================
"""

import streamlit as st

# =========================================================
# PIH FRAMEWORK
# =========================================================

PROJECT_FEATURES = [
    {
        "icon": "🌍",
        "title": "Human-Centered Technology",
        "description": (
            "Technology should amplify human curiosity, "
            "knowledge and purpose — not replace human presence."
        ),
        "popup_title": "Technology With Purpose",
        "popup_quote": (
            "Technology becomes meaningful when it amplifies "
            "human purpose, not when it replaces human presence."
        ),
        "popup_body": (
            "PIH uses technology to make knowledge easier to explore, "
            "understand and connect with people. The purpose is not to "
            "replace human curiosity or local experience, but to amplify them."
        ),
        "framework": "Technology serves Purpose.",
    },
    {
        "icon": "🏛️",
        "title": "Local Identity",
        "description": (
            "PIH connects Palembang's heritage, culture, food "
            "and local identity through digital discovery."
        ),
        "popup_title": "Discover the City Behind the Map",
        "popup_quote": ("A city is more than its location."),
        "popup_body": (
            "PIH explores Palembang through its history, culture, "
            "food, music, geography and tourism. Local identity is "
            "not simply something to preserve. It is something to "
            "understand, share and keep alive."
        ),
        "framework": "Purpose protects Identity.",
    },
    {
        "icon": "📈",
        "title": "Local Opportunity",
        "description": (
            "The platform helps connect local knowledge, "
            "business visibility and economic opportunity."
        ),
        "popup_title": "From Identity to Opportunity",
        "popup_quote": ("What is understood can become visible."),
        "popup_body": (
            "PIH connects local identity with economic context, "
            "including GDP, growth, UMKM, agriculture, investment "
            "and business opportunity. Greater visibility can help "
            "local potential become easier to discover."
        ),
        "framework": "Identity creates Opportunity.",
    },
    {
        "icon": "🧠",
        "title": "Intelligent Discovery",
        "description": (
            "AI and trusted knowledge sources help people "
            "explore Palembang with greater context."
        ),
        "popup_title": "How PIH Finds an Answer",
        "popup_quote": ("Intelligence connects knowledge with curiosity."),
        "popup_body": (
            "A question is classified by topic. Relevant information "
            "is retrieved from trusted local knowledge sources. "
            "The retrieved context is then used to prepare a focused "
            "answer supported by source evidence."
        ),
        "framework": "Intelligence connects them.",
    },
]


# =========================================================
# INITIALISE ABOUT STATE
# =========================================================


def initialise_about_state():
    """
    Initialise About page session state.
    """

    if "selected_feature" not in st.session_state:

        st.session_state.selected_feature = None


# =========================================================
# FEATURE POPUP
# =========================================================


@st.dialog(
    "PIH Framework",
    width="large",
)
def render_feature_popup(
    feature: dict,
):
    """
    Render the selected framework feature
    inside a centered Streamlit dialog.
    """

    st.markdown(
        f"""
        <div style="
            text-align:center;
            padding:10px 18px 18px 18px;
        ">

            <div style="
                font-size:42px;
                margin-bottom:12px;
            ">
                {feature["icon"]}
            </div>

            <div style="
                color:#294d72;
                font-family:Georgia, serif;
                font-size:28px;
                font-weight:700;
                margin-bottom:18px;
            ">
                {feature["popup_title"]}
            </div>

            <div style="
                color:#294d72;
                font-family:Georgia, serif;
                font-size:22px;
                font-style:italic;
                line-height:1.55;
                margin:0 auto 22px auto;
                max-width:700px;
            ">
                “{feature["popup_quote"]}”
            </div>

            <div style="
                color:#74869a;
                font-size:13px;
                line-height:1.85;
                text-align:left;
                max-width:700px;
                margin:0 auto 24px auto;
            ">
                {feature["popup_body"]}
            </div>

            <div style="
                padding:14px 18px;
                border:1px solid #dce8f4;
                border-radius:14px;
                background:#f7fbff;
                color:#3978c3;
                font-family:Georgia, serif;
                font-size:18px;
                font-style:italic;
                font-weight:700;
            ">
                {feature["framework"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    if st.button(
        "Close",
        use_container_width=True,
    ):

        st.session_state.selected_feature = None

        st.rerun()


# =========================================================
# FEATURE CARD
# =========================================================


def render_project_feature(
    feature: dict,
    index: int,
):
    """
    Render one interactive PIH framework card.
    """

    card_key = f"about_feature_{index}"

    st.markdown(
        """
        <style>

        div[data-testid="stButton"] > button {
            min-height: 175px;
            padding: 20px;
            border: 1px solid #dfe9f4;
            border-radius: 17px;
            background:
                linear-gradient(
                    180deg,
                    #ffffff,
                    #f8fbff
                );
            box-shadow:
                0 8px 20px
                rgba(71,105,145,0.05);
            text-align: left;
            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease;
        }

        div[data-testid="stButton"] > button:hover {
            transform: translateY(-4px);
            box-shadow:
                0 12px 26px
                rgba(71,105,145,0.12);
            border-color: #bcd4ec;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    button_label = (
        f'{feature["icon"]}\n\n' f'{feature["title"]}\n\n' f'{feature["description"]}'
    )

    if st.button(
        button_label,
        key=card_key,
        use_container_width=True,
    ):

        st.session_state.selected_feature = feature

        render_feature_popup(feature)


# =========================================================
# PIH PHILOSOPHY
# =========================================================


def render_pih_philosophy():
    """
    Render the central PIH philosophy.
    """

    st.html(
        """
        <section style="
            margin:38px 46px 34px 46px;
            padding:30px 25px;
            text-align:center;
            border-top:1px solid #dce8f4;
            border-bottom:1px solid #dce8f4;
        ">

            <div style="
                color:#294d72;
                font-family:Georgia, serif;
                font-size:21px;
                font-style:italic;
                line-height:1.9;
            ">

                Technology serves Purpose.<br>

                Purpose protects Identity.<br>

                Identity creates Opportunity.<br>

                Intelligence connects them.

            </div>

        </section>
        """,
    )


# =========================================================
# ABOUT PAGE
# =========================================================


def render_about_page():
    """
    Render the complete About page.
    """

    initialise_about_state()

    # -----------------------------------------------------
    # HERO
    # -----------------------------------------------------

    st.html(
        """
        <section style="
            padding:58px 46px 28px 46px;
        ">

            <div style="
                display:grid;
                grid-template-columns:1.12fr 0.88fr;
                gap:36px;
                align-items:center;
            ">

                <div>

                    <div style="
                        color:#3978c3;
                        font-size:11px;
                        font-weight:800;
                        text-transform:uppercase;
                        letter-spacing:1.2px;
                        margin-bottom:12px;
                    ">
                        Why Palembang Intelligence Hub
                    </div>

                    <h1 style="
                        margin:0;
                        font-family:Georgia, serif;
                        font-size:48px;
                        line-height:1.04;
                        color:#1d416b;
                    ">
                        Technology
                        <span style="
                            display:block;
                            color:#2d72c7;
                        ">
                            With Purpose
                        </span>
                    </h1>

                    <p style="
                        max-width:650px;
                        margin-top:18px;
                        color:#74869a;
                        font-size:14px;
                        line-height:1.75;
                    ">
                        Palembang Intelligence Hub is a human-centered
                        digital platform designed to make Palembang's
                        heritage, culture, food, local businesses and
                        economic identity easier to discover, understand
                        and connect with opportunity.
                    </p>

                </div>

                <div style="
                    min-height:220px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    border:1px solid #dce8f4;
                    border-radius:24px;
                    background:
                        radial-gradient(
                            circle,
                            #deedff,
                            #f9fcff 68%
                        );
                    font-size:28px;
                    color:#294d72;
                    text-align:center;
                    padding:30px;
                ">
                    Technology becomes meaningful
                    when it amplifies human purpose,
                    not when it replaces human presence.
                </div>

            </div>

        </section>
        """,
    )

    # -----------------------------------------------------
    # WHY PIH EXISTS
    # -----------------------------------------------------

    st.html(
        """
        <section style="
            margin:0 46px 30px 46px;
            padding:25px;
            border:1px solid #dce8f4;
            border-radius:18px;
            background:#ffffff;
            box-shadow:
                0 9px 25px
                rgba(68,104,145,0.06);
        ">

            <div style="
                color:#294d72;
                font-family:Georgia, serif;
                font-size:22px;
                font-weight:700;
                margin-bottom:11px;
            ">
                Why PIH Exists
            </div>

            <div style="
                color:#71849a;
                font-size:12px;
                line-height:1.8;
            ">
                Palembang is more than a destination.

                It is a city shaped by history, rivers, culture,
                food, people and economic potential.

                Palembang Intelligence Hub was created to connect
                these pieces through accessible digital technology.

                The goal is not simply to provide information,
                but to help people discover more, understand better
                and see new possibilities within a local place.
            </div>

        </section>
        """,
    )

    # -----------------------------------------------------
    # INTERACTIVE FRAMEWORK
    # -----------------------------------------------------

    columns = st.columns(4)

    for index, (
        column,
        feature,
    ) in enumerate(
        zip(
            columns,
            PROJECT_FEATURES,
        )
    ):

        with column:

            render_project_feature(
                feature=feature,
                index=index,
            )

    # -----------------------------------------------------
    # PHILOSOPHY
    # -----------------------------------------------------

    render_pih_philosophy()

    # -----------------------------------------------------
    # MISSION & PRINCIPLES
    # -----------------------------------------------------

    st.html(
        """
        <section style="
            margin:34px 46px 24px 46px;
            display:grid;
            grid-template-columns:1fr 1fr;
            gap:18px;
        ">

            <div style="
                padding:23px;
                border:1px solid #dce8f4;
                border-radius:18px;
                background:#f7fbff;
            ">

                <div style="
                    color:#294d72;
                    font-size:17px;
                    font-weight:800;
                    margin-bottom:10px;
                ">
                    Mission & Vision
                </div>

                <div style="
                    color:#74869a;
                    font-size:11px;
                    line-height:1.8;
                ">

                    <strong>Mission</strong><br>

                    To make Palembang more visible,
                    more connected and more economically active
                    through human-centered digital technology.

                    <br><br>

                    <strong>Vision</strong><br>

                    To grow PIH into a trusted and scalable
                    intelligence platform that begins with Palembang
                    and expands to other Indonesian cities.

                </div>

            </div>

            <div style="
                padding:23px;
                border:1px solid #dce8f4;
                border-radius:18px;
                background:#ffffff;
            ">

                <div style="
                    color:#294d72;
                    font-size:17px;
                    font-weight:800;
                    margin-bottom:10px;
                ">
                    Core Principles
                </div>

                <div style="
                    color:#74869a;
                    font-size:11px;
                    line-height:1.8;
                ">

                    <strong>Human-Centered Technology</strong><br>
                    Technology should serve human purpose.

                    <br><br>

                    <strong>Local Economic Empowerment</strong><br>
                    Digital visibility should create opportunity.

                    <br><br>

                    <strong>Cultural Preservation</strong><br>
                    Local identity should remain visible and accessible.

                    <br><br>

                    <strong>Practical Innovation</strong><br>
                    Innovation should create meaningful value.

                </div>

            </div>

        </section>
        """,
    )

    # -----------------------------------------------------
    # CLOSING
    # -----------------------------------------------------

    st.html(
        """
        <section style="
            margin:0 46px 50px 46px;
            padding:20px 24px;
            text-align:center;
            border:1px solid #dce8f4;
            border-radius:18px;
            background:
                linear-gradient(
                    135deg,
                    #f3f8ff,
                    #ffffff
                );
        ">

            <div style="
                color:#294d72;
                font-size:14px;
                font-weight:800;
            ">
                Built by S. Widjaja
            </div>

            <div style="
                color:#8797a8;
                font-size:9px;
                margin-top:6px;
            ">
                Palembang Intelligence Hub
                <br>
                Discover more than a place. Understand a city.
            </div>

        </section>
        """,
    )
