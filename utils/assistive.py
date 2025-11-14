"""
utils/assistive.py

Contains all functions for assistive text rendering:
- Grapheme-safe bolding of first N characters
- Telugu character assist highlighting
- English/Telugu vowel bolding
- Optional letter coloring mode
- Safe HTML rendering with regex (unicode-aware)

All functions return HTML strings safe for st.markdown(..., unsafe_allow_html=True)
"""

import regex   # safer unicode support than re

# Telugu assistive character map
TELUGU_ASSIST_CLASSES = {
    "అ": "df-ta", 
    "ఆ": "df-taa", 
    "ఇ": "df-ti", 
    "ఈ": "df-ti", 
    "ఉ": "df-tu", 
    "ఊ": "df-tu",
    "వ": "df-tva"
}


def apply_letter_coloring(text: str) -> str:
    """
    Colors each unique English letter with a unique color.
    Does NOT nest tags incorrectly (safe).
    """
    colors = [
        "red", "blue", "green", "orange", "purple",
        "brown", "pink", "gray", "olive", "cyan",
        "magenta", "lime", "teal", "navy", "maroon",
        "silver", "gold", "indigo", "violet", "turquoise"
    ]

    color_map = {}
    color_index = 0

    def replacer(match):
        nonlocal color_index
        ch = match.group(0)
        if ch not in color_map:
            color_map[ch] = colors[color_index % len(colors)]
            color_index += 1
        return f'<span style="color:{color_map[ch]}">{ch}</span>'

    return regex.sub(r'([A-Za-z])', replacer, text)


def apply_bold_vowels(text: str, lang: str) -> str:
    """
    Bolds vowels depending on language.
    Telugu vowel set differs from English.
    """
    if lang == "తెలుగు":
        pattern = r"([అఆఇఈఉఊఋౠఎఏఐఒఓఔ])"
    else:
        pattern = r"([AEIOUaeiou])"

    return regex.sub(pattern, r"<b>\1</b>", text)


def apply_reading_assist(text: str, lang: str, bold_first_n: int = 2, char_assist: bool = True) -> str:
    """
    Bold the first N graphemes (not characters!), and apply telugu character assist spans.
    """
    words = text.split()
    processed = []

    for word in words:
        graphemes = regex.findall(r"\X", word)

        if not graphemes:
            processed.append(word)
            continue

        head = "".join(graphemes[:bold_first_n])
        tail = "".join(graphemes[bold_first_n:])

        assisted_word = f"<b>{head}</b>{tail}"

        # Telugu-only character assist
        if lang == "తెలుగు" and char_assist:
            for char, cls in TELUGU_ASSIST_CLASSES.items():
                assisted_word = assisted_word.replace(char, f'<span class="{cls}">{char}</span>')

        processed.append(assisted_word)

    return " ".join(processed)


def apply_all_assists(
    text: str,
    lang: str,
    assist_on: bool,
    bold_first_n: int,
    char_assist: bool,
    bold_letters: bool,
    color_letters: bool
) -> str:
    """
    Central function that applies all assistive transformations in safe order.
    """
    output = text

    # Step 1 — bold vowels (optional)
    if bold_letters:
        output = apply_bold_vowels(output, lang)

    # Step 2 — color letters (optional)
    if color_letters and lang != "తెలుగు":
        output = apply_letter_coloring(output)

    # Step 3 — reading assist (bold first N graphemes + Telugu assist spans)
    if assist_on:
        output = apply_reading_assist(output, lang, bold_first_n, char_assist)

    return output
