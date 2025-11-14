import streamlit as st
from utils.css import inject_global_css
from app import goto


def render():
    inject_global_css()

    st.markdown("""
    <h1 style='color:#7C3AED; font-weight:800; margin-top:25px;'>
        🌐 Choose Your Language
    </h1>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2 = st.columns(2)

    # ----------------------
    # English Card
    # ----------------------
    with col1:
        if st.button(" ", key="english_card_btn"):
            st.session_state.lang = "English"
            goto("examples")

        st.markdown("""
        <div class="lang-box" style="
            background-image: url('https://flagcdn.com/w320/gb.png');
            background-size: cover;
            background-position: center;
            opacity: 0.95;
        ">
            E
        </div>
        <div class="lang-label">English</div>
        """, unsafe_allow_html=True)

    # ----------------------
    # Telugu Card
    # ----------------------
    with col2:
        if st.button(" ", key="telugu_card_btn"):
            st.session_state.lang = "తెలుగు"
            goto("examples")

        st.markdown("""
        <div class="lang-box" style="
            background-image: url('https://flagcdn.com/w320/in.png');
            background-size: cover;
            background-position: center;
            opacity: 0.95;
        ">
            త
        </div>
        <div class="lang-label">తెలుగు</div>
        """, unsafe_allow_html=True)
