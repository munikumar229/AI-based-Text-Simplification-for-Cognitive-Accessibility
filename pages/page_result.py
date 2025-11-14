import streamlit as st
from utils.css import inject_global_css
from utils.assistive import apply_assistive_features
from backend import generate_tts_audio
from app import goto


def render():
    inject_global_css()

    lang = st.session_state.lang
    simplified = st.session_state.simplified_text

    # ------------------------------
    # Localized text
    # ------------------------------
    if lang == "English":
        t_title = "🪄 Simplified Output"
        t_compare = "Compare with Original"
        t_original = "Original Text"
        t_simplified = "Simplified Text"
        t_download = "⬇️ Download"
        t_copy = "📋 Copy"
        t_play = "🔊 Play Audio"
        t_theme = "Theme"
        t_light = "🌞 Light"
        t_sepia = "📜 Sepia"
        t_dark = "🌙 Dark"
        t_back = "⬅️ Back"
        t_home = "🏠 Home"
        t_restart = "🔄 Start Over"
        t_word_count = "Number of words"
        t_resimplify = "🔄 Re-simplify"
    else:
        t_title = "🪄 సరళీకృత పాఠ్యం"
        t_compare = "అసలుతో పోల్చు"
        t_original = "అసలు పాఠ్యం"
        t_simplified = "సరళీకృత పాఠ్యం"
        t_download = "⬇️ డౌన్‌లోడ్"
        t_copy = "📋 కాపీ"
        t_play = "🔊 ఆడియో ప్లే చేయండి"
        t_theme = "థీమ్"
        t_light = "🌞 లైట్"
        t_sepia = "📜 సెపియా"
        t_dark = "🌙 డార్క్"
        t_back = "⬅️ వెనక్కి"
        t_home = "🏠 హోమ్"
        t_restart = "🔄 మళ్లీ మొదలుపెట్టు"
        t_word_count = "పదాల సంఖ్య"
        t_resimplify = "🔄 మళ్లీ సరళీకరించు"

    # ------------------------------
    # Theme selection
    # ------------------------------
    st.markdown(f"<h1 style='color:#7C3AED; font-weight:800;'>{t_title}</h1>", unsafe_allow_html=True)

    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        if st.button(t_light, use_container_width=True):
            st.session_state.theme = "light"
    with col_t2:
        if st.button(t_sepia, use_container_width=True):
            st.session_state.theme = "sepia"
    with col_t3:
        if st.button(t_dark, use_container_width=True):
            st.session_state.theme = "dark"

    # ------------------------------
    # Toggle features
    # ------------------------------
    st.write("")
    st.markdown("<h3>Reading Features</h3>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.session_state.bold_vowels = st.checkbox(
            "Bold Vowels",
            value=st.session_state.get("bold_vowels", False)
        )

    with c2:
        st.session_state.color_letters = st.checkbox(
            "Color Letters",
            value=st.session_state.get("color_letters", False)
        )

    with c3:
        st.session_state.reading_assist = st.checkbox(
            "Reading Assist",
            value=st.session_state.get("reading_assist", False)
        )

    if st.session_state.reading_assist:
        st.session_state.bold_first_n = st.slider(
            "Bold first grapheme(s)",
            1, 3,
            st.session_state.get("bold_first_n", 1)
        )

        if lang == "తెలుగు":
            st.session_state.telugu_assist = st.checkbox(
                "Telugu character assist",
                value=st.session_state.get("telugu_assist", True)
            )

    # ------------------------------
    # Apply assistive features
    # ------------------------------
    processed_text = apply_assistive_features(
        text=simplified,
        lang=lang,
        theme=st.session_state.theme,
        bold_vowels=st.session_state.get("bold_vowels", False),
        color_letters=st.session_state.get("color_letters", False),
        assist_on=st.session_state.get("reading_assist", False),
        bold_first_n=st.session_state.get("bold_first_n", 1),
        telugu_assist=st.session_state.get("telugu_assist", True)
    )

    # ------------------------------
    # Show output
    # ------------------------------
    st.markdown(processed_text, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # ------------------------------
    # Compare toggle
    # ------------------------------
    if st.button(t_compare, use_container_width=True):
        st.session_state.show_compare = not st.session_state.get("show_compare", False)

    if st.session_state.get("show_compare", False):
        colA, colB = st.columns(2)

        with colA:
            st.markdown(f"<h3>{t_original}</h3>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='compare-box'>{st.session_state.text_input}</div>",
                unsafe_allow_html=True
            )
        with colB:
            st.markdown(f"<h3>{t_simplified}</h3>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='compare-box'>{processed_text}</div>",
                unsafe_allow_html=True
            )

    st.write("")
    st.write("")

    # ------------------------------
    # Audio + Download + Copy
    # ------------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(t_play, use_container_width=True):
            try:
                audio_file = generate_tts_audio(
                    simplified,
                    lang="te" if lang == "తెలుగు" else "en"
                )
                st.audio(audio_file, format="audio/mp3")
            except Exception as e:
                st.error(f"TTS Failed: {e}")

    with col2:
        st.download_button(
            t_download,
            simplified,
            file_name="simplified.txt",
            use_container_width=True
        )

    with col3:
        if st.button(t_copy, use_container_width=True):
            st.info("Copied to clipboard (browser dependent).")

    # ------------------------------
    # Word Count Adjustment + Re-simplify
    # ------------------------------
    st.write("")
    st.markdown(f"<h3>{t_word_count}</h3>", unsafe_allow_html=True)

    new_count = st.slider(
        t_word_count,
        50, 300,
        st.session_state.desired_word_count,
        step=10
    )

    if new_count != st.session_state.desired_word_count:
        st.session_state.desired_word_count = new_count

    if st.button(t_resimplify, use_container_width=True):
        goto("processing")

    # ------------------------------
    # Navigation
    # ------------------------------
    st.write("")
    colB, colC, colD = st.columns(3)

    with colB:
        if st.button(t_back, use_container_width=True):
            goto("input")

    with colC:
        if st.button(t_restart, use_container_width=True):
            goto("language")

    with colD:
        if st.button(t_home, use_container_width=True):
            goto("language")
