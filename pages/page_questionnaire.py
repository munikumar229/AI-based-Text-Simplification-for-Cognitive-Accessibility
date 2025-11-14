import streamlit as st
from utils.css import inject_global_css
from app import goto


def render():
    inject_global_css()

    lang = st.session_state.lang

    # ------------------------------
    # Localized labels
    # ------------------------------
    if lang == "English":
        t_harder = "What's harder for you?"
        t_reading = "Reading the text"
        t_understand = "Understanding the meaning"
        t_obstacles = "What makes reading hard?"
        t_prefs = "Reading Preferences"
        t_tts = "TTS Autoplay"
        t_next = "➡️ Next"
        t_back = "⬅️ Back"
    else:
        t_harder = "ఏది కష్టం?"
        t_reading = "పాఠ్యం చదవడం"
        t_understand = "అర్థం చేసుకోవడం"
        t_obstacles = "ఏవి అడ్డుగా ఉన్నాయి?"
        t_prefs = "పఠన ప్రాధాన్యతలు"
        t_tts = "TTS ఆటోప్లే"
        t_next = "➡️ ముందుకు"
        t_back = "⬅️ వెనక్కి"

    # ------------------------------
    # PAGE HEADER
    # ------------------------------
    st.markdown(f"""
        <h1 style='color:#7C3AED; font-weight:800;'>{t_harder}</h1>
    """, unsafe_allow_html=True)

    st.write("")

    # ------------------------------
    # HARDER TOGGLE
    # ------------------------------
    col1, col2 = st.columns(2)

    # Reading
    with col1:
        selected = (st.session_state.harder == "reading")
        st.markdown("<div class='outline-btn'>", unsafe_allow_html=True)
        if st.button(("✅ " if selected else "") + t_reading, key="harder_read", use_container_width=True):
            st.session_state.harder = "reading"
        st.markdown("</div>", unsafe_allow_html=True)

    # Understanding
    with col2:
        selected = (st.session_state.harder == "understanding")
        st.markdown("<div class='outline-btn'>", unsafe_allow_html=True)
        if st.button(("✅ " if selected else "") + t_understand, key="harder_under", use_container_width=True):
            st.session_state.harder = "understanding"
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.write("")

    # ------------------------------
    # OBSTACLES
    # ------------------------------
    st.markdown(f"<h1 style='color:#7C3AED; font-weight:800;'>{t_obstacles}</h1>", unsafe_allow_html=True)

    # Options localized
    if lang == "English":
        options = [
            ("small_text", "Small text"),
            ("tight_spacing", "Tight spacing"),
            ("dense_paragraphs", "Dense paragraphs"),
            ("complex_words", "Complex words"),
            ("long_sentences", "Long sentences"),
            ("busy_layout", "Busy layout"),
        ]
    else:
        options = [
            ("small_text", "చిన్న అక్షరాలు"),
            ("tight_spacing", "తక్కువ స్పేసింగ్"),
            ("dense_paragraphs", "ఘనమైన పేరాగ్రాఫ్‌లు"),
            ("complex_words", "సంక్లిష్ట పదాలు"),
            ("long_sentences", "పొడవైన వాక్యాలు"),
            ("busy_layout", "బిజీ లేఅవుట్"),
        ]

    cols = st.columns(3)

    for idx, (key, label) in enumerate(options):
        col = cols[idx % 3]
        with col:
            selected = key in st.session_state.obstacles
            css = "outline-btn" if not selected else "primary-btn"

            st.markdown(f"<div class='{css}'>", unsafe_allow_html=True)
            if st.button(("✅ " if selected else "") + label, key=f"ob_{key}", use_container_width=True):
                if selected:
                    st.session_state.obstacles.remove(key)
                else:
                    st.session_state.obstacles.append(key)
            st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.write("")

    # ------------------------------
    # READING PREFERENCES
    # ------------------------------
    st.markdown(f"<h1 style='color:#7C3AED; font-weight:800;'>{t_prefs}</h1>", unsafe_allow_html=True)

    colA, colB, colC = st.columns(3)

    with colA:
        st.session_state.font_size = st.slider(
            "Font Size",
            14, 32,
            st.session_state.font_size,
            key="font_size_slider"
        )

    with colB:
        st.session_state.line_height = st.slider(
            "Line Spacing",
            1.0, 4.0,
            st.session_state.line_height,
            0.1,
            key="line_height_slider"
        )

    with colC:
        st.session_state.letter_spacing = st.slider(
            "Letter Spacing",
            0.0, 0.25,
            st.session_state.letter_spacing,
            0.01,
            key="letter_spacing_slider"
        )

    st.write("")
    st.write("")

    # ------------------------------
    # TTS AUTOPLAY
    # ------------------------------
    st.markdown("<h3>🔊 TTS Autoplay</h3>", unsafe_allow_html=True)
    st.session_state.tts_autoplay = st.checkbox(
        t_tts,
        value=st.session_state.tts_autoplay,
        key="tts_auto"
    )

    # ------------------------------
    # NAVIGATION
    # ------------------------------
    st.write("")
    st.write("")
    col_back, col_next = st.columns(2)

    with col_back:
        st.markdown("<div class='secondary-btn'>", unsafe_allow_html=True)
        if st.button(t_back, use_container_width=True):
            goto("spacing_examples")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_next:
        st.markdown("<div class='primary-btn'>", unsafe_allow_html=True)
        if st.button(t_next, use_container_width=True):
            goto("input")
        st.markdown("</div>", unsafe_allow_html=True)
