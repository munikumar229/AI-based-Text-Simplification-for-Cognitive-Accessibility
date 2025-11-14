import streamlit as st

def inject_global_css():
    css = """
    <style>

    /* Global page layout */
    body, html {
        margin: 0;
        padding: 0;
    }

    h1, h2, h3, h4 {
        text-align: center;
        font-family: 'Inter', sans-serif;
    }

    /* Standard card container */
    .example-card {
        background: #f3e8ff;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        line-height: 1.6;
        font-size: 18px;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.08);
        transition: 0.2s;
        min-height: 180px;
    }

    .example-card:hover {
        transform: scale(1.03);
    }

    .example-card.selected {
        border: 3px solid #16a34a !important;
    }

    /* Buttons */
    .primary-btn button {
        background:#22c55e !important;
        color:white !important;
        font-weight:600 !important;
        border-radius:10px !important;
        height:50px !important;
        border:none !important;
    }
    .primary-btn button:hover {
        transform:scale(1.05);
    }

    .secondary-btn button {
        background:#e5e7eb !important;
        color:#333 !important;
        font-weight:600 !important;
        border-radius:10px !important;
        height:50px !important;
        border:none !important;
    }
    .secondary-btn button:hover {
        transform:scale(1.05);
    }

    .outline-btn button {
        background:white !important;
        border:1px solid #ccc !important;
        color:#333 !important;
        border-radius:10px !important;
        height:50px !important;
        font-weight:600 !important;
    }
    .outline-btn button:hover {
        transform:scale(1.05);
    }

    /* Result comparison boxes */
    .compare-box {
        background:#fafafa;
        padding:20px;
        border-radius:10px;
        font-size:16px;
        line-height:1.5;
        min-height:150px;
        border:1px solid #ddd;
        overflow-wrap:break-word;
        white-space:pre-wrap;
    }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
