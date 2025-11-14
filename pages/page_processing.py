import streamlit as st
import time
from utils.css import inject_global_css
from app import goto
from backend import simplify_text_with_nlp


def render():
    inject_global_css()

    st.markdown("""
    <h1 style='color:#7C3AED; font-weight:800;'>
        Processing Your Text...
    </h1>
    <p style='color:gray; font-size:18px; margin-top:-10px;'>
        This may take a few seconds depending on text length
    </p>
    """, unsafe_allow_html=True)

    # -----------------------------------
    # Show progress bar animation
    # -----------------------------------
    progress = st.progress(0)
    status = st.empty()

    steps = [
        "Loading language model...",
        "Analyzing text...",
        "Extracting important phrases...",
        "Simplifying sentences...",
        "Finalizing output..."
    ]

    for i, msg in enumerate(steps):
        status.write(msg)
        progress.progress((i + 1) / len(steps))
        time.sleep(0.5)

    status.empty()
    progress.empty()

    # -----------------------------------
    # Call NLP + Summarization backend
    # -----------------------------------

    raw_text = st.session_state.text_input
    target_words = st.session_state.desired_word_count

    # Telugu or English?
    lang_code = "tel_Telu" if st.session_state.lang == "తెలుగు" else "eng_Latn"

    # These options come from page_input.py
    simplify_vocab = st.session_state.opt_simplify_vocab
    split_long = st.session_state.opt_split_long

    try:
        simplified = simplify_text_with_nlp(
            raw_text,
            target_language=lang_code,
            simplify_vocab=simplify_vocab,
            split_sentences=split_long,
            target_words=target_words,
        )

        st.session_state.simplified_text = simplified

        # Short pause for smoother UX
        time.sleep(0.3)

        goto("result")

    except Exception as e:
        st.error(f"❌ Failed to process text: {e}")
        st.info("Try reducing text length or check your GPU environment.")
