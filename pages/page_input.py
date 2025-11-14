import streamlit as st
from utils.css import inject_global_css
from app import goto
from io import StringIO


def render():
    inject_global_css()

    lang = st.session_state.lang

    # ------------------------------
    # Localization
    # ------------------------------
    if lang == "English":
        t_title = "Enter your text"
        t_paste = "📋 Paste Text"
        t_upload = "📁 Upload File"
        t_placeholder = "Paste your text here..."
        t_back = "⬅️ Back"
        t_next = "✨ Simplify"
        t_word_label = "Number of words"
        t_word_help = "This is the approximate length of the simplified text."
        t_split = "Split long sentences"
        t_vocab = "Simplify vocabulary"
    else:
        t_title = "మీ పాఠ్యాన్ని ఇవ్వండి"
        t_paste = "📋 పాఠ్యం అతికించండి"
        t_upload = "📁 ఫైల్ అప్‌లోడ్ చేయండి"
        t_placeholder = "మీ పాఠ్యాన్ని ఇక్కడ అతికించండి..."
        t_back = "⬅️ వెనక్కి"
        t_next = "✨ సరళీకరించు"
        t_word_label = "పదాల సంఖ్య"
        t_word_help = "సరళీకృత పాఠ్యం సుమారుగా ఇన్ని పదాలు ఉంటుంది."
        t_split = "పొడవైన వాక్యాలను విభజించు"
        t_vocab = "పదజాలాన్ని సరళీకరించు"

    # ------------------------------
    # PAGE TITLE
    # ------------------------------
    st.markdown(f"""
        <h1 style='color:#7C3AED; font-weight:800;'>{t_title}</h1>
    """, unsafe_allow_html=True)

    st.write("")

    # ------------------------------------------------------------
    # Input mode: paste / upload
    # ------------------------------------------------------------
    if "input_mode" not in st.session_state:
        st.session_state.input_mode = "paste"

    col1, col2 = st.columns(2)

    # Paste mode button
    with col1:
        css = "primary-btn" if st.session_state.input_mode == "paste" else "outline-btn"
        st.markdown(f"<div class='{css}'>", unsafe_allow_html=True)
        if st.button(t_paste, key="paste_mode_btn", use_container_width=True):
            st.session_state.input_mode = "paste"
        st.markdown("</div>", unsafe_allow_html=True)

    # Upload mode button
    with col2:
        css = "primary-btn" if st.session_state.input_mode == "upload" else "outline-btn"
        st.markdown(f"<div class='{css}'>", unsafe_allow_html=True)
        if st.button(t_upload, key="upload_mode_btn", use_container_width=True):
            st.session_state.input_mode = "upload"
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # ------------------------------------------------------------
    # Paste Mode
    # ------------------------------------------------------------
    if st.session_state.input_mode == "paste":
        text = st.text_area(
            "",
            height=220,
            placeholder=t_placeholder,
            value=st.session_state.text_input,
            label_visibility="collapsed",
            key="paste_text_area"
        )
        st.session_state.text_input = text.strip()

    # ------------------------------------------------------------
    # Upload Mode
    # ------------------------------------------------------------
    else:
        uploaded = st.file_uploader(t_upload, type=["txt"], key="txt_uploader")
        if uploaded:
            try:
                content = uploaded.getvalue().decode("utf-8")
                st.session_state.text_input = content.strip()
                st.success("File uploaded successfully!")
            except UnicodeDecodeError:
                st.error("Unable to decode file. Please upload a UTF-8 encoded .txt file.")

        st.write("")
        st.markdown("<h4>Extracted Text</h4>", unsafe_allow_html=True)
        st.text_area("", value=st.session_state.text_input, height=200, key="upload_preview", disabled=True)

    st.write("")
    st.write("")

    # ------------------------------------------------------------
    # Word count slider
    # ------------------------------------------------------------
    st.markdown(f"<h3>{t_word_label}</h3>", unsafe_allow_html=True)

    st.session_state.desired_word_count = st.slider(
        t_word_label,
        50, 300,
        st.session_state.desired_word_count,
        step=10,
        help=t_word_help
    )

    st.write("")
    st.write("")

    # ------------------------------------------------------------
    # Simplification options
    # ------------------------------------------------------------
    st.markdown("<h3>🛠️ Simplification Options</h3>", unsafe_allow_html=True)

    colA, colB = st.columns(2)

    with colA:
        st.session_state.opt_split_long = st.checkbox(
            t_split, 
            value=st.session_state.get("opt_split_long", True),
            key="split_checkbox"
        )

    with colB:
        st.session_state.opt_simplify_vocab = st.checkbox(
            t_vocab,
            value=st.session_state.get("opt_simplify_vocab", True),
            key="vocab_checkbox"
        )

    st.write("")
    st.write("")

    # ------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------
    col_back, col_next = st.columns(2)

    # BACK BUTTON
    with col_back:
        st.markdown("<div class='secondary-btn'>", unsafe_allow_html=True)
        if st.button(t_back, use_container_width=True):
            goto("questionnaire")
        st.markdown("</div>", unsafe_allow_html=True)

    # NEXT BUTTON
    with col_next:
        disabled = not st.session_state.text_input.strip()
        st.markdown("<div class='primary-btn'>", unsafe_allow_html=True)
        if st.button(t_next, use_container_width=True, disabled=disabled):
            goto("processing")
        st.markdown("</div>", unsafe_allow_html=True)
