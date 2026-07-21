from textwrap import dedent

import streamlit as st


INVESTMENT_SECTORS = [
    {
        "icon": "🏭",
        "title": "Manufacturing",
        "description": (
            "Explore industrial development, processing activities "
            "and opportunities connected to regional production."
        ),
        "question": (
            "What manufacturing investment opportunities "
            "are available in Palembang?"
        ),
    },
    {
        "icon": "🌾",
        "title": "Agriculture",
        "description": (
            "Understand agriculture, plantation output, food supply "
            "and downstream processing potential."
        ),
        "question": (
            "What agriculture and food processing opportunities "
            "exist in Palembang?"
        ),
    },
    {
        "icon": "🚚",
        "title": "Logistics",
        "description": (
            "Discover opportunities related to transportation, "
            "warehousing, trade and Musi River connectivity."
        ),
        "question": (
            "Why is Palembang attractive for logistics investment?"
        ),
    },
    {
        "icon": "🏨",
        "title": "Tourism",
        "description": (
            "Explore tourism, accommodation, culinary businesses "
            "and destination development opportunities."
        ),
        "question": (
            "What tourism investment opportunities "
            "are available in Palembang?"
        ),
    },
    {
        "icon": "🏗️",
        "title": "Infrastructure",
        "description": (
            "Review opportunities connected to urban development, "
            "public facilities and supporting infrastructure."
        ),
        "question": (
            "What infrastructure opportunities "
            "support Palembang's economic growth?"
        ),
    },
    {
        "icon": "💻",
        "title": "Digital Economy",
        "description": (
            "Explore digital services, smart-city solutions, "
            "creative businesses and technology adoption."
        ),
        "question": (
            "What digital economy opportunities "
            "can be developed in Palembang?"
        ),
    },
]


def set_investment_question(question: str):
    """
    Queue an investment question and return to Home.
    """

    st.session_state.pending_question = question
    st.query_params["page"] = "home"


def render_sector_card(
    sector: dict,
    index: int,
):
    """
    Render one investment sector.
    """

    with st.container(border=True):
        card_html = dedent(
            f"""
            <div style="
                min-height:190px;
                padding:8px 5px;
            ">
                <div style="
                    width:46px;
                    height:46px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    margin-bottom:14px;
                    border-radius:14px;
                    background:#edf5ff;
                    font-size:22px;
                ">
                    {sector["icon"]}
                </div>

                <div style="
                    color:#264c73;
                    font-size:16px;
                    font-weight:800;
                    margin-bottom:8px;
                ">
                    {sector["title"]}
                </div>

                <div style="
                    color:#75879b;
                    font-size:11px;
                    line-height:1.65;
                ">
                    {sector["description"]}
                </div>
            </div>
            """
        ).strip()

        st.html(card_html)

        if st.button(
            f'Ask about {sector["title"]}',
            key=f"investment_sector_{index}",
            use_container_width=True,
        ):
            set_investment_question(
                sector["question"]
            )
            st.rerun()


def render_investment_summary():
    """
    Render four investment summary cards.
    """

    metrics = [
        (
            "Economic Insight",
            "Regional Growth",
            "GDP trends and sector performance",
        ),
        (
            "Business Potential",
            "Opportunity Mapping",
            "Promising sectors and local demand",
        ),
        (
            "Income Analysis",
            "Market Capacity",
            "Recommendations based on income",
        ),
        (
            "Local Evidence",
            "Trusted Sources",
            "GDP and Bank Indonesia documents",
        ),
    ]

    columns = st.columns(4)

    for column, metric in zip(
        columns,
        metrics,
    ):
        label, value, description = metric

        with column:
            metric_html = dedent(
                f"""
                <div style="
                    min-height:130px;
                    padding:18px;
                    border:1px solid #dfe9f4;
                    border-radius:16px;
                    background:
                        linear-gradient(
                            180deg,
                            #ffffff,
                            #f8fbff
                        );
                    box-shadow:
                        0 8px 20px
                        rgba(71,105,145,0.05);
                ">
                    <div style="
                        color:#7d8fa3;
                        font-size:9px;
                        font-weight:800;
                        text-transform:uppercase;
                        letter-spacing:0.8px;
                    ">
                        {label}
                    </div>

                    <div style="
                        color:#285077;
                        font-size:16px;
                        font-weight:800;
                        margin-top:10px;
                    ">
                        {value}
                    </div>

                    <div style="
                        color:#8494a5;
                        font-size:9px;
                        line-height:1.5;
                        margin-top:6px;
                    ">
                        {description}
                    </div>
                </div>
                """
            ).strip()

            st.html(metric_html)


def render_investment_page():
    """
    Render the Investment Intelligence page.
    """

    header_html = dedent(
        """
        <section style="
            padding:58px 46px 26px 46px;
        ">
            <div style="
                display:grid;
                grid-template-columns:1.15fr 0.85fr;
                gap:34px;
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
                        Data-driven opportunity discovery
                    </div>

                    <h1 style="
                        margin:0;
                        font-family:Georgia, serif;
                        font-size:48px;
                        line-height:1.04;
                        color:#1d416b;
                    ">
                        Investment
                        <span style="
                            display:block;
                            color:#2d72c7;
                        ">
                            Intelligence
                        </span>
                    </h1>

                    <p style="
                        max-width:640px;
                        margin-top:18px;
                        color:#74869a;
                        font-size:14px;
                        line-height:1.75;
                    ">
                        Explore Palembang's economic growth,
                        sector performance, income conditions
                        and potential business opportunities
                        supported by trusted local documents.
                    </p>
                </div>

                <div style="
                    min-height:215px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    border:1px solid #dce8f4;
                    border-radius:24px;
                    background:
                        radial-gradient(
                            circle,
                            #ddebff,
                            #f9fcff 68%
                        );
                    font-size:90px;
                ">
                    📈
                </div>
            </div>
        </section>
        """
    ).strip()

    st.html(header_html)

    render_investment_summary()

    sector_header_html = dedent(
        """
        <div style="
            padding:30px 46px 16px 46px;
        ">
            <div style="
                color:#294d72;
                font-family:Georgia, serif;
                font-size:23px;
                font-weight:700;
            ">
                Explore Investment Sectors
            </div>

            <div style="
                color:#8797a8;
                font-size:10px;
                margin-top:4px;
            ">
                Select a sector and send a focused
                question to the AI assistant.
            </div>
        </div>
        """
    ).strip()

    st.html(sector_header_html)

    for row_start in range(
        0,
        len(INVESTMENT_SECTORS),
        3,
    ):
        columns = st.columns(3)

        row_items = INVESTMENT_SECTORS[
            row_start : row_start + 3
        ]

        for local_index, (
            column,
            sector,
        ) in enumerate(
            zip(columns, row_items)
        ):
            absolute_index = (
                row_start + local_index
            )

            with column:
                render_sector_card(
                    sector=sector,
                    index=absolute_index,
                )

    logic_html = dedent(
        """
        <section style="
            margin:35px 46px 50px 46px;
            padding:24px;
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
                font-size:17px;
                font-weight:800;
                margin-bottom:9px;
            ">
                ✦ Investment Recommendation Logic
            </div>

            <div style="
                color:#71849a;
                font-size:12px;
                line-height:1.75;
            ">
                The final AI system will combine economic growth,
                regional income, sector performance and documented
                opportunities. Recommendations will distinguish
                between evidence from the source documents and
                analytical suggestions generated by the assistant.
            </div>
        </section>
        """
    ).strip()

    st.html(logic_html)