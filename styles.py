import streamlit as st


def load_css():
    st.html(
        """
        <style>

        /* =========================================
           GLOBAL
        ========================================= */

        html,
        body,
        [data-testid="stAppViewContainer"] {
            background:
                linear-gradient(
                    180deg,
                    rgba(247, 251, 255, 0.96) 0%,
                    rgba(241, 247, 255, 0.98) 48%,
                    rgba(250, 252, 255, 1) 100%
                );
            color: #152f55;
            font-family:
                Inter,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
        }

        [data-testid="stAppViewContainer"] {
            min-height: 100vh;
        }

        [data-testid="stMain"] {
            background: transparent;
        }

        [data-testid="stMainBlockContainer"] {
            width: 100%;
            max-width: 1440px;
            padding-top: 0.4rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
            padding-bottom: 4rem;
        }

        [data-testid="stHeader"] {
            background: transparent;
            height: 0;
        }

        [data-testid="stToolbar"] {
            display: none;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            visibility: hidden;
        }

        .block-container {
            padding-top: 0 !important;
        }

        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
            color: #15375f;
        }

        p {
            color: #61738b;
        }

        /* =========================================
           APP SHELL
        ========================================= */

        [data=testid="stMainBlockContainer"] {
            background:
                linear-gradient(
                    180deg,
                    rgba(255, 255, 255, 0.98),
                    rgba(247, 251, 255, 0.98)
                );
            border: 1px solid rgba(117, 153, 198, 0.18);
            border-radius: 30px;
            box-shadow:
                0 26px 70px rgba(53, 92, 141, 0.12),
                0 8px 24px rgba(53, 92, 141, 0.07);
            overflow: hidden;
        }

        /* =========================================
           NAVBAR
        ========================================= */

        .top-navbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            min-height: 72px;
            padding: 0 26px;
            background: rgba(255, 255, 255, 0.96);
            border-bottom: 1px solid #edf2f8;
            box-shadow: 0 5px 18px rgba(72, 103, 143, 0.04);
            position: relative;
            z-index: 20;
        }

        .navbar-brand {
            display: flex;
            align-items: center;
            gap: 11px;
            min-width: 210px;
        }

        .navbar-logo {
            width: 38px;
            height: 38px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
            background:
                linear-gradient(
                    135deg,
                    #eaf4ff,
                    #dfeeff
                );
            border: 1px solid #cddff5;
            color: #2d70c9;
            font-size: 19px;
            box-shadow: 0 5px 13px rgba(43, 103, 177, 0.12);
        }

        .navbar-brand-text {
            line-height: 1.05;
        }

        .navbar-brand-title {
            font-family: Georgia, "Times New Roman", serif;
            font-size: 18px;
            font-weight: 700;
            color: #173c68;
            letter-spacing: -0.3px;
        }

        .navbar-brand-subtitle {
            margin-top: 4px;
            font-size: 8px;
            font-weight: 600;
            color: #8a9aaf;
            text-transform: uppercase;
            letter-spacing: 0.7px;
        }

        .navbar-menu {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 7px;
            flex: 1;
        }

        .nav-item {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 10px 13px;
            border-radius: 9px;
            color: #52667e;
            font-size: 12px;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s ease;
        }

        .nav-item:hover {
            color: #2769c5;
            background: #f0f6ff;
        }

        .nav-item.active {
            color: #286bc5;
            background: #eef5ff;
            box-shadow: inset 0 -2px 0 #4c8bda;
        }

        .navbar-actions {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 8px;
            min-width: 210px;
        }

        .language-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            height: 34px;
            padding: 0 12px;
            border: 1px solid #dce7f3;
            border-radius: 18px;
            background: white;
            color: #48617d;
            font-size: 11px;
            font-weight: 700;
        }

        .navbar-circle {
            width: 34px;
            height: 34px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            border: 1px solid #dce7f3;
            background: white;
            color: #55708d;
            font-size: 14px;
        }

        /* =========================================
           HERO SECTION
        ========================================= */

        .hero-wrapper {
            position: relative;
            min-height: 500px;
            padding: 46px 46px 42px 46px;
            overflow: hidden;
            background:
                radial-gradient(
                    circle at 72% 44%,
                    rgba(215, 235, 255, 0.78) 0%,
                    rgba(233, 244, 255, 0.42) 30%,
                    rgba(255, 255, 255, 0) 59%
                ),
                linear-gradient(
                    180deg,
                    #ffffff 0%,
                    #f9fcff 100%
                );
        }

        .hero-wrapper::before {
            content: "";
            position: absolute;
            left: -90px;
            bottom: -68px;
            width: 460px;
            height: 245px;
            background:
                radial-gradient(
                    ellipse,
                    rgba(173, 208, 246, 0.34),
                    rgba(220, 237, 255, 0.08) 55%,
                    transparent 72%
                );
            filter: blur(4px);
            pointer-events: none;
        }

        .hero-content-grid {
            display: grid;
            grid-template-columns: 1.02fr 1.18fr;
            gap: 28px;
            align-items: center;
            min-height: 420px;
        }

        .hero-copy {
            position: relative;
            z-index: 4;
            padding-top: 8px;
        }

        .hero-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            padding: 7px 11px;
            margin-bottom: 13px;
            border: 1px solid #d9e8f9;
            border-radius: 20px;
            background: rgba(245, 250, 255, 0.9);
            color: #54718f;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.3px;
        }

        .hero-title {
            margin: 0;
            font-family: Georgia, "Times New Roman", serif;
            font-size: clamp(42px, 4.2vw, 66px);
            line-height: 0.95;
            font-weight: 700;
            letter-spacing: -2.2px;
            color: #183960;
        }

        .hero-title-accent {
            display: block;
            margin-top: 10px;
            color: #2670c9;
        }

        .hero-description {
            max-width: 520px;
            margin-top: 22px;
            margin-bottom: 16px;
            color: #6b7f96;
            font-size: 14px;
            line-height: 1.65;
        }

        .hero-signature {
            margin-top: 8px;
            font-family: "Segoe Script", "Brush Script MT", cursive;
            font-size: 20px;
            color: #6986a7;
            transform: rotate(-2deg);
        }

        .hero-author {
            margin-top: 4px;
            color: #8a9caf;
            font-size: 10px;
            font-weight: 600;
        }

        
                .hero-visual {
            position: relative;
            min-height: 390px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .hero-orbit {
            position: absolute;
            width: 510px;
            height: 360px;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
        }

        /* =========================================
           ORBIT LINES
        ========================================= */

        .orbit-ring {
            position: absolute;
            left: 50%;
            top: 50%;
            border: 1px solid rgba(96, 150, 211, 0.16);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            pointer-events: none;
        }

        .orbit-ring.ring-1 {
            width: 205px;
            height: 205px;
        }

        .orbit-ring.ring-2 {
            width: 335px;
            height: 285px;
        }

        .orbit-ring.ring-3 {
            width: 480px;
            height: 350px;
        }

        .orbit-line-horizontal {
            position: absolute;
            left: 18px;
            right: 18px;
            top: 50%;
            height: 1px;
            background:
                linear-gradient(
                    90deg,
                    transparent,
                    rgba(95, 145, 205, 0.18),
                    transparent
                );
            pointer-events: none;
        }

        .orbit-line-vertical {
            position: absolute;
            top: 7px;
            bottom: 7px;
            left: 50%;
            width: 1px;
            background:
                linear-gradient(
                    180deg,
                    transparent,
                    rgba(95, 145, 205, 0.18),
                    transparent
                );
            pointer-events: none;
        }

        /* =========================================
           ROBOT — 20% LARGER
        ========================================= */

        .robot-stage {
            position: absolute;
            left: 50%;
            bottom: -29px;

            /*
            Previous width was approximately 250px.
            300px makes the robot 20% larger.
            */
            width: 300px;

            z-index: 6;
            pointer-events: none;

            transform:
                translateX(-50%)
                translateY(0)
                rotate(0deg);

            transform-origin: center bottom;

            filter:
                drop-shadow(
                    0 22px 24px
                    rgba(62, 96, 132, 0.20)
                );

            transition:
                transform 0.35s ease,
                filter 0.35s ease;
        }

        .robot-stage img {
            width: 100%;
            height: auto;
            display: block;
            object-fit: contain;
        }

        .robot-fallback {
            text-align: center;
            font-size: 138px;
        }

        /* =========================================
           INTERACTIVE ORBIT CARDS
        ========================================= */

        .orbit-card {
            position: absolute;

            width: 148px;
            min-height: 112px;

            padding: 13px 14px;

            border:
                1px solid
                rgba(178, 207, 239, 0.82);

            border-radius: 19px;

            background:
                rgba(255, 255, 255, 0.93);

            box-shadow:
                0 10px 26px
                rgba(75, 117, 165, 0.09);

            backdrop-filter: blur(10px);

            z-index: 8;
            cursor: pointer;
            text-decoration: none;
            overflow: hidden;

            transition:
                transform 0.25s ease,
                border-color 0.25s ease,
                box-shadow 0.25s ease,
                background 0.25s ease;
        }

        .orbit-link,
        .orbit-link:visited {
            color: inherit;
            text-decoration: none;
        }

        .orbit-card::after {
            content: "";
            position: absolute;
            inset: 0;

            opacity: 0;

            background:
                linear-gradient(
                    135deg,
                    rgba(234, 245, 255, 0.18),
                    rgba(202, 226, 255, 0.46)
                );

            transition: opacity 0.25s ease;
            pointer-events: none;
        }

        .orbit-card:hover {
            transform:
                translateY(-7px)
                scale(1.035);

            border-color: #76abe5;

            background:
                rgba(255, 255, 255, 0.99);

            box-shadow:
                0 20px 40px
                rgba(53, 111, 177, 0.18);
        }

        .orbit-card:hover::after {
            opacity: 1;
        }

        .orbit-card-icon,
        .orbit-card-title,
        .orbit-card-text,
        .orbit-card-action {
            position: relative;
            z-index: 2;
        }

        .orbit-card-icon {
            width: 32px;
            height: 32px;

            display: flex;
            align-items: center;
            justify-content: center;

            margin-bottom: 9px;

            border-radius: 10px;

            background: #edf5ff;
            color: #3976bd;

            font-size: 15px;

            transition:
                transform 0.25s ease,
                background 0.25s ease;
        }

        .orbit-card:hover .orbit-card-icon {
            transform:
                scale(1.12)
                rotate(-3deg);

            background: #deedff;
        }

        .orbit-card-title {
            margin-bottom: 5px;

            color: #21476f;

            font-size: 13px;
            font-weight: 800;
        }

        .orbit-card-text {
            color: #7c8fa4;

            font-size: 9px;
            line-height: 1.45;

            min-height: 38px;

            transition:
                transform 0.25s ease,
                opacity 0.25s ease;
        }

        .orbit-card-action {
            margin-top: 7px;

            color: #2f73c6;

            font-size: 9px;
            font-weight: 800;

            opacity: 0;

            transform: translateY(5px);

            transition:
                opacity 0.25s ease,
                transform 0.25s ease;
        }

        .orbit-card:hover .orbit-card-action {
            opacity: 1;
            transform: translateY(0);
        }

        /* =========================================
           CARD POSITIONS
        ========================================= */

        .orbit-history {
            left: 50%;
            top: -4px;
            transform: translateX(-50%);
        }

        .orbit-history:hover {
            transform:
                translateX(-50%)
                translateY(-7px)
                scale(1.035);
        }

        .orbit-general {
            left: 0;
            top: 101px;
        }

        .orbit-culture {
            right: 0;
            top: 101px;
        }

        .orbit-economy {
            left: 15px;
            bottom: 3px;
        }

        .orbit-food {
            right: 15px;
            bottom: 3px;
        }

        /* =========================================
           ROBOT REACTION
        ========================================= */

        .hero-orbit:has(
            .orbit-general:hover
        ) .robot-stage {
            transform:
                translateX(-50%)
                translateX(-9px)
                rotate(-2deg);
        }

        .hero-orbit:has(
            .orbit-history:hover
        ) .robot-stage {
            transform:
                translateX(-50%)
                translateY(-8px);

            filter:
                drop-shadow(
                    0 27px 26px
                    rgba(52, 101, 154, 0.23)
                );
        }

        .hero-orbit:has(
            .orbit-culture:hover
        ) .robot-stage {
            transform:
                translateX(-50%)
                translateX(9px)
                rotate(2deg);
        }

        .hero-orbit:has(
            .orbit-economy:hover
        ) .robot-stage {
            transform:
                translateX(-50%)
                translateX(-8px)
                translateY(-4px)
                rotate(-2deg);
        }

        .hero-orbit:has(
            .orbit-food:hover
        ) .robot-stage {
            transform:
                translateX(-50%)
                translateX(8px)
                translateY(-4px)
                rotate(2deg);
        }


        /* =========================================
           SEARCH PANEL
        ========================================= */

        .search-panel {
            position: relative;
            z-index: 12;
            margin-top: -10px;
            padding: 0 46px;
        }

        .search-card {
            padding: 18px 20px 13px 20px;
            border: 1px solid rgba(184, 207, 235, 0.65);
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.96);
            box-shadow:
                0 18px 45px rgba(58, 98, 146, 0.13),
                0 4px 13px rgba(58, 98, 146, 0.06);
        }

        .search-title-row {
            display: flex;
            align-items: center;
            gap: 9px;
            color: #49627f;
            font-size: 12px;
            font-weight: 700;
            margin-bottom: 9px;
        }

        .search-input-shell {
            display: flex;
            align-items: center;
            min-height: 55px;
            padding: 5px 7px 5px 17px;
            border: 1px solid #dbe8f5;
            border-radius: 15px;
            background: #fbfdff;
        }

        .search-icon {
            margin-right: 12px;
            color: #6d83a0;
            font-size: 17px;
        }

        .search-placeholder {
            flex: 1;
            color: #8191a5;
            font-size: 13px;
        }

        .search-language {
            padding: 5px 9px;
            color: #7990ab;
            font-size: 10px;
            font-weight: 700;
        }

        .search-submit {
            width: 42px;
            height: 42px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            background:
                linear-gradient(
                    135deg,
                    #4b8fe6,
                    #2568c6
                );
            color: white;
            font-size: 18px;
            box-shadow: 0 7px 16px rgba(47, 113, 199, 0.3);
        }

        .search-meta {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 10px;
            gap: 12px;
        }

        .search-example {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 5px 9px;
            border-radius: 12px;
            background: #f1f6fc;
            color: #607995;
            font-size: 8px;
            font-weight: 700;
        }

        .search-privacy {
            color: #9aa8b7;
            font-size: 8px;
        }

        /* =========================================
           SUGGESTION CHIPS
        ========================================= */

        .question-strip {
            display: flex;
            align-items: center;
            gap: 9px;
            overflow-x: auto;
            padding: 15px 46px 6px 46px;
            scrollbar-width: none;
        }

        .question-strip::-webkit-scrollbar {
            display: none;
        }

        .question-chip {
            white-space: nowrap;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 7px 11px;
            border: 1px solid #e0eaf5;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.9);
            color: #5e7691;
            font-size: 9px;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(71, 109, 151, 0.05);
        }

        /* =========================================
           ECOSYSTEM
        ========================================= */

        .section-container {
            padding: 22px 46px 8px 46px;
        }

        .section-header {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            margin-bottom: 14px;
        }

        .section-title {
            margin: 0;
            color: #1d416b;
            font-family: Georgia, "Times New Roman", serif;
            font-size: 19px;
            font-weight: 700;
        }

        .section-subtitle {
            margin-top: 4px;
            color: #8a9aac;
            font-size: 9px;
        }

        .section-link {
            color: #3e7ec8;
            font-size: 9px;
            font-weight: 700;
        }

        .ecosystem-grid {
            display: grid;
            grid-template-columns: repeat(8, minmax(72px, 1fr));
            gap: 10px;
        }

        .ecosystem-item {
            min-height: 77px;
            padding: 13px 7px 10px 7px;
            text-align: center;
            border: 1px solid #e0eaf4;
            border-radius: 14px;
            background:
                linear-gradient(
                    180deg,
                    #ffffff,
                    #f9fcff
                );
            box-shadow: 0 5px 14px rgba(75, 110, 150, 0.05);
            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease;
        }

        .ecosystem-item:hover {
            transform: translateY(-3px);
            box-shadow: 0 11px 22px rgba(75, 110, 150, 0.11);
        }

        .ecosystem-icon {
            width: 31px;
            height: 31px;
            margin: 0 auto 8px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            background: #eef5ff;
            color: #3978c2;
            font-size: 15px;
        }

        .ecosystem-label {
            color: #365470;
            font-size: 8px;
            font-weight: 700;
        }

        /* =========================================
           LOWER CONTENT
        ========================================= */

        .content-grid {
            display: grid;
            grid-template-columns: 0.82fr 2.18fr;
            gap: 16px;
            padding: 15px 46px 38px 46px;
        }

        .info-card,
        .recommendation-card {
            border: 1px solid #e1eaf4;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.96);
            box-shadow: 0 8px 22px rgba(72, 105, 143, 0.06);
        }

        .info-card {
            padding: 18px;
        }

        .info-card-title {
            color: #25486d;
            font-size: 13px;
            font-weight: 800;
            margin-bottom: 9px;
        }

        .info-card-text {
            color: #75879b;
            font-size: 9px;
            line-height: 1.65;
        }

        .info-button {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            margin-top: 15px;
            padding: 7px 11px;
            border: 1px solid #dbe8f5;
            border-radius: 14px;
            background: #f7fbff;
            color: #537493;
            font-size: 8px;
            font-weight: 700;
        }

        .recommendation-card {
            padding: 17px 19px;
        }

        .recommendation-layout {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 18px;
        }

        .restaurant-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .restaurant-item {
            display: grid;
            grid-template-columns: 58px 1fr auto;
            gap: 10px;
            align-items: center;
            padding-bottom: 9px;
            border-bottom: 1px solid #eef3f8;
        }

        .restaurant-item:last-child {
            padding-bottom: 0;
            border-bottom: none;
        }

        .restaurant-thumb {
            width: 58px;
            height: 42px;
            overflow: hidden;
            border-radius: 9px;
            background: #edf3f8;
        }

        .restaurant-thumb img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .restaurant-name {
            color: #29496b;
            font-size: 9px;
            font-weight: 800;
        }

        .restaurant-details {
            margin-top: 3px;
            color: #8595a5;
            font-size: 7px;
            line-height: 1.4;
        }

        .restaurant-rating {
            color: #e0a329;
            font-size: 7px;
            font-weight: 700;
        }

        .restaurant-distance {
            color: #8a9bac;
            font-size: 7px;
            font-weight: 700;
        }

        .map-panel {
            min-height: 205px;
            overflow: hidden;
            border: 1px solid #dfe9f3;
            border-radius: 13px;
            background:
                linear-gradient(
                    135deg,
                    rgba(227, 239, 251, 0.85),
                    rgba(245, 249, 253, 0.9)
                );
            position: relative;
        }

        .map-grid {
            position: absolute;
            inset: 0;
            opacity: 0.55;
            background-image:
                linear-gradient(
                    rgba(124, 156, 191, 0.12) 1px,
                    transparent 1px
                ),
                linear-gradient(
                    90deg,
                    rgba(124, 156, 191, 0.12) 1px,
                    transparent 1px
                );
            background-size: 27px 27px;
        }

        .map-road {
            position: absolute;
            height: 3px;
            border-radius: 3px;
            background: rgba(255, 255, 255, 0.95);
            box-shadow: 0 0 0 1px rgba(175, 194, 214, 0.42);
            transform-origin: left center;
        }

        .map-marker {
            position: absolute;
            width: 16px;
            height: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50% 50% 50% 0;
            background: #367dd0;
            color: white;
            font-size: 7px;
            transform: rotate(-45deg);
            box-shadow: 0 4px 8px rgba(44, 101, 169, 0.24);
        }

        .map-marker span {
            transform: rotate(45deg);
        }

        .map-estimate {
            position: absolute;
            left: 10px;
            right: 10px;
            bottom: 10px;
            padding: 9px 10px;
            border: 1px solid rgba(213, 225, 238, 0.9);
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.94);
            box-shadow: 0 5px 13px rgba(76, 105, 141, 0.08);
        }

        .estimate-title {
            color: #3c5670;
            font-size: 8px;
            font-weight: 800;
            margin-bottom: 6px;
        }

        .estimate-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 3px;
            color: #8292a2;
            font-size: 7px;
        }

        /* =========================================
           STREAMLIT BUTTONS
        ========================================= */

        div.stButton > button {
            min-height: 40px;
            border: 1px solid #d9e6f3;
            border-radius: 13px;
            background:
                linear-gradient(
                    180deg,
                    #ffffff,
                    #f7fbff
                );
            color: #456887;
            font-size: 12px;
            font-weight: 700;
            box-shadow: 0 4px 12px rgba(74, 108, 147, 0.06);
            transition: all 0.2s ease;
        }

        div.stButton > button:hover {
            border-color: #8bb6e7;
            color: #286cbd;
            transform: translateY(-1px);
            box-shadow: 0 8px 18px rgba(54, 110, 176, 0.12);
        }

        div.stButton > button:focus {
            box-shadow: 0 0 0 3px rgba(71, 133, 204, 0.15);
        }

        /* =========================================
           STREAMLIT INPUT
        ========================================= */

        [data-testid="stTextInput"] input {
            min-height: 53px;
            padding-left: 17px;
            padding-right: 17px;
            border: 1px solid #d7e5f3;
            border-radius: 14px;
            background: #fbfdff;
            color: #2b4b6c;
            font-size: 13px;
            box-shadow: none;
        }

        [data-testid="stTextInput"] input:focus {
            border-color: #78a8de;
            box-shadow: 0 0 0 3px rgba(74, 134, 203, 0.12);
        }

        [data-testid="stTextInput"] label {
            display: none;
        }

        /* =========================================
           ANSWER CARD
        ========================================= */

        .answer-card {
            margin: 18px 46px;
            padding: 22px;
            border: 1px solid #dbe7f3;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.97);
            box-shadow: 0 12px 30px rgba(67, 104, 147, 0.09);
        }

        .answer-header {
            display: flex;
            align-items: center;
            gap: 9px;
            margin-bottom: 12px;
        }

        .answer-icon {
            width: 35px;
            height: 35px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 11px;
            background: #eaf3ff;
            color: #3376c5;
            font-size: 17px;
        }

        .answer-title {
            color: #254a72;
            font-size: 14px;
            font-weight: 800;
        }

        .answer-text {
            color: #62768d;
            font-size: 12px;
            line-height: 1.75;
        }

        .source-badge {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            margin-top: 14px;
            padding: 6px 10px;
            border-radius: 13px;
            background: #eff6ff;
            color: #52769a;
            font-size: 8px;
            font-weight: 700;
        }

        /* =========================================
           RESPONSIVE
        ========================================= */

        @media (max-width: 1150px) {

            .navbar-menu {
                gap: 2px;
            }

            .nav-item {
                padding-left: 8px;
                padding-right: 8px;
                font-size: 10px;
            }

            .ecosystem-grid {
                grid-template-columns: repeat(4, 1fr);
            }
        }

        @media (max-width: 900px) {

            [data-testid="stMainBlockContainer"] {
                padding-left: 0.7rem;
                padding-right: 0.7rem;
            }

            .top-navbar {
                padding: 0 15px;
            }

            .navbar-menu {
                display: none;
            }

            .navbar-brand,
            .navbar-actions {
                min-width: auto;
            }

            .hero-wrapper {
                padding: 31px 25px 25px 25px;
            }

            .hero-content-grid {
                grid-template-columns: 1fr;
            }

            .hero-copy {
                text-align: center;
            }

            .hero-description {
                margin-left: auto;
                margin-right: auto;
            }

            .hero-visual {
                min-height: 340px;
            }

            .search-panel,
            .question-strip,
            .section-container {
                padding-left: 25px;
                padding-right: 25px;
            }

            .content-grid {
                grid-template-columns: 1fr;
                padding-left: 25px;
                padding-right: 25px;
            }

            .recommendation-layout {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 620px) {

            .app-shell {
                border-radius: 17px;
            }

            .hero-title {
                font-size: 43px;
            }

            .hero-wrapper {
                padding-left: 15px;
                padding-right: 15px;
            }

            .hero-orbit {
                transform:
                    translate(-50%, -50%)
                    scale(0.8);
            }

            .search-panel,
            .question-strip,
            .section-container,
            .content-grid {
                padding-left: 14px;
                padding-right: 14px;
            }

            .ecosystem-grid {
                grid-template-columns: repeat(2, 1fr);
            }

            .navbar-brand-subtitle,
            .language-pill {
                display: none;
            }
        }

        

            /* =========================================
           FINAL HERO ORBIT OVERRIDE
           Put this at the very bottom of styles.py
        ========================================= */

        .hero-wrapper {
            min-height: 530px !important;
            padding: 44px 46px 44px 46px !important;
        }

        .hero-content-grid {
            grid-template-columns: 0.95fr 1.25fr !important;
            min-height: 420px !important;
            gap: 40px !important;
        }

        .hero-visual {
            min-height: 420px !important;
            overflow: visible !important;
        }

        .hero-orbit {
            width: 560px !important;
            height: 400px !important;
            left: 50% !important;
            top: 50% !important;
            transform: translate(-50%, -50%) !important;
        }

        .orbit-ring.ring-1 {
            width: 210px !important;
            height: 210px !important;
        }

        .orbit-ring.ring-2 {
            width: 350px !important;
            height: 300px !important;
        }

        .orbit-ring.ring-3 {
            width: 520px !important;
            height: 380px !important;
        }

        .robot-stage {
            width: 300px !important;
            left: 50% !important;
            bottom: -24px !important;
            transform: translateX(-50%) !important;
            z-index: 6 !important;

            pointer-events: none !important;

            transform:
            translateX(-50%)
            translateY(0)
            rotate(0deg) !important;

            transform-origin:
            center bottom !important;

            transition:
            transform 0.38s ease,
            filter 0.38s ease !important;

            animation:
            robot-idle 3.2s ease-in-out infinite;
        }



        /* =========================================
   ROBOT IDLE ANIMATION
========================================= */

@keyframes robot-idle {

    0%,
    100% {
        transform:
            translateX(-50%)
            translateY(0)
            rotate(0deg);
    }

    50% {
        transform:
            translateX(-50%)
            translateY(-7px)
            rotate(0deg);
    }
}


/* =========================================
   ROBOT REACTION TO CARD HOVER
========================================= */

.hero-orbit:has(
    .orbit-general:hover
) .robot-stage {
    animation: none !important;

    transform:
        translateX(-50%)
        translateX(-11px)
        translateY(-3px)
        rotate(-3deg) !important;
}


.hero-orbit:has(
    .orbit-history:hover
) .robot-stage {
    animation: none !important;

    transform:
        translateX(-50%)
        translateY(-13px)
        scale(1.03) !important;

    filter:
        drop-shadow(
            0 28px 28px
            rgba(52, 101, 154, 0.26)
        ) !important;
}


.hero-orbit:has(
    .orbit-culture:hover
) .robot-stage {
    animation: none !important;

    transform:
        translateX(-50%)
        translateX(11px)
        translateY(-3px)
        rotate(3deg) !important;
}


.hero-orbit:has(
    .orbit-economy:hover
) .robot-stage {
    animation: none !important;

    transform:
        translateX(-50%)
        translateX(-10px)
        translateY(-7px)
        rotate(-2deg) !important;
}


.hero-orbit:has(
    .orbit-food:hover
) .robot-stage {
    animation: none !important;

    transform:
        translateX(-50%)
        translateX(10px)
        translateY(-7px)
        rotate(2deg) !important;
}


        .orbit-card {
            box-sizing: border-box !important;

            width: 155px !important;
            height: 128px !important;
            min-height: 128px !important;
            max-height: 128px !important;

            padding: 13px 14px !important;

            display: flex !important;
            flex-direction: column !important;
            align-items: flex-start !important;

            border-radius: 18px !important;
            overflow: hidden !important;

            background: rgba(255, 255, 255, 0.96) !important;
            border: 1px solid #c9ddf2 !important;

            box-shadow:
                0 12px 28px
                rgba(70, 111, 157, 0.10) !important;

            text-decoration: none !important;
            z-index: 8 !important;
        }

        .orbit-card-icon {
            flex: 0 0 auto !important;

            width: 32px !important;
            height: 32px !important;

            margin: 0 0 8px 0 !important;

            border-radius: 10px !important;
            font-size: 15px !important;
        }

        .orbit-card-title {
            flex: 0 0 auto !important;

            margin: 0 0 5px 0 !important;

            color: #21476f !important;
            font-size: 13px !important;
            line-height: 1.2 !important;
            font-weight: 800 !important;
        }

        .orbit-card-text {
            flex: 1 1 auto !important;

            margin: 0 !important;

            color: #7c8fa4 !important;
            font-size: 9px !important;
            line-height: 1.4 !important;

            min-height: 0 !important;
            overflow: hidden !important;
        }

        .orbit-card-action {
            flex: 0 0 auto !important;

            margin-top: 5px !important;

            color: #2f73c6 !important;
            font-size: 9px !important;
            line-height: 1.2 !important;
            font-weight: 800 !important;

            opacity: 0 !important;
            transform: translateY(3px) !important;
        }

        .orbit-card:hover {
            border-color: #78aae1 !important;

            box-shadow:
                0 20px 38px
                rgba(53, 111, 177, 0.18) !important;
        }

        .orbit-card:hover .orbit-card-action {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }

        /* TOP CENTER */

        .orbit-history {
            left: 50% !important;
            right: auto !important;
            top: 0 !important;
            bottom: auto !important;

            transform: translateX(-50%) !important;
        }

        .orbit-history:hover {
            transform:
                translateX(-50%)
                translateY(-6px)
                scale(1.025) !important;
        }

        /* MIDDLE LEFT */

        .orbit-general {
            left: 0 !important;
            right: auto !important;
            top: 116px !important;
            bottom: auto !important;
        }

        /* MIDDLE RIGHT */

        .orbit-culture {
            left: auto !important;
            right: 0 !important;
            top: 116px !important;
            bottom: auto !important;
        }

        /* BOTTOM LEFT */

        .orbit-economy {
            left: 18px !important;
            right: auto !important;
            top: auto !important;
            bottom: 2px !important;
        }

        /* BOTTOM RIGHT */

        .orbit-food {
            left: auto !important;
            right: 18px !important;
            top: auto !important;
            bottom: 2px !important;
        }

        .orbit-general:hover,
        .orbit-culture:hover,
        .orbit-economy:hover,
        .orbit-food:hover {
            transform:
                translateY(-6px)
                scale(1.025) !important;
        }

        @media (max-width: 1150px) {

            .hero-content-grid {
                grid-template-columns: 0.9fr 1.1fr !important;
                gap: 20px !important;
            }

            .hero-orbit {
                transform:
                    translate(-50%, -50%)
                    scale(0.88) !important;
            }
        }

        @media (max-width: 900px) {

            .hero-wrapper {
                min-height: auto !important;
            }

            .hero-content-grid {
                grid-template-columns: 1fr !important;
            }

            .hero-visual {
                min-height: 430px !important;
            }

            .hero-orbit {
                transform:
                    translate(-50%, -50%)
                    scale(0.86) !important;
            }
        }

        @media (max-width: 620px) {

            .hero-visual {
                min-height: 360px !important;
            }

            .hero-orbit {
                transform:
                    translate(-50%, -50%)
                    scale(0.68) !important;
            }
        }

                /* =========================================
           UNIFIED SEARCH BAR
        ========================================= */

        [data-testid="stTextInput"] {
            margin: 0 !important;
        }

        [data-testid="stTextInput"] input {
            min-height: 72px !important;
            height: 72px !important;

            padding:
                0 26px !important;

            border:
                1px solid
                #cbdff3 !important;

            border-radius:
                22px !important;

            background:
                rgba(255, 255, 255, 0.97) !important;

            color:
                #244b73 !important;

            font-size:
                15px !important;

            font-weight:
                600 !important;

            box-shadow:
                0 15px 36px
                rgba(57, 99, 150, 0.11) !important;
        }

        [data-testid="stTextInput"] input::placeholder {
            color:
                #425f80 !important;

            opacity:
                1 !important;

            font-weight:
                700 !important;
        }

        [data-testid="stTextInput"] input:focus {
            border-color:
                #72a6df !important;

            box-shadow:
                0 0 0 4px
                rgba(75, 138, 210, 0.11),
                0 16px 38px
                rgba(57, 99, 150, 0.13) !important;

            outline:
                none !important;
        }

        .unified-search-language {
            height: 72px;

            display: flex;
            align-items: center;
            justify-content: center;

            color: #5f7fa3;

            font-size: 12px;
            font-weight: 800;
        }

        div.stButton > button[
            aria-label="Ask Palembang Intelligence"
        ] {
            min-height: 72px !important;
            height: 72px !important;

            border-radius: 20px !important;

            background:
                linear-gradient(
                    135deg,
                    #4e91e4,
                    #286cc7
                ) !important;

            color:
                #ffffff !important;

            font-size:
                19px !important;
        }

        .search-helper-row {
            display: flex;
            align-items: center;
            justify-content: space-between;

            padding:
                8px 8px 12px 8px;

            color:
                #8296ad;

            font-size:
                9px;

            font-weight:
                600;
        }


        </style>
        """,
    )
