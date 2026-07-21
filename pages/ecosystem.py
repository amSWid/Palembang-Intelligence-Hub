from textwrap import dedent

import streamlit as st

from ui.page_ai import (
    queue_page_question,
    render_page_ai,
)

# =========================================================
# ECOSYSTEM DATA
# =========================================================

ECOSYSTEM_SERVICES = {
    "hotels": {
        "icon": "🏨",
        "title": "Hotels",
        "description": (
            "Find accommodation for different budgets, " "locations and travel styles."
        ),
        "items": [
            {
                "name": "The Arista Hotel Palembang",
                "type": "Business & leisure hotel",
                "icon": "🏨",
                "description": (
                    "An accommodation option for visitors "
                    "seeking business and leisure facilities."
                ),
                "question": (
                    "Tell me about hotel options for business "
                    "and leisure travelers in Palembang."
                ),
            },
            {
                "name": "Aryaduta Palembang",
                "type": "City hotel",
                "icon": "🛏️",
                "description": (
                    "A city accommodation option for visitors "
                    "who want access to central Palembang."
                ),
                "question": (
                    "What should a visitor consider when choosing "
                    "a centrally located hotel in Palembang?"
                ),
            },
            {
                "name": "The Excelton Hotel",
                "type": "Urban accommodation",
                "icon": "🏢",
                "description": (
                    "An urban hotel option for business trips, "
                    "meetings and city exploration."
                ),
                "question": (
                    "What hotel facilities are useful for "
                    "business travelers visiting Palembang?"
                ),
            },
            {
                "name": "Wyndham OPI Hotel",
                "type": "South Palembang accommodation",
                "icon": "🌆",
                "description": (
                    "An accommodation option for travelers "
                    "visiting the Jakabaring and OPI area."
                ),
                "question": (
                    "What should visitors know about staying "
                    "near Jakabaring and the OPI area?"
                ),
            },
        ],
    },
    "restaurants": {
        "icon": "🍽️",
        "title": "Restaurants",
        "description": ("Discover traditional dishes and local " "restaurant options."),
        "items": [
            {
                "name": "Pempek Restaurant",
                "type": "Traditional Palembang food",
                "icon": "🐟",
                "description": (
                    "A place focused on pempek and other "
                    "fish-based Palembang dishes."
                ),
                "question": (
                    "What should a visitor know before choosing "
                    "a traditional pempek restaurant in Palembang?"
                ),
            },
            {
                "name": "Mie Celor 26 Ilir",
                "type": "Traditional noodle dish",
                "icon": "🍜",
                "description": (
                    "A culinary option associated with "
                    "Palembang's well-known mie celor."
                ),
                "question": (
                    "What makes mie celor a distinctive "
                    "Palembang culinary experience?"
                ),
            },
            {
                "name": "Tekwan Kitchen",
                "type": "Fish dumpling soup",
                "icon": "🍲",
                "description": (
                    "A local dining option for tekwan and "
                    "other traditional soup dishes."
                ),
                "question": (
                    "What is tekwan and how is it usually " "served in Palembang?"
                ),
            },
            {
                "name": "Musi Riverside Dining",
                "type": "River-view dining",
                "icon": "🌊",
                "description": (
                    "A dining concept combining local cuisine "
                    "with views of the Musi River."
                ),
                "question": (
                    "What makes dining near the Musi River " "interesting for visitors?"
                ),
            },
        ],
    },
    "transportation": {
        "icon": "🚕",
        "title": "Transportation",
        "description": (
            "Understand airport, rail, road and river " "transportation options."
        ),
        "items": [
            {
                "name": "Palembang LRT",
                "type": "Urban rail transport",
                "icon": "🚆",
                "description": (
                    "A public transportation option connecting "
                    "important areas of Palembang."
                ),
                "question": (
                    "How can visitors use public rail " "transportation in Palembang?"
                ),
            },
            {
                "name": "Sultan Mahmud Badaruddin II Airport",
                "type": "Air transportation",
                "icon": "✈️",
                "description": (
                    "The main air gateway used by visitors "
                    "traveling to and from Palembang."
                ),
                "question": (
                    "What transportation options can visitors "
                    "consider after arriving at Palembang airport?"
                ),
            },
            {
                "name": "Taxi & Ride-Hailing",
                "type": "Road transportation",
                "icon": "🚖",
                "description": (
                    "Flexible transportation for traveling "
                    "between hotels, restaurants and attractions."
                ),
                "question": (
                    "What road transportation options are "
                    "practical for tourists in Palembang?"
                ),
            },
            {
                "name": "Musi River Boat",
                "type": "River transportation",
                "icon": "🚤",
                "description": (
                    "River transport associated with Palembang's "
                    "historic relationship with the Musi River."
                ),
                "question": (
                    "What role does river transportation play "
                    "in Palembang tourism and daily life?"
                ),
            },
        ],
    },
    "attractions": {
        "icon": "🏛️",
        "title": "Attractions",
        "description": ("Explore landmarks, heritage sites and " "city destinations."),
        "items": [
            {
                "name": "Ampera Bridge",
                "type": "City landmark",
                "icon": "🌉",
                "description": (
                    "One of the most recognizable landmarks "
                    "associated with Palembang."
                ),
                "question": ("What is the history and importance " "of Ampera Bridge?"),
            },
            {
                "name": "Musi River",
                "type": "Natural & cultural landmark",
                "icon": "🌊",
                "description": (
                    "A river that has influenced transportation, "
                    "trade and Palembang culture."
                ),
                "question": (
                    "How has the Musi River shaped " "Palembang's history and culture?"
                ),
            },
            {
                "name": "Kemaro Island",
                "type": "River destination",
                "icon": "🏝️",
                "description": (
                    "A river island associated with local "
                    "stories, culture and tourism."
                ),
                "question": ("What should visitors know about " "Kemaro Island?"),
            },
            {
                "name": "Benteng Kuto Besak",
                "type": "Historic area",
                "icon": "🏰",
                "description": (
                    "A historic riverside area connected "
                    "with Palembang's urban identity."
                ),
                "question": (
                    "What is the historical importance " "of Benteng Kuto Besak?"
                ),
            },
        ],
    },
    "shopping": {
        "icon": "🛍️",
        "title": "Shopping",
        "description": ("Find local products, souvenirs and " "shopping experiences."),
        "items": [
            {
                "name": "Songket Palembang",
                "type": "Traditional textile",
                "icon": "🧵",
                "description": (
                    "A traditional textile associated with "
                    "Palembang culture and craftsmanship."
                ),
                "question": (
                    "What makes Palembang songket culturally "
                    "important and distinctive?"
                ),
            },
            {
                "name": "Traditional Souvenirs",
                "type": "Local products",
                "icon": "🎁",
                "description": (
                    "Local products that visitors may consider "
                    "as gifts or travel memories."
                ),
                "question": (
                    "What traditional souvenirs should visitors "
                    "look for in Palembang?"
                ),
            },
            {
                "name": "Traditional Markets",
                "type": "Local shopping",
                "icon": "🧺",
                "description": (
                    "Shopping areas where visitors can explore "
                    "local products and daily city life."
                ),
                "question": (
                    "What can visitors experience at "
                    "traditional markets in Palembang?"
                ),
            },
            {
                "name": "Modern Shopping Centers",
                "type": "Urban shopping",
                "icon": "🏬",
                "description": (
                    "Modern retail and lifestyle facilities "
                    "for residents and visitors."
                ),
                "question": (
                    "What types of modern shopping experiences "
                    "are available in Palembang?"
                ),
            },
        ],
    },
    "tour_guides": {
        "icon": "🧑‍💼",
        "title": "Tour Guides",
        "description": (
            "Choose guided experiences for culture, " "food and heritage exploration."
        ),
        "items": [
            {
                "name": "Heritage Guide",
                "type": "History & landmarks",
                "icon": "🏛️",
                "description": (
                    "Guided exploration focused on Palembang's "
                    "history and heritage locations."
                ),
                "question": (
                    "What should be included in a Palembang " "heritage tour?"
                ),
            },
            {
                "name": "Culinary Guide",
                "type": "Food experience",
                "icon": "🍜",
                "description": (
                    "A guided experience focused on local dishes "
                    "and Palembang culinary culture."
                ),
                "question": (
                    "What foods should be included in a " "Palembang culinary tour?"
                ),
            },
            {
                "name": "Musi River Guide",
                "type": "River experience",
                "icon": "🚤",
                "description": (
                    "A guided city experience centered on "
                    "the Musi River and nearby landmarks."
                ),
                "question": (
                    "What should visitors explore during " "a Musi River tour?"
                ),
            },
            {
                "name": "One-Day City Guide",
                "type": "Short itinerary",
                "icon": "🗓️",
                "description": (
                    "A guided option for visitors with " "limited time in Palembang."
                ),
                "question": (
                    "What should a first-time visitor include "
                    "in a one-day Palembang itinerary?"
                ),
            },
        ],
    },
    "health": {
        "icon": "🏥",
        "title": "Health Services",
        "description": (
            "Access general health, pharmacy and " "emergency service information."
        ),
        "items": [
            {
                "name": "Hospitals",
                "type": "Medical services",
                "icon": "🏥",
                "description": (
                    "General information about hospital services "
                    "that visitors may need."
                ),
                "question": (
                    "What health service information should "
                    "travelers prepare before visiting Palembang?"
                ),
            },
            {
                "name": "Clinics",
                "type": "General treatment",
                "icon": "🩺",
                "description": (
                    "Medical service options for general "
                    "health needs and consultation."
                ),
                "question": (
                    "What should tourists know about accessing "
                    "general clinics in Palembang?"
                ),
            },
            {
                "name": "Pharmacies",
                "type": "Medicine & supplies",
                "icon": "💊",
                "description": (
                    "Places for obtaining common medicine " "and basic health supplies."
                ),
                "question": (
                    "What basic health preparations are useful "
                    "for visitors traveling in Palembang?"
                ),
            },
            {
                "name": "Emergency Information",
                "type": "Urgent assistance",
                "icon": "🚑",
                "description": (
                    "General guidance for handling urgent "
                    "medical or travel situations."
                ),
                "question": (
                    "What emergency information should "
                    "visitors keep while traveling in Palembang?"
                ),
            },
        ],
    },
    "more": {
        "icon": "•••",
        "title": "More Services",
        "description": ("Explore additional city and visitor " "support services."),
        "items": [
            {
                "name": "Banking & ATM",
                "type": "Financial services",
                "icon": "🏧",
                "description": (
                    "General financial services useful "
                    "for visitors and business travelers."
                ),
                "question": (
                    "What financial preparations should "
                    "travelers make before visiting Palembang?"
                ),
            },
            {
                "name": "Prayer Facilities",
                "type": "Visitor facilities",
                "icon": "🙏",
                "description": (
                    "General information about religious " "and prayer facilities."
                ),
                "question": (
                    "What should visitors know about finding "
                    "prayer facilities in Palembang?"
                ),
            },
            {
                "name": "Police & Public Assistance",
                "type": "Public support",
                "icon": "👮",
                "description": (
                    "Public assistance information for "
                    "travel and safety-related needs."
                ),
                "question": (
                    "What safety information is useful "
                    "for tourists visiting Palembang?"
                ),
            },
            {
                "name": "Business Support",
                "type": "Investor services",
                "icon": "📊",
                "description": (
                    "General support information for "
                    "business and investment visitors."
                ),
                "question": (
                    "What business support information "
                    "is useful for investors visiting Palembang?"
                ),
            },
        ],
    },
}


# =========================================================
# SESSION STATE
# =========================================================


def initialise_ecosystem_state():
    """
    Prepare Ecosystem page session state.
    """

    if "selected_ecosystem_service" not in st.session_state:
        st.session_state.selected_ecosystem_service = "hotels"


def select_ecosystem_service(
    service_key: str,
):
    """
    Select one Ecosystem service.
    """

    st.session_state.selected_ecosystem_service = service_key


def ask_ecosystem_ai(
    question: str,
):
    """
    Queue an Ecosystem question.

    The answer stays on the Ecosystem page.
    """

    queue_page_question(
        page_key="ecosystem",
        question=question,
    )


# =========================================================
# PAGE HEADER
# =========================================================


def render_ecosystem_header():
    """
    Render the Ecosystem page header.
    """

    header_html = dedent("""
        <section style="
            padding:58px 46px 28px 46px;
        ">
            <div style="
                display:grid;
                grid-template-columns:1.2fr 0.8fr;
                gap:35px;
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
                        Connected city services
                    </div>

                    <h1 style="
                        margin:0;
                        font-family:Georgia, serif;
                        font-size:48px;
                        line-height:1.05;
                        color:#1d416b;
                    ">
                        Palembang

                        <span style="
                            display:block;
                            color:#2d72c7;
                        ">
                            Travel Ecosystem
                        </span>
                    </h1>

                    <p style="
                        max-width:620px;
                        margin-top:18px;
                        color:#74869a;
                        font-size:14px;
                        line-height:1.75;
                    ">
                        A connected information center for tourism,
                        transportation, food, accommodation, health
                        and supporting city services.
                    </p>
                </div>

                <div style="
                    min-height:210px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    border:1px solid #dce8f4;
                    border-radius:24px;
                    background:
                        radial-gradient(
                            circle,
                            #e1efff,
                            #f8fbff 65%
                        );
                    font-size:86px;
                ">
                    🏙️
                </div>
            </div>
        </section>
        """).strip()

    st.html(header_html)


# =========================================================
# SERVICE SELECTOR
# =========================================================


def render_service_selector():
    """
    Render eight clickable service categories.
    """

    st.html("""
        <div style="
            padding:8px 46px 15px 46px;
        ">
            <div style="
                color:#294d72;
                font-family:Georgia, serif;
                font-size:22px;
                font-weight:700;
            ">
                Essential Services
            </div>

            <div style="
                margin-top:5px;
                color:#8495a8;
                font-size:10px;
            ">
                Select a category to view available city services.
            </div>
        </div>
        """)

    service_keys = list(ECOSYSTEM_SERVICES.keys())

    for row_start in range(
        0,
        len(service_keys),
        4,
    ):
        columns = st.columns(4)

        row_keys = service_keys[row_start : row_start + 4]

        for column, service_key in zip(
            columns,
            row_keys,
        ):
            service = ECOSYSTEM_SERVICES[service_key]

            is_selected = st.session_state.selected_ecosystem_service == service_key

            button_label = f"{service['icon']}  " f"{service['title']}"

            with column:
                if st.button(
                    button_label,
                    key=("ecosystem_service_" f"{service_key}"),
                    use_container_width=True,
                    type=("primary" if is_selected else "secondary"),
                ):
                    select_ecosystem_service(service_key)
                    st.rerun()


# =========================================================
# ITEM CARDS
# =========================================================


def render_item_card(
    item: dict,
    service_key: str,
    item_index: int,
):
    """
    Render one Ecosystem item.
    """

    with st.container(border=True):
        item_html = dedent(f"""
            <div style="
                min-height:155px;
                padding:8px 5px 3px 5px;
            ">
                <div style="
                    width:42px;
                    height:42px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    border-radius:13px;
                    background:#edf5ff;
                    font-size:20px;
                    margin-bottom:13px;
                ">
                    {item["icon"]}
                </div>

                <div style="
                    color:#294d72;
                    font-size:15px;
                    font-weight:800;
                    margin-bottom:5px;
                ">
                    {item["name"]}
                </div>

                <div style="
                    color:#3978c3;
                    font-size:9px;
                    font-weight:700;
                    margin-bottom:8px;
                ">
                    {item["type"]}
                </div>

                <div style="
                    color:#76889b;
                    font-size:10px;
                    line-height:1.6;
                ">
                    {item["description"]}
                </div>
            </div>
            """).strip()

        st.html(item_html)

        if st.button(
            "explore more",
            key=(f"ecosystem_ask_" f"{service_key}_" f"{item_index}"),
            use_container_width=True,
        ):
            ask_ecosystem_ai(item["question"])
            st.rerun()


def render_selected_service():
    """
    Render items for the selected service.
    """

    selected_key = st.session_state.selected_ecosystem_service

    service = ECOSYSTEM_SERVICES[selected_key]

    selected_header = dedent(f"""
        <section style="
            margin:30px 46px 18px 46px;
            padding:22px 24px;
            border:1px solid #dce8f4;
            border-radius:18px;
            background:
                linear-gradient(
                    135deg,
                    #ffffff,
                    #f5faff
                );
        ">
            <div style="
                display:flex;
                align-items:center;
                gap:14px;
            ">
                <div style="
                    width:48px;
                    height:48px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    border-radius:15px;
                    background:#eaf3ff;
                    font-size:23px;
                ">
                    {service["icon"]}
                </div>

                <div>
                    <div style="
                        color:#294d72;
                        font-size:19px;
                        font-weight:800;
                    ">
                        {service["title"]}
                    </div>

                    <div style="
                        margin-top:4px;
                        color:#77899c;
                        font-size:11px;
                    ">
                        {service["description"]}
                    </div>
                </div>
            </div>
        </section>
        """).strip()

    st.html(selected_header)

    items = service["items"]

    columns = st.columns(4)

    for index, item in enumerate(items):
        with columns[index]:
            render_item_card(
                item=item,
                service_key=selected_key,
                item_index=index,
            )


# =========================================================
# MAIN PAGE
# =========================================================


def render_ecosystem_page():
    """
    Render the complete interactive Ecosystem page.
    """

    initialise_ecosystem_state()

    render_ecosystem_header()
    render_service_selector()
    render_selected_service()

    # The AI answer remains on the Ecosystem page.
    render_page_ai(
        page_key="ecosystem",
    )
