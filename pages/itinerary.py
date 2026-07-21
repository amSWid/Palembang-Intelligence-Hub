import streamlit as st


def initialise_itinerary_state():
    """
    Initialise itinerary form state.
    """

    defaults = {
        "itinerary_days": 2,
        "itinerary_budget": "Medium",
        "itinerary_interest": "Culture & History",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_itinerary_result(
    days: int,
    budget: str,
    interest: str,
):
    """
    Render a temporary itinerary preview.
    """

    st.html(
        f"""
        <section style="
            margin:25px 46px 50px 46px;
            padding:25px;
            border:1px solid #dbe7f3;
            border-radius:19px;
            background:#ffffff;
            box-shadow:0 12px 30px rgba(68,104,145,0.08);
        ">

            <div style="
                color:#2a4e74;
                font-size:18px;
                font-weight:800;
                margin-bottom:7px;
            ">
                Your Palembang Itinerary
            </div>

            <div style="
                color:#7a8b9d;
                font-size:11px;
                margin-bottom:20px;
            ">
                {days} day(s) • {budget} budget • {interest}
            </div>

            <div style="
                display:grid;
                grid-template-columns:repeat(3, 1fr);
                gap:14px;
            ">

                <div style="
                    padding:17px;
                    border-radius:15px;
                    background:#f4f9ff;
                ">
                    <strong style="color:#31577c;">
                        Morning
                    </strong>

                    <div style="
                        color:#74879b;
                        font-size:11px;
                        line-height:1.6;
                        margin-top:7px;
                    ">
                        Visit Ampera Bridge and explore
                        the Musi River area.
                    </div>
                </div>

                <div style="
                    padding:17px;
                    border-radius:15px;
                    background:#f4f9ff;
                ">
                    <strong style="color:#31577c;">
                        Afternoon
                    </strong>

                    <div style="
                        color:#74879b;
                        font-size:11px;
                        line-height:1.6;
                        margin-top:7px;
                    ">
                        Enjoy traditional Palembang food
                        and visit a cultural destination.
                    </div>
                </div>

                <div style="
                    padding:17px;
                    border-radius:15px;
                    background:#f4f9ff;
                ">
                    <strong style="color:#31577c;">
                        Evening
                    </strong>

                    <div style="
                        color:#74879b;
                        font-size:11px;
                        line-height:1.6;
                        margin-top:7px;
                    ">
                        Explore local culinary areas
                        and enjoy the city atmosphere.
                    </div>
                </div>

            </div>

            <div style="
                margin-top:17px;
                color:#8a9aac;
                font-size:9px;
            ">
                This is currently a UI preview. The final itinerary
                will be generated using the Palembang AI assistant.
            </div>

        </section>
        """,
        
    )


def render_itinerary_page():
    """
    Render smart itinerary planner.
    """

    initialise_itinerary_state()

    st.html(
        """
        <section style="
            padding:58px 46px 22px 46px;
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
                Personalized travel planning
            </div>

            <h1 style="
                margin:0;
                font-family:Georgia, serif;
                font-size:48px;
                color:#1d416b;
            ">
                Smart Itinerary
            </h1>

            <p style="
                max-width:660px;
                margin:16px auto 0 auto;
                color:#74869a;
                font-size:14px;
                line-height:1.7;
            ">
                Build a Palembang travel plan based on your
                available time, budget and interests.
            </p>

        </section>
        """,
        
    )

    st.html(
        """
        <div style="
            margin:15px 46px 0 46px;
            padding:24px 24px 10px 24px;
            border:1px solid #dce8f4;
            border-radius:19px;
            background:#ffffff;
            box-shadow:0 10px 25px rgba(68,104,145,0.07);
        ">
        """,
        
    )

    days_column, budget_column, interest_column = st.columns(3)

    with days_column:
        days = st.selectbox(
            "Trip duration",
            options=[1, 2, 3, 4, 5],
            key="itinerary_days",
        )

    with budget_column:
        budget = st.selectbox(
            "Budget level",
            options=[
                "Budget",
                "Medium",
                "Premium",
            ],
            key="itinerary_budget",
        )

    with interest_column:
        interest = st.selectbox(
            "Main interest",
            options=[
                "Culture & History",
                "Traditional Food",
                "Family Travel",
                "Business & Investment",
                "City Exploration",
            ],
            key="itinerary_interest",
        )

    generate_clicked = st.button(
        "Generate My Itinerary",
        key="generate_itinerary",
        use_container_width=True,
    )

    st.html(
        "</div>",
        
    )

    if generate_clicked:
        render_itinerary_result(
            days=days,
            budget=budget,
            interest=interest,
        )
