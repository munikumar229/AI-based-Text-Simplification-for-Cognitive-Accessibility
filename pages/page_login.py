import streamlit as st
from utils.css import inject_global_css
from app import goto


def render():
    inject_global_css()

    st.markdown("""
    <h1 style='color:#7C3AED; font-weight:800; margin-top:40px;'>
        🧠 Text Simplifier
    </h1>
    <p style='font-size:18px; color:gray; margin-top:-10px;'>
        AI-powered Simplification • English & Telugu • Reading Assist • TTS
    </p>
    """, unsafe_allow_html=True)

    st.write("")  # spacing

    st.markdown("<h3>Enter your name or continue as guest</h3>", unsafe_allow_html=True)

    username = st.text_input(
        "",
        placeholder="Your name",
        key="username_input",
        label_visibility="collapsed"
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='primary-btn'>", unsafe_allow_html=True)
        if st.button("Login", key="login_btn", use_container_width=True):
            if username.strip():
                st.session_state.user = username.strip()
                goto("language")
            else:
                st.warning("Please enter your name.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='secondary-btn'>", unsafe_allow_html=True)
        if st.button("Continue as Guest", key="guest_btn", use_container_width=True):
            st.session_state.user = "guest"
            goto("language")
        st.markdown("</div>", unsafe_allow_html=True)
