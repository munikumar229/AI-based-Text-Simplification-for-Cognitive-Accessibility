import streamlit as st

# ---------------------------
# GLOBAL SESSION INITIALIZER
# ---------------------------

def init_session_state():

    defaults = {
        "user": None,
        "lang": None,
        "selected_example": None,
        "selected_spacing_example": None,

        # Summary & processing
        "text_input": "",
        "desired_word_count": 120,
        "simplified_text": None,

        # UI prefs
        "font_size": 18,
        "line_height": 1.6,
        "letter_spacing": 0.02,
        "theme": "Light",
        "assist_on": True,
        "bold_first_n": 2,
        "char_assist": True,
        "bold_letters": False,
        "color_letters": False,

        # TTS
        "tts_autoplay": False,
        "audio_rate": 1.0,

        # Navigation
        "page": "login",
        "show_comparison": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# Initialize session
init_session_state()


# ---------------------------
# PAGE ROUTING
# ---------------------------
def goto(page_name: str):
    st.session_state.page = page_name
    st.rerun()


# ---------------------------
# MAIN ROUTER
# ---------------------------

def main():
    page = st.session_state.page

    if page == "login":
        from pages.page_login import render
        render()

    elif page == "language":
        from pages.page_language import render
        render()

    elif page == "examples":
        from pages.page_examples import render
        render()

    elif page == "spacing_examples":
        from pages.page_spacing_examples import render
        render()

    elif page == "questionnaire":
        from pages.page_questionnaire import render
        render()

    elif page == "input":
        from pages.page_input import render
        render()

    elif page == "processing":
        from pages.page_processing import render
        render()

    elif page == "result":
        from pages.page_result import render
        render()

    else:
        st.error("Unknown page: " + page)


if __name__ == "__main__":
    main()
