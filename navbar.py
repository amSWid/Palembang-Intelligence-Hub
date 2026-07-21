from textwrap import dedent

import streamlit as st

NAV_ITEMS = [
    ("Home", "home"),
    ("Discover", "discover"),
    ("Food", "food"),
    ("Ecosystem", "ecosystem"),
    ("Itinerary", "itinerary"),
    ("Investment", "investment"),
    ("About", "about"),
]


def get_current_page() -> str:
    """
    Read the active page from the URL.
    """

    page = st.query_params.get(
        "page",
        "home",
    )

    if isinstance(page, list):
        page = page[0]

    valid_pages = {page_name for _, page_name in NAV_ITEMS}

    if page not in valid_pages:
        return "home"

    return page


def build_navigation_html(
    current_page: str,
) -> str:
    """
    Build all navigation links.
    """

    menu_items = []

    for label, page_name in NAV_ITEMS:
        active_class = "active" if current_page == page_name else ""

        item_html = dedent(f"""
            <a
                class="nav-item {active_class}"
                href="?page={page_name}"
                target="_self"
            >
                {label}
            </a>
            """).strip()

        menu_items.append(item_html)

    return "".join(menu_items)


def render_navbar() -> str:
    """
    Render the top navigation.
    """

    current_page = get_current_page()

    navigation_html = build_navigation_html(current_page)

    navbar_html = dedent(f"""
        <nav class="top-navbar">

            <div class="navbar-brand">

                <div class="navbar-logo">
                    🏙️
                </div>

                <div class="navbar-brand-text">

                    <div class="navbar-brand-title">
                        Palembang
                    </div>

                    <div class="navbar-brand-subtitle">
                        Intelligence Hub
                    </div>

                </div>

            </div>

            <div class="navbar-menu">
                {navigation_html}
            </div>

            <div class="navbar-actions">

                <div
                    class="language-pill"
                    title="Application language"
                >
                    🌐 EN
                </div>

                <div
                    class="navbar-circle"
                    title="Light appearance"
                >
                    ☀
                </div>

                <div
                    class="navbar-circle"
                    title="Palembang Intelligence"
                >
                    ✦
                </div>

            </div>

        </nav>
        """).strip()

    st.html(navbar_html)

    return current_page
