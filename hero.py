import base64
from pathlib import Path
from textwrap import dedent

import streamlit as st

from config import IMAGE_DIR

AUDIO_DIR = Path(__file__).resolve().parent / "assets" / "audio"
THEME_AUDIO_PATH = AUDIO_DIR / "palembang_theme.mp3"


TOPIC_CARDS = [
    {
        "position": "orbit-general",
        "icon": "⌘",
        "title": "General",
        "description": "Get practical information about Palembang.",
        "page": "home",
    },
    {
        "position": "orbit-history",
        "icon": "🏛️",
        "title": "History",
        "description": "Discover heritage, legends and geography.",
        "page": "discover",
    },
    {
        "position": "orbit-culture",
        "icon": "✺",
        "title": "Culture",
        "description": "Explore traditions, arts and local music.",
        "page": "discover",
    },
    {
        "position": "orbit-economy",
        "icon": "📈",
        "title": "Economy",
        "description": "Explore economy, harvest and business data.",
        "page": "investment",
    },
    {
        "position": "orbit-food",
        "icon": "🍜",
        "title": "Food",
        "description": "Discover local dishes and restaurant addresses.",
        "page": "food",
    },
]


def file_to_base64(
    file_path: Path,
) -> str:
    """
    Convert a local file into a Base64 string.
    """

    if not file_path.exists():
        return ""

    return base64.b64encode(file_path.read_bytes()).decode("utf-8")


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

    encoded_image = file_to_base64(image_path)

    return f"data:{mime_type};" f"base64,{encoded_image}"


def get_music_status() -> bool:
    """
    Read music status from the URL query parameter.

    Example:
        ?page=home&music=on
    """

    music_value = st.query_params.get(
        "music",
        "off",
    )

    return str(music_value).lower() == "on"


def build_music_html(
    music_is_on: bool,
) -> str:
    """
    Create the hidden looping audio player.
    """

    if not music_is_on:
        return ""

    if not THEME_AUDIO_PATH.exists():
        return ""

    audio_base64 = file_to_base64(THEME_AUDIO_PATH)

    if not audio_base64:
        return ""

    return dedent(f"""
        <audio
            autoplay
            loop
            preload="auto"
            style="display:none;"
        >
            <source
                src="data:audio/mpeg;base64,{audio_base64}"
                type="audio/mpeg"
            >
        </audio>
        """).strip()


def build_robot_html(
    robot_base64: str,
    music_is_on: bool,
) -> str:
    """
    Create the clickable robot.

    Clicking the robot toggles the Palembang theme music.
    """

    if music_is_on:
        music_target = "off"
        music_label = "Music On"
        music_icon = "♫"
        accessibility_label = "Stop Palembang theme music"
        status_class = "music-active"
    else:
        music_target = "on"
        music_label = "Play Music"
        music_icon = "♪"
        accessibility_label = "Play Palembang theme music"
        status_class = ""

    target_url = f"?page=home&music={music_target}"

    if robot_base64:
        robot_content = dedent(f"""
            <img
                src="{robot_base64}"
                alt="Palembang Intelligence Robot"
            >
            """).strip()
    else:
        robot_content = dedent("""
            <div class="robot-fallback">
                🤖
            </div>
            """).strip()

    return dedent(f"""
        <a
            class="robot-music-link {status_class}"
            href="{target_url}"
            target="_self"
            aria-label="{accessibility_label}"
            title="{accessibility_label}"
        >
            <div class="robot-stage">
                {robot_content}
            </div>

            <div class="robot-music-badge">
                <span class="robot-music-icon">
                    {music_icon}
                </span>

                <span class="robot-music-label">
                    {music_label}
                </span>
            </div>

            <div class="robot-music-credit">
                Original music by S. Widjaja
            </div>

        </a>
        """).strip()


def render_orbit_card(
    position_class: str,
    icon: str,
    title: str,
    description: str,
    page: str,
) -> str:
    """
    Create one clickable topic card.
    """

    music_value = "on" if get_music_status() else "off"

    return dedent(f"""
        <a
            class="orbit-card orbit-link {position_class}"
            href="?page={page}&music={music_value}"
            target="_self"
            aria-label="Open {title} page"
        >
            <div class="orbit-card-icon">
                {icon}
            </div>

            <div class="orbit-card-title">
                {title}
            </div>

            <div class="orbit-card-text">
                {description}
            </div>

            <div class="orbit-card-action">
                Explore →
            </div>
        </a>
        """).strip()


def render_hero():
    """
    Render the interactive Palembang homepage hero.
    """

    robot_path = IMAGE_DIR / "robot_palembang.png"

    robot_base64 = image_to_base64(robot_path)

    music_is_on = get_music_status()

    music_html = build_music_html(music_is_on)

    robot_html = build_robot_html(
        robot_base64=robot_base64,
        music_is_on=music_is_on,
    )

    cards_html = "".join(
        render_orbit_card(
            position_class=card["position"],
            icon=card["icon"],
            title=card["title"],
            description=card["description"],
            page=card["page"],
        )
        for card in TOPIC_CARDS
    )

    hero_html = dedent(f"""
        <style>
            .robot-music-link {{
                position: absolute;
                left: 50%;
                top: 48%;
                z-index: 20;
                display: flex;
                flex-direction: column;
                align-items: center;
                text-decoration: none;
                transform: translate(-50%, -50%);
                cursor: pointer;
            }}

            .robot-music-link .robot-stage {{
                position: relative;
                transition:
                    transform 0.35s ease,
                    filter 0.35s ease;
            }}

            .robot-music-link:hover .robot-stage {{
                transform:
                    translateY(-7px)
                    scale(1.035);
                filter:
                    drop-shadow(
                        0 18px 24px
                        rgba(87, 76, 255, 0.20)
                    );
            }}

            .robot-music-link.music-active
            .robot-stage {{
                animation:
                    robotMusicPulse
                    2.4s ease-in-out
                    infinite;
            }}

            .robot-music-badge {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
                min-width: 150px;
                margin-top: 10px;
                padding: 10px 22px;
                border:
                    1px solid
                    rgba(87, 76, 255, 0.18);
                border-radius: 999px;
                background:
                    rgba(255, 255, 255, 0.92);
                box-shadow:
                    0 8px 22px
                    rgba(15, 23, 42, 0.08);
                color: #5750d8;
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 0.02em;
                line-height: 1;
                white-space: nowrap;
                backdrop-filter: blur(12px);
                transition:
                    transform 0.25s ease,
                    box-shadow 0.25s ease,
                    background 0.25s ease;
            }}

            .robot-music-link:hover
            .robot-music-badge {{
                transform: translateY(-2px);
                background: #ffffff;
                box-shadow:
                    0 10px 28px
                    rgba(87, 76, 255, 0.16);
            }}

            .robot-music-link.music-active
            .robot-music-badge {{
                color: #ffffff;
                border-color: transparent;
                background:
                    linear-gradient(
                        135deg,
                        #665cff,
                        #8b5cf6
                    );
            }}

            .robot-music-icon {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 18px;
                height: 18px;
                border-radius: 50%;
                font-size: 14px;
            }}

            .robot-music-label {{
                display: inline-block;
                line-height: 1;
            }}

            .robot-music-credit {{
                margin-top: 8px;
                color: #718198;
                font-size: 10px;
                font-weight: 600;
                letter-spacing: 0.03em;
                line-height: 1.3;
                text-align: center;
                white-space: nowrap;
            }}

            .robot-music-link.music-active
            .robot-music-icon {{
                animation:
                    musicNotePulse
                    1.1s ease-in-out
                    infinite;
            }}

            @keyframes robotMusicPulse {{
                0%,
                100% {{
                    filter:
                        drop-shadow(
                            0 10px 18px
                            rgba(87, 76, 255, 0.12)
                        );
                }}

                50% {{
                    filter:
                        drop-shadow(
                            0 17px 31px
                            rgba(87, 76, 255, 0.32)
                        );
                }}
            }}

            @keyframes musicNotePulse {{
                0%,
                100% {{
                    transform: scale(1);
                }}

                50% {{
                    transform: scale(1.25);
                }}
            }}
        </style>

        {music_html}

        <section class="hero-wrapper">

            <div class="hero-content-grid">

                <div class="hero-copy">

                    <div class="hero-eyebrow">
                        ✦ AI Tourism &amp; Investment Assistant
                    </div>

                    <h1 class="hero-title">
                        Palembang

                        <span class="hero-title-accent">
                            Intelligence Hub
                        </span>
                    </h1>

                    <div class="hero-description">
                        Explore Palembang through heritage,
                        cuisine, culture, economy and investment
                        intelligence powered by local knowledge
                        and artificial intelligence.
                    </div>

                    <div class="hero-signature">
                        S. Widjaja
                    </div>

                    <div class="hero-author">
                        Designed by S. Widjaja
                    </div>

                </div>

                <div class="hero-visual">

                    <div class="hero-orbit">

                        <div class="orbit-ring ring-1"></div>
                        <div class="orbit-ring ring-2"></div>
                        <div class="orbit-ring ring-3"></div>

                        <div class="orbit-line-horizontal"></div>
                        <div class="orbit-line-vertical"></div>

                        {cards_html}
                        {robot_html}

                    </div>

                </div>

            </div>

        </section>
        """).strip()

    st.html(hero_html)

    if not THEME_AUDIO_PATH.exists():
        st.warning("Audio file was not found: " f"{THEME_AUDIO_PATH}")
