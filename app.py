import streamlit as st

from navbar import render_navbar
from pages.about import render_about_page
from pages.discover import render_discover_page
from pages.ecosystem import render_ecosystem_page
from pages.food import render_food_page
from pages.home import render_home_page
from pages.investment import render_investment_page
from pages.itinerary import render_itinerary_page
from styles import load_css

st.set_page_config(
    page_title="Palembang Intelligence Hub",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def initialise_app_state():
    defaults = {
        "question_input": "",
        "submitted_question": "",
        "auto_run": False,
        "last_answer": "",
        "last_source_id": None,
        "last_category": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_current_page(current_page: str):
    page_routes = {
        "home": render_home_page,
        "discover": render_discover_page,
        "food": render_food_page,
        "ecosystem": render_ecosystem_page,
        "itinerary": render_itinerary_page,
        "investment": render_investment_page,
        "about": render_about_page,
    }

    selected_page = page_routes.get(
        current_page,
        render_home_page,
    )

    selected_page()


def main():
    initialise_app_state()
    load_css()

    current_page = render_navbar()

    render_current_page(current_page)

if __name__ == "__main__":
    main()
