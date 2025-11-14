import streamlit as st
from utils.css import inject_global_css
from utils.db import load_user_selection, save_user_selection
from app import goto
import regex


def render():
    inject_global_css()

    lang = st.session_state.lang
    user = st.session_state.user or "guest"

    st.markdown("""
        <h1 style='color:#7C3AED; font-weight:800; margin-bottom:5px;'>
            Example Style Preference
        </h1>
        <p style='color:gray; font-size:18px; margin-top:-8px;'>
            Choose the text style that feels easier for you to read
        </p>
    """, unsafe_allow_html=True)

    # ------------------------------
    # Choose the base example text
    # ------------------------------
    if lang == "English":
        base_text = "The quick brown fox jumps over the lazy dog."
    else:
        base_text = "వంద బోధనే తుమ్హి రాజు శాసనే రాష్ట్రం ప్రజల ప్రియమే"

    # ------------------------------
    # Bold-first-grapheme version
    # ------------------------------
    words = base_text.split()
    bolded_words = []
    for w in words:
        g = regex.findall(r"\X", w)
        if not g:
            bolded_words.append(w)
        else:
            bolded_words.append(f"<b>{g[0]}</b>{''.join(g[1:])}")

    bold_text = " ".join(bolded_words)

    # ------------------------------
    # Load previous selection from DB (once)
    # ------------------------------
    if st.session_state.selected_example is None:
        st.session_state.selected_example = load_user_selection(user, "examples")

    selected = st.session_state.selected_example

    # ------------------------------
    # Render example selection cards
    # ------------------------------
    col1, col2 = st.columns(2)

    # --- LEFT BOX ---
    with col1:
        is_sel = (selected == "left")
        css_class = "example-card selected" if is_sel else "example-card"

        if st.button(" ", key="examples_left_btn"):
            st.session_state.selected_example = "left"
            save_user_selection(user, "examples", "left")
            goto("spacing_examples")

        st.markdown(
            f"<div class='{css_class}'>{base_text}</div>",
            unsafe_allow_html=True
        )

    # --- RIGHT BOX ---
    with col2:
        is_sel = (selected == "right")
        css_class = "example-card selected" if is_sel else "example-card"

        if st.button(" ", key="examples_right_btn"):
            st.session_state.selected_example = "right"
            save_user_selection(user, "examples", "right")
            goto("spacing_examples")

        st.markdown(
            f"<div class='{css_class}'>{bold_text}</div>",
            unsafe_allow_html=True
        )

    # ------------------------------
    # Navigation buttons
    # ------------------------------
    st.write("")
    st.write("")
    col_back, col_next = st.columns(2)

    with col_back:
        st.markdown("<div class='secondary-btn'>", unsafe_allow_html=True)
        if st.button("⬅️ Back", use_container_width=True, key="ex_back_btn"):
            goto("language")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_next:
        st.markdown("<div class='primary-btn'>", unsafe_allow_html=True)
        # Only enable Next if a selection was made
        if st.button("➡️ Next", use_container_width=True, key="ex_next_btn",
                     disabled=(st.session_state.selected_example is None)):
            goto("spacing_examples")
        st.markdown("</div>", unsafe_allow_html=True)
