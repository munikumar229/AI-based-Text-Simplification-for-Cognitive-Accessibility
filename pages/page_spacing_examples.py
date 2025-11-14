import streamlit as st
from utils.css import inject_global_css
from utils.db import load_user_selection, save_user_selection
from app import goto


def render():
    inject_global_css()

    lang = st.session_state.lang
    user = st.session_state.user or "guest"

    st.markdown("""
    <h1 style='color:#7C3AED; font-weight:800;'>Spacing Preference</h1>
    <p style='color:gray; font-size:18px; margin-top:-8px;'>
        Choose which spacing style feels easier to read
    </p>
    """, unsafe_allow_html=True)

    # ------------------------------
    # Base Example Text
    # ------------------------------
    if lang == "English":
        example_text = "The quick brown fox jumps over the lazy dog."
    else:
        example_text = "వంద బోధనే తుమ్హి రాజు శాసనే రాష్ట్రం ప్రజల ప్రియమే"

    # ------------------------------
    # Load previous selection once
    # ------------------------------
    if st.session_state.selected_spacing_example is None:
        st.session_state.selected_spacing_example = load_user_selection(user, "spacing_examples")

    selected = st.session_state.selected_spacing_example

    # ------------------------------
    # Render two spacing example cards
    # ------------------------------
    col1, col2 = st.columns(2)

    # LEFT - normal spacing
    with col1:
        is_sel = (selected == "left")
        css_class = "example-card selected" if is_sel else "example-card"

        if st.button(" ", key="spacing_left_btn"):
            st.session_state.selected_spacing_example = "left"
            save_user_selection(user, "spacing_examples", "left")
            goto("questionnaire")

        st.markdown(
            f"<div class='{css_class}'>{example_text}</div>",
            unsafe_allow_html=True
        )

    # RIGHT - wider spacing
    with col2:
        is_sel = (selected == "right")
        css_class = "example-card selected" if is_sel else "example-card"

        if st.button(" ", key="spacing_right_btn"):
            st.session_state.selected_spacing_example = "right"
            save_user_selection(user, "spacing_examples", "right")
            goto("questionnaire")

        st.markdown(
            f"<div class='{css_class}' style='letter-spacing: 4px;'>{example_text}</div>",
            unsafe_allow_html=True
        )

    st.write("")
    st.write("")

    # ------------------------------
    # Navigation Buttons
    # ------------------------------
    col_back, col_next = st.columns(2)

    # BACK
    with col_back:
        st.markdown("<div class='secondary-btn'>", unsafe_allow_html=True)
        if st.button("⬅️ Back", key="spacing_back_btn", use_container_width=True):
            goto("examples")
        st.markdown("</div>", unsafe_allow_html=True)

    # NEXT
    with col_next:
        st.markdown("<div class='primary-btn'>", unsafe_allow_html=True)
        if st.button(
            "➡️ Next",
            key="spacing_next_btn",
            use_container_width=True,
            disabled=(st.session_state.selected_spacing_example is None)
        ):
            goto("questionnaire")
        st.markdown("</div>", unsafe_allow_html=True)
