import streamlit as st
import time
from io import StringIO
import pyttsx3
import io
import streamlit.components.v1 as components

# Import backend functions
from backend import simplify_text_with_nlp, generate_tts_audio

# Compatibility for rerun
if not hasattr(st, 'experimental_rerun'):
    st.experimental_rerun = st.rerun

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="Text Simplifier — English & Telugu", layout="centered")

# ------------------------------
# Custom CSS
# ------------------------------
st.markdown("""
<style>
/* Center heading and buttons nicely */
h1, h3, p { text-align: center; }

.lang-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 80px;
    margin-top: 50px;
}

.lang-card {
    width: 220px;
    height: 220px;
    border-radius: 20px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    cursor: pointer;
    transition: all 0.25s ease;
    background-color: #EDE9FE;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.lang-card:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}
.lang-letter {
    font-size: 100px;
    font-weight: 800;
    color: #5B21B6;
    margin-bottom: 10px;
}

.lang-name {
    font-size: 20px;
    font-weight: 500;
    color: #333;
    width: 220px;
}
.output {
    border-radius: 12px;
    padding: 20px;
    margin-top: 10px;
}

/* Harder buttons */
.harder-btn button {
    border-radius: 10px !important;
    height: 50px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    margin: 6px 4px !important;
    border: 1px solid #ccc !important;
    background-color: white !important;
    color: #333 !important;
    transition: all 0.25s ease-in-out !important;
}
.harder-btn button:hover {
    transform: scale(1.05);
}
.harder-btn.selected button {
    background-color: #22c55e !important;
    color: white !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Helper
# ------------------------------
def simplify_text(txt, simplify_vocab=True, split_sentences=True, target_words=100):
    if not txt.strip():
        return ""
    txt = " ".join(txt.split())
    if split_sentences:
        txt = txt.replace(",", ".")
    if simplify_vocab:
        simple_map = {
            "approximately": "about",
            "consequently": "so",
            "demonstrate": "show",
            "nevertheless": "still",
            "however": "but",
            "therefore": "so",
        }
        for k, v in simple_map.items():
            txt = txt.replace(k, v)
    words = txt.split()
    return " ".join(words[:target_words]) + ("..." if len(words) > target_words else "")

# ------------------------------
# Session State
# ------------------------------
for key, default in {
    "page": "welcome",
    "lang": None,
    "harder": None,
    "obstacles": [],
    "font_size": 18,
    "line_height": 1.6,
    "letter_spacing": 0.02,
    "summary_len": 120,  # Keep for backward compatibility
    "simplified": None,
    "theme": "Light",
    "reading_assist": False,
    "text_input": "",
    "audio_rate": 1.0,
    "show_comparison": False,
    "desired_word_count": 120,  # New: user-controlled word count
    "bold_letters": False,  # For bolding letters feature
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ------------------------------
# Translations
# ------------------------------
def get_texts(lang):
    if lang == "English":
        return {
            "choose_language": "🌐 Choose your language",
            "harder": "What's harder for you?",
            "reading": "Reading the text",
            "understanding": "Understanding the meaning",
            "obstacles": "What gets in the way?",
            "prefs": "🛠️ Reading Preferences",
            "text_input": "✍️ Enter your text",
            "placeholder_paste": "Paste your text here...",
            "upload_label": "Upload .txt file",
            "tab_paste": "Paste",
            "tab_upload": "Upload",
            "simplify": "Simplify",
            "processing": "Simplifying your text...",
            "result": "🪄 Simplified Output",
            "reading_assist": "Reading Assist",
            "download": "⬇️ Download Simplified Text",
            "back": "⬅️ Back",
            "next": "➡️ Next",
            "theme": "Theme",
            "font_size_label": "Font size",
            "line_spacing_label": "Line spacing",
            "letter_spacing_label": "Letter spacing",
            
            # Obstacle labels
            "small_text": "Small text",
            "tight_spacing": "Tight spacing",
            "dense_paragraphs": "Dense paragraphs",
            "complex_words": "Complex words",
            "long_sentences": "Long sentences",
            "busy_layout": "Busy layout",
            
            # Misc
            "font_preferences": "Font & Layout Preferences",
            "reading_difficulty": "Reading Difficulty",
            "language_detected": "Detected language",
            "apply_changes": "Apply Changes",
            "simplify_now": "Simplify Now",
            "audio_controls": "Audio Controls",
            "text_layout_settings": "Text Layout Settings",
            "speech_speed_label": "Speech Speed (x)",
            "play": "Play",
            "pause": "Pause",
            "mute": "Mute",
            "play_audio": "Play Audio",
            "simplified_text": "Simplified Text",
            "original_text": "Original Text",
            "compare_with_original": "Compare with Original",
            "light_theme": "Light",
            "sepia_theme": "Sepia",
            "dark_theme": "Dark",
            "word_count_label": "Number of words",
            "current_word_count": "Current: {current} words | Target: {target} words",
            "resimplify_button": "Re-simplify with New Word Count",
            "home": "🏠 Home",
            "app_title": "🧠 Text Simplifier",
            "app_subtitle": "AI-powered Text Simplifier • English & Telugu • Reading Assist • TTS",
            "english_label": "English",
            "telugu_label": "తెలుగు",
            "paste_text": "📋 Paste Text",
            "upload_file": "📁 Upload File",
            "speed_control": "🎵 Speed Control",
            "target_words": "🎯 Target: {count} words",
            "approx_length": "This will be the approximate length of your simplified text",
            "word_count_help": "Set the desired number of words in the simplified text",
            "adjust_word_count": "Adjust the number of words in the simplified text",
        }

    else:
        return {
            "choose_language": "🌐 మీ భాషను ఎంచుకోండి",
            "harder": "ఏది కష్టం?",
            "reading": "పాఠ్యం చదవడం",
            "understanding": "అర్థం చేసుకోవడం",
            "obstacles": "ఏవి అడ్డుగా ఉన్నాయి?",
            "prefs": "🛠️ పఠన ప్రాధాన్యతలు",
            "text_input": "✍️ మీ పాఠ్యాన్ని ఇవ్వండి",
            "placeholder_paste": "మీ పాఠ్యాన్ని ఇక్కడ అతికించండి...",
            "upload_label": ".txt ఫైల్ అప్‌లోడ్ చేయండి",
            "tab_paste": "అతికించు",
            "tab_upload": "అప్‌లోడ్",
            "simplify": "సరళీకరించు",
            "processing": "మీ పాఠ్యం సరళీకరించబడుతోంది...",
            "result": "🪄 సరళీకృత పాఠ్యం",
            "reading_assist": "పఠన సహాయం",
            "download": "⬇️ సరళీకృత పాఠ్యాన్ని డౌన్‌లోడ్ చేయి",
            "back": "⬅️ వెనక్కి",
            "next": "➡️ ముందుకు",
            "theme": "థీమ్",
            "font_size_label": "అక్షర పరిమాణం",
            "line_spacing_label": "వరుస మధ్య ఖాళీ",
            "letter_spacing_label": "అక్షర మధ్య ఖాళీ",
            
            # Obstacle labels (Telugu)
            "small_text": "చిన్న అక్షరాలు",
            "tight_spacing": "తక్కువ స్పేసింగ్",
            "dense_paragraphs": "ఘనమైన పేరాగ్రాఫ్‌లు",
            "complex_words": "సంక్లిష్ట పదాలు",
            "long_sentences": "పొడవైన వాక్యాలు",
            "busy_layout": "బిజీ లేఅవుట్",
            
            # Misc
            "font_preferences": "అక్షరాలు మరియు లేఅవుట్ ప్రాధాన్యతలు",
            "reading_difficulty": "పఠన క్లిష్టత",
            "language_detected": "గుర్తించబడిన భాష",
            "apply_changes": "మార్పులను వర్తింపజేయి",
            "simplify_now": "ఇప్పుడే సరళీకరించు",
            "audio_controls": "ఆడియో నియంత్రణలు",
            "text_layout_settings": "పాఠ్య లేఅవుట్ సెట్టింగులు",
            "speech_speed_label": "మాట్లాడే వేగం (x)",
            "play": "ప్లే",
            "pause": "పాజ్",
            "mute": "మ్యూట్",
            "play_audio": "ఆడియో ప్లే చేయు",
            "simplified_text": "సరళీకృత పాఠ్యం",
            "original_text": "అసలు పాఠ్యం",
            "compare_with_original": "అసలుతో పోల్చు",
            "light_theme": "లైట్",
            "sepia_theme": "సెపియా",
            "dark_theme": "డార్క్",
            "word_count_label": "పదాల సంఖ్య",
            "current_word_count": "ప్రస్తుతం: {current} పదాలు | లక్ష్యం: {target} పదాలు",
            "resimplify_button": "కొత్త పదాల సంఖ్యతో మళ్లీ సరళీకరించు",
            "home": "🏠 హోమ్",
            "app_title": "🧠 పాఠ్య సరళీకరణ",
            "app_subtitle": "AI-ఆధారిత పాఠ్య సరళీకరణ • ఇంగ్లీష్ & తెలుగు • పఠన సహాయం • TTS",
            "english_label": "ఇంగ్లీష్",
            "telugu_label": "తెలుగు",
            "paste_text": "📋 పాఠ్యం అతికించండి",
            "upload_file": "📁 ఫైల్ అప్‌లోడ్ చేయండి",
            "speed_control": "🎵 వేగం నియంత్రణ",
            "target_words": "🎯 లక్ష్యం: {count} పదాలు",
            "approx_length": "ఇది మీ సరళీకృత పాఠ్యం యొక్క సుమారు పొడవు అవుతుంది",
            "word_count_help": "సరళీకృత పాఠ్యంలో కావలసిన పదాల సంఖ్యను సెట్ చేయండి",
            "adjust_word_count": "సరళీకృత పాఠ్యంలో పదాల సంఖ్యను సర్దుబాటు చేయండి",
        }

# ------------------------------
# Pages
# ------------------------------
def page_welcome():
    # Custom CSS styling for centering + button
    st.markdown("""
        <style>
        /* Center the whole page vertically and horizontally */
        .welcome-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 85vh;
            text-align: center;
        }

        /* Title styling */
        .welcome-title {
            font-size: 52px;
            font-weight: 800;
            color: #7C3AED;
            margin-bottom: 15px;
        }

        /* Subtitle styling */
        .welcome-subtitle {
            font-size: 20px;
            color: gray;
            margin-bottom: 40px;
        }

        /* Custom Streamlit button styling */
        div[data-testid="stButton"] > button {
            background-color: #22c55e !important;
            color: white !important;
            border: none !important;
            padding: 15px 40px !important;
            font-size: 20px !important;
            font-weight: 600 !important;
            border-radius: 12px !important;
            cursor: pointer !important;
            transition: all 0.25s ease-in-out !important;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1) !important;
        }
        div[data-testid="stButton"] > button:hover {
            transform: scale(1.05);
            background-color: #16a34a !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Centered layout
    st.markdown("""
        <div class="welcome-container">
            <div class="welcome-title">🧠 Text Simplifier</div>
            <div class="welcome-subtitle">
                AI-powered Text Simplifier • English & Telugu • Reading Assist • TTS
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Center the button below content
    _, col, _ = st.columns([1, 2, 1])
    with col:
        if st.button("🚀 Get Started", use_container_width=True):
            st.session_state.page = "language"
            st.rerun()
def page_language():
    t = get_texts("English")  # Default to English for language selection page

    # ---------------- CSS Styling ----------------
    st.markdown("""
        <style>
        /* Container layout */
        .lang-container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 40px;
            flex-wrap: wrap;
            margin-top: 60px;
        }

        /* Common button styles for both cards */
        div[data-testid="stButton"] > button {
            height: 220px !important;
            width: 220px !important;
            border-radius: 20px !important;
            background-color: #EDE9FE !important;
            border: none !important;
            color: #5B21B6 !important;
            font-size: 200px !important;
            font-weight: 800 !important;
            text-align: center !important;
            position: relative !important;
            overflow: hidden !important;
            transition: all 0.25s ease !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1) !important;
        }
        div[data-testid="stMarkdownContainer"] > p{
            font-size: 150px;        
        }

        /* English flag watermark */
        div[data-testid="stButton"][key="english_btn"] > button::before {
            content: "";
            position: absolute;
            inset: 0;
            background-image: url("https://flagcdn.com/w320/gb.png");
            background-size: cover;
            background-position: center;
            opacity: 0.08;
        }

        /* Telugu (India) flag watermark */
        div[data-testid="stButton"][key="telugu_btn"] > button::before {
            content: "";
            position: absolute;
            inset: 0;
            background-image: url("https://flagcdn.com/w320/in.png");
            background-size: cover;
            background-position: center;
            opacity: 0.08;
        }

        /* Hover animation */
        div[data-testid="stButton"] > button:hover {
            transform: scale(1.06);
            background-color: #DDD6FE !important;
            box-shadow: 0 8px 20px rgba(0,0,0,0.15) !important;
        }

        /* Language label under the box */
        .lang-name {
            text-align: center;
            font-size: 30px;
            font-weight: 600;
            color: #333;
            margin-top: 10px;
            cursor: pointer;
            transition: color 0.25s ease;
        }
        .lang-name:hover {
            color: #5B21B6;
        }

        /* Center text headers */
        h1, h3, p { text-align: center; }
        </style>

        <div style='text-align:center;'>
            <h1 style='color:#7C3AED; font-weight:800;'>Text Summarizier</h1>
            <p style='color:gray; margin-top:-10px;'></p>
            <h3 style='margin-top:40px;'>Choose your Language</h3>
        </div>
    """, unsafe_allow_html=True)

    # Layout
    col1, col2 = st.columns(2)

    with col1:
        if st.button("E", key="english_btn"):
            st.session_state.lang = "English"
            st.session_state.page = "questionnaire"
            st.experimental_rerun()
        
        st.markdown(f"<div class='lang-name'>{t['english_label']}</div>", unsafe_allow_html=True)

    with col2:
        if st.button("త", key="telugu_btn"):
            st.session_state.lang = "తెలుగు"
            st.session_state.page = "questionnaire"
            st.experimental_rerun()
        
        st.markdown(f"<div class='lang-name'>{t['telugu_label']}</div>", unsafe_allow_html=True)


def page_questionnaire():
    t = get_texts(st.session_state.lang)

    # ------------------- CSS Styling -------------------
    st.markdown("""
        <style>
        /* Center headings */
        h3 { text-align: center; }

        /* Harder as toggle buttons */
        div.row-widget.stRadio > div {
            display: flex;
            justify-content: center;
            gap: 20px;
        }

        div.row-widget.stRadio label {
            background-color: white;
            color: #333;
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 10px 24px;
            font-weight: 500;
            transition: all 0.25s ease-in-out;
            cursor: pointer;
        }

        div.row-widget.stRadio label:hover {
            transform: scale(1.05);
            border-color: #22c55e;
        }

        /* selected option */
        div.row-widget.stRadio div[role="radiogroup"] label[data-testid="stMarkdownContainer"][aria-checked="true"],
        div.row-widget.stRadio div[role="radiogroup"] label[aria-checked="true"] {
            background-color: #22c55e !important;
            color: white !important;
            border: none !important;
        }

        /* Hide default radio circles */
        div.row-widget.stRadio input[type="radio"] {
            display: none;
        }

        /* Common obstacle button base */
        .obstacle-btn button {
            border-radius: 10px !important;
            height: 50px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            margin: 6px 4px !important;
            border: 1px solid #ccc !important;
            background-color: white !important;
            color: #333 !important;
            transition: all 0.25s ease-in-out !important;
        }
        .obstacle-btn button:hover {
            transform: scale(1.05);
        }
        .obstacle-btn.selected button {
            background-color: #22c55e !important;
            color: white !important;
            border: none !important;
        }
        button[data-testid="stBaseButton-secondary"]:active {
                background-color: #0f0;
        }
        </style>
    """, unsafe_allow_html=True)

    # ------------------- Section 1: Harder -------------------
    st.markdown(f"<h3>{t['harder']}</h3>", unsafe_allow_html=True)
    
    # Harder as toggle buttons
    col1, col2 = st.columns(2)
    with col1:
        selected = st.session_state.harder == t["reading"]
        css_class = "harder-btn selected" if selected else "harder-btn"
        st.markdown(f"<div class='{css_class}'>", unsafe_allow_html=True)
        if st.button(("✅ " if selected else "") + t["reading"], key="reading_btn", use_container_width=True):
            st.session_state.harder = t["reading"]
            st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        selected = st.session_state.harder == t["understanding"]
        css_class = "harder-btn selected" if selected else "harder-btn"
        st.markdown(f"<div class='{css_class}'>", unsafe_allow_html=True)
        if st.button(("✅ " if selected else "") + t["understanding"], key="understanding_btn", use_container_width=True):
            st.session_state.harder = t["understanding"]
            st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ------------------- Section 2: Obstacles -------------------
    st.markdown(f"<h3 style='margin-top:30px;'>{t['obstacles']}</h3>", unsafe_allow_html=True)

    # Label options by language
    if st.session_state.lang == "తెలుగు":
        options = [
            ("చిన్న అక్షరాలు", "small_text"),
            ("తక్కువ స్పేసింగ్", "tight_spacing"),
            ("ఘనమైన పేరాగ్రాఫ్‌లు", "dense_paragraphs"),
            ("సంక్లిష్ట పదాలు", "complex_words"),
            ("పొడవైన వాక్యాలు", "long_sentences"),
            ("బిజీ లేఅవుట్", "busy_layout"),
        ]
    else:
        options = [
            ("Small text", "small_text"),
            ("Tight spacing", "tight_spacing"),
            ("Dense paragraphs", "dense_paragraphs"),
            ("Complex words", "complex_words"),
            ("Long sentences", "long_sentences"),
            ("Busy layout", "busy_layout"),
        ]

    # Render buttons
    cols = st.columns(3)
    for i, (label, key) in enumerate(options):
        col = cols[i % 3]
        with col:
            selected = key in st.session_state.obstacles
            css_class = "obstacle-btn selected" if selected else "obstacle-btn"
            with st.container():
                st.markdown(f"<div class='{css_class}'>", unsafe_allow_html=True)
                if st.button(("✅ " if selected else "") + label, key=f"{key}_btn", use_container_width=True):
                    if selected:
                        st.session_state.obstacles.remove(key)
                    else:
                        st.session_state.obstacles.append(key)
                    st.experimental_rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    # ------------------- Section 3: Preferences -------------------
    st.divider()
    st.markdown(f"<h3>🛠️ {t['prefs']}</h3>", unsafe_allow_html=True)
    colA, colB, colC = st.columns(3)
    with colA:
        st.session_state.font_size = st.slider(t["font_size_label"], 14, 30, st.session_state.font_size, key="prefs_font_size")
    with colB:
        st.session_state.line_height = st.slider(t["line_spacing_label"], 1.2, 4.0, st.session_state.line_height, step=0.1, key="prefs_line_spacing")
    with colC:
        st.session_state.letter_spacing = st.slider(t["letter_spacing_label"], 0.0, 0.3, st.session_state.letter_spacing, step=0.01, key="prefs_letter_spacing")

    # ------------------- Section 4: Navigation -------------------
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t["back"], use_container_width=True):
            st.session_state.page = "language"
            st.experimental_rerun()
    with col2:
        if st.button(t["next"], use_container_width=True):
            st.session_state.page = "input"
            st.experimental_rerun()

def page_input():
    t = get_texts(st.session_state.lang)

    # ---------------- CSS ----------------
    st.markdown("""
        <style>
        h3 { text-align: center; }

        /* Mode buttons (Paste / Upload) */
        .mode-btn button {
            border-radius: 10px !important;
            height: 55px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            margin: 6px 4px !important;
            border: 1px solid #ccc !important;
            background-color: white !important;
            color: #333 !important;
            transition: all 0.25s ease-in-out !important;
        }
        .mode-btn button:hover {
            transform: scale(1.05);
            border-color: #22c55e !important;
        }
        .mode-btn.selected button {
            background-color: #22c55e !important;
            color: white !important;
            border: none !important;
        }

        textarea {
            border-radius: 10px !important;
            font-size: 16px !important;
            padding: 12px !important;
        }

        /* Simplify button styling */
        div[data-testid="stButton"][key="input_simplify_btn"] > button {
            background-color: #22c55e !important;
            color: white !important;
            border-radius: 10px !important;
            font-size: 18px !important;
            font-weight: 600 !important;
            height: 55px !important;
            border: none !important;
            transition: all 0.25s ease !important;
        }
        div[data-testid="stButton"][key="input_simplify_btn"] > button:hover {
            transform: scale(1.05);
            background-color: #16a34a !important;
        }

        /* Back button styling */
        div[data-testid="stButton"][key="input_back_btn"] > button {
            background-color: #E5E7EB !important;
            color: #333 !important;
            border-radius: 10px !important;
            font-size: 18px !important;
            font-weight: 600 !important;
            height: 55px !important;
            transition: all 0.25s ease !important;
            border: none !important;
        }
        div[data-testid="stButton"][key="input_back_btn"] > button:hover {
            transform: scale(1.05);
            background-color: #D1D5DB !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # ---------------- Header ----------------
    st.markdown(f"<h3>{t['text_input']}</h3>", unsafe_allow_html=True)

    # ------------- Mode Selection -------------
    if "input_mode" not in st.session_state:
        st.session_state.input_mode = "paste"

    # localized labels
    paste_label = t["paste_text"]
    upload_label = t["upload_file"]

    col1, col2 = st.columns(2)
    with col1:
        selected = st.session_state.input_mode == "paste"
        css_class = "mode-btn selected" if selected else "mode-btn"
        st.markdown(f"<div class='{css_class}'>", unsafe_allow_html=True)
        if st.button(paste_label, key="paste_mode_btn", use_container_width=True):
            st.session_state.input_mode = "paste"
            st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        selected = st.session_state.input_mode == "upload"
        css_class = "mode-btn selected" if selected else "mode-btn"
        st.markdown(f"<div class='{css_class}'>", unsafe_allow_html=True)
        if st.button(upload_label, key="upload_mode_btn", use_container_width=True):
            st.session_state.input_mode = "upload"
            st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ------------- Paste / Upload area -------------
    text_input = st.session_state.text_input

    if st.session_state.input_mode == "paste":
        # LIVE update (no Ctrl+Enter required)
        new_text = st.text_area(
            " ",
            height=220,
            placeholder=t["placeholder_paste"],
            value=text_input,
            key="paste_textarea"
        )
        # Always store updated text
        st.session_state.text_input = new_text.strip()

    else:
        uploaded_file = st.file_uploader(t["upload_label"], type=["txt"], key="upload_file_input")
        if uploaded_file is not None:
            if not uploaded_file.name.lower().endswith('.txt'):
                st.error("Please upload a .txt file only. Re-upload the correct file.")
            else:
                try:
                    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                    uploaded_text = stringio.read()
                    st.session_state.text_input = uploaded_text.strip()
                except UnicodeDecodeError:
                    st.error("Unable to decode the file. Please ensure it's a valid text file and re-upload.")

    # ------------- Word Count Settings -------------
    st.divider()
    st.markdown(f"**📝 {t['word_count_label']}**")
    col_word_settings = st.columns([2, 1])
    
    with col_word_settings[0]:
        st.session_state.desired_word_count = st.slider(
            t["word_count_label"], 
            50, 300, 
            st.session_state.desired_word_count, 
            step=10,
            help=t["word_count_help"],
            key="input_word_count_slider"
        )
    
    with col_word_settings[1]:
        st.markdown(f"**{t['target_words'].format(count=st.session_state.desired_word_count)}**")
        st.caption(t["approx_length"])

    # ------------- Navigation buttons -------------
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t["back"], use_container_width=True, key="input_back_btn"):
            st.session_state.page = "questionnaire"
            st.experimental_rerun()
    with col2:
        simplify_disabled = not st.session_state.text_input.strip()
        if st.button(f"✨ {t['simplify']}", use_container_width=True, disabled=simplify_disabled, key="input_simplify_btn"):
            st.session_state.page = "processing"
            st.experimental_rerun()

def page_processing():
    t = get_texts(st.session_state.lang)
    st.markdown(f"### {t['processing']}")
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.02)
        progress.progress(i + 1)
    
    # Use advanced NLP-based simplification
    target_lang = 'tel_Telu' if st.session_state.lang == "తెలుగు" else 'eng_Latn'
    st.session_state.simplified = simplify_text_with_nlp(
        st.session_state.text_input,
        target_language=target_lang,
        target_words=st.session_state.desired_word_count,
    )
    st.session_state.page = "result"
    st.experimental_rerun()

def page_result():
    t = get_texts(st.session_state.lang)
    simplified = st.session_state.simplified
    theme = st.session_state.theme
    bg_color = "#fff" if theme == "Light" else "#f4ecd8" if theme == "Sepia" else "#1a1a1a"
    text_color = "#000" if theme != "Dark" else "#fff"
    st.markdown(f"### {t['result']}")

    # --- Theme Toggle Buttons ---
    col_theme = st.columns(3)
    with col_theme[0]:
        if st.button(f"🌞 {t['light_theme']}", use_container_width=True):
            st.session_state.theme = "Light"
            st.experimental_rerun()
    with col_theme[1]:
        if st.button(f"📜 {t['sepia_theme']}", use_container_width=True):
            st.session_state.theme = "Sepia"
            st.experimental_rerun()
    with col_theme[2]:
        if st.button(f"🌙 {t['dark_theme']}", use_container_width=True):
            st.session_state.theme = "Dark"
            st.experimental_rerun()

    # --- Bold Letters Toggle ---
    if st.button("🔤 Bold Vowels" if not st.session_state.bold_letters else "🔤 Normal Text", use_container_width=True):
        st.session_state.bold_letters = not st.session_state.bold_letters
        st.experimental_rerun()

    # --- Simplified Text Display ---
    display_text = simplified
    if st.session_state.bold_letters:
        import re
        if st.session_state.lang == "తెలుగు":
            # Telugu vowels
            display_text = re.sub(r'([అఆఇఈఉఊఋౠఎఏఐఒఓఔ])', r'<b>\1</b>', display_text)
        else:
            # English vowels
            display_text = re.sub(r'([aeiouAEIOU])', r'<b>\1</b>', display_text)
    
    if not st.session_state.show_comparison:
        st.markdown(
            f"<div class='output' style='background:{bg_color}; color:{text_color}; font-size:{st.session_state.font_size}px; line-height:{st.session_state.line_height}; letter-spacing:{st.session_state.letter_spacing}em;'>{display_text}</div>",
            unsafe_allow_html=True,
        )

    # Comparison button
    if st.button(t["compare_with_original"], use_container_width=True):
        st.session_state.show_comparison = not st.session_state.show_comparison
        st.experimental_rerun()

    if st.session_state.show_comparison:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"### {t['original_text']}")
            st.markdown(
                f"<div class='output' style='background:{bg_color}; color:{text_color}; font-size:{st.session_state.font_size}px; line-height:{st.session_state.line_height}; letter-spacing:{st.session_state.letter_spacing}em;'>{st.session_state.text_input}</div>",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(f"### {t['simplified_text']}")
            st.markdown(
                f"<div class='output' style='background:{bg_color}; color:{text_color}; font-size:{st.session_state.font_size}px; line-height:{st.session_state.line_height}; letter-spacing:{st.session_state.letter_spacing}em;'>{display_text}</div>",
                unsafe_allow_html=True,
            )

    # Audio and Download buttons side by side
    col_audio, col_download = st.columns(2)
    with col_audio:
        if st.button(f"🔊 {t['play_audio']}", use_container_width=True):
            try:
                audio_file = generate_tts_audio(simplified, lang='en' if st.session_state.lang == "English" else 'te')
                st.audio(audio_file, format="audio/mp3")
            except Exception as e:
                st.error(f"Audio playback failed: {e}")
    with col_download:
        st.download_button(t["download"], simplified, "simplified.txt", use_container_width=True)

    # Audio controls in dropdown
    with st.expander(f"🔊 {t['audio_controls']}"):
        col_play, col_pause, col_mute = st.columns(3)
        with col_play:
            if st.button(f"▶️ {t['play']}", use_container_width=True):
                # Play logic
                pass
        with col_pause:
            if st.button(f"⏸️ {t['pause']}", use_container_width=True):
                # Pause logic
                pass
        with col_mute:
            if st.button(f"🔇 {t['mute']}", use_container_width=True):
                # Mute logic
                pass
        
        # Speed control with +/- buttons
        st.markdown(f"**{t['speed_control']}**")
        col_speed_minus, col_speed_display, col_speed_plus = st.columns([1, 2, 1])
        
        with col_speed_minus:
            if st.button("➖", key="speed_minus", help="Decrease speed"):
                st.session_state.audio_rate = max(0.25, st.session_state.audio_rate - 0.1)
                st.experimental_rerun()
        
        with col_speed_display:
            st.markdown(f"""
                <div style='text-align: center; font-size: 18px; font-weight: bold; padding: 8px;'>
                    {st.session_state.audio_rate:.1f}x
                </div>
            """, unsafe_allow_html=True)
        
        with col_speed_plus:
            if st.button("➕", key="speed_plus", help="Increase speed"):
                st.session_state.audio_rate = min(2.0, st.session_state.audio_rate + 0.1)
                st.experimental_rerun()
        
        # Speed control styling and slider
        st.markdown("""
            <style>
            div[data-testid="stSlider"][key="audio_rate_slider"] {
                text-align: center;
            }
            div[data-testid="stSlider"][key="audio_rate_slider"] label {
                font-size: 16px !important;
                font-weight: normal !important;
            }
            div[data-testid="stButton"][key="speed_minus"] > button,
            div[data-testid="stButton"][key="speed_plus"] > button {
                width: 50px !important;
                height: 50px !important;
                font-size: 24px !important;
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                margin: 0 auto !important;
                border-radius: 50% !important;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.session_state.audio_rate = st.slider(
            t["speech_speed_label"], 
            0.25, 2.0, 
            st.session_state.audio_rate, 
            step=0.1, 
            key="audio_rate_slider"
        )

    # --- Line and Letter Spacing Controls (moved to bottom) ---
   
    
    with st.expander(t['text_layout_settings']):
        col_controls = st.columns(2)
        
        # First column: Font and spacing controls
        with col_controls[0]:
            st.session_state.font_size = st.slider(t["font_size_label"], 14, 30, st.session_state.font_size, help="Adjust the font size of the text", key="font_size_slider")
            st.session_state.line_height = st.slider(t["line_spacing_label"], 1.2, 4.0, st.session_state.line_height, step=0.1, key="line_spacing_slider")
            st.session_state.letter_spacing = st.slider(t["letter_spacing_label"], 0.0, 0.3, st.session_state.letter_spacing, step=0.01, key="letter_spacing_slider")
        
        # Second column: Word count control
        with col_controls[1]:
            st.markdown(f"**📝 {t['word_count_label']}**")
            new_word_count = st.slider(
                t["word_count_label"], 
                50, 300, 
                st.session_state.desired_word_count, 
                step=10,
                help=t["adjust_word_count"],
                key="word_count_slider"
            )
            
            # Update desired word count
            if new_word_count != st.session_state.desired_word_count:
                st.session_state.desired_word_count = new_word_count
            
            # Show current word count
            current_words = len(simplified.split())
            st.caption(t["current_word_count"].format(current=current_words, target=st.session_state.desired_word_count))
            
            # Re-simplify button
            if st.button(f"🔄 {t['resimplify_button']}", use_container_width=True, key="resimplify_btn"):
                st.session_state.page = "processing"
                st.session_state.summary_len = st.session_state.desired_word_count
                st.experimental_rerun()

    col1, col2 = st.columns(2)
    with col1:
        if st.button(t["back"], use_container_width=True):
            st.session_state.page = "input"
            st.experimental_rerun()
    with col2:
        if st.button(t["home"], use_container_width=True):
            st.session_state.page = "language"
            st.experimental_rerun()

# ------------------------------
# Router
# ------------------------------
if st.session_state.page == "welcome":
    page_welcome()
elif st.session_state.page == "language":
    page_language()
elif st.session_state.page == "questionnaire":
    page_questionnaire()
elif st.session_state.page == "input":
    page_input()
elif st.session_state.page == "processing":
    page_processing()
elif st.session_state.page == "result":
    page_result()
