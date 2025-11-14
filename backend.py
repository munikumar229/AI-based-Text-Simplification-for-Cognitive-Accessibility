from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re
import stanza
import io
import subprocess
import tempfile
import os
from gtts import gTTS
from pydub import AudioSegment

# Lazy loading for translation
_tokenizer = None
_model = None

def _get_tokenizer():
    global _tokenizer
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-1.3B")
    return _tokenizer

def _get_model():
    global _model
    if _model is None:
        _model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-1.3B")
    return _model

class summarizer_TTS:
    def __init__(self, text, target_language='Telugu'):
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-1.3B")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-1.3B")
        self.text = text
        self.target_language = target_language

    def convert_indic_lang_to_english(self, indic_text, target_language_code='eng_Latn'):
        inputs = self.tokenizer(indic_text, return_tensors="pt")
        translated_tokens = self.model.generate(
            **inputs,
            forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(target_language_code))
        translated_text = self.tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        return translated_text

    def convert_english_to_indic_lang(self, english_text, target_language_code='tel_Telu'):
        inputs = self.tokenizer(english_text, return_tensors="pt")
        translated_tokens = self.model.generate(
            **inputs,
            forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(target_language_code))
        translated_text = self.tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        return translated_text

def convert_indic_lang_to_english(indic_text, target_language_code='eng_Latn'):
    tokenizer = _get_tokenizer()
    model = _get_model()
    inputs = tokenizer(indic_text, return_tensors="pt")
    translated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(target_language_code))
    translated_text = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
    return translated_text

def convert_english_to_indic_lang(english_text, target_language_code='tel_Telu'):
    tokenizer = _get_tokenizer()
    model = _get_model()
    inputs = tokenizer(english_text, return_tensors="pt")
    translated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(target_language_code))
    translated_text = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
    return translated_text

# If using a POS pipeline, set nlp to your Telugu tagger; else set nlp=None
nlp = stanza.Pipeline(lang='te', processors='tokenize,pos')  # Telugu POS tagger

TOOL_HINTS = ["పనిముట్టు", "సాధనం", "యాప్", "సాఫ్ట్‌వేర్"]
TELUGU = r"[\u0C00-\u0C7F]+"

def highlight_nouns_with_fallback(text):
    spans = []

    # POS-driven spans
    if nlp is not None:
        doc = nlp(text)
        for s in doc.sentences:
            for w in s.words:
                if w.upos in {"NOUN", "PROPN"} and w.start_char is not None and w.end_char is not None:
                    pre = text[w.start_char-1] if w.start_char > 0 else ""
                    post = text[w.end_char] if w.end_char < len(text) else ""
                    if pre in "'‘’" or post in "'‘’":
                        continue
                    spans.append((w.start_char, w.end_char))

    # Merge overlaps
    spans = sorted(set(spans))
    merged = []
    for s, e in spans:
        if not merged or s > merged[-1][1]:
            merged.append([s, e])
        else:
            merged[-1][1] = max(merged[-1][1], e)

    # Rebuild without quotes
    out, i = [], 0
    for s, e in merged:
        out.append(text[i:s]); out.append(text[s:e]); i = e
    out.append(text[i:])
    return "".join(out)

def simplify_text_with_nlp(text, target_language='tel_Telu', simplify_vocab=True, split_sentences=True, target_words=100):
    """
    Advanced text simplification that uses NLP functions:
    1. Identify key nouns first
    2. Create a summary that preserves these nouns
    3. Apply simplification and highlighting
    """
    if not text.strip():
        return ""

    # Detect if text is Telugu (contains Telugu characters)
    is_telugu = bool(re.search(TELUGU, text))

    # Step 1: Identify key nouns
    key_nouns = []
    if is_telugu and nlp is not None:
        doc = nlp(text)
        for sentence in doc.sentences:
            for word in sentence.words:
                if word.upos in {"NOUN", "PROPN"}:
                    key_nouns.append(word.text)

    # Step 2: Create summary that preserves key nouns
    if is_telugu:
        summarized_text = _create_noun_preserving_summary(text, key_nouns, target_words, is_telugu)
    else:
        summarized_text = _basic_summarize_text(text, target_words)

    # Step 3: Apply additional simplification
    simplified_text = _basic_simplify_text(summarized_text, simplify_vocab, split_sentences, target_words)

    # Step 4: Highlight nouns in the final text (only for Telugu)
    if is_telugu:
        final_text = highlight_nouns_with_fallback(simplified_text)
    else:
        final_text = simplified_text

    return final_text

def _create_noun_preserving_summary(text, key_nouns, target_words, is_telugu):
    """
    Create a summary that prioritizes sentences containing key nouns
    """
    if not key_nouns:
        return _basic_summarize_text(text, target_words)

    # Split into sentences
    if is_telugu:
        # For Telugu, split on common sentence endings
        sentences = re.split(r'[।\.\!\?]', text)
    else:
        sentences = re.split(r'[.!?]', text)

    sentences = [s.strip() for s in sentences if s.strip()]

    # Score sentences based on noun presence
    scored_sentences = []
    for sentence in sentences:
        score = 0
        for noun in key_nouns:
            if noun in sentence:
                score += 1
        scored_sentences.append((sentence, score))

    # Sort by score (highest first) and take top sentences
    scored_sentences.sort(key=lambda x: x[1], reverse=True)

    # Build summary with sentences containing nouns first
    summary_sentences = []
    word_count = 0

    for sentence, score in scored_sentences:
        if score > 0:  # Prioritize sentences with nouns
            sentence_words = len(sentence.split())
            if word_count + sentence_words <= target_words:
                summary_sentences.append(sentence)
                word_count += sentence_words
            else:
                # Take partial sentence if needed
                remaining_words = target_words - word_count
                if remaining_words > 0:
                    words = sentence.split()[:remaining_words]
                    summary_sentences.append(' '.join(words))
                break

    # If we don't have enough content, add more sentences
    if word_count < target_words * 0.7:  # Less than 70% of target
        for sentence, score in scored_sentences:
            if sentence not in summary_sentences:
                sentence_words = len(sentence.split())
                if word_count + sentence_words <= target_words:
                    summary_sentences.append(sentence)
                    word_count += sentence_words
                else:
                    break

    # Join sentences
    if is_telugu:
        summary = '। '.join(summary_sentences)
        if summary and not summary.endswith('।'):
            summary += '।'
    else:
        summary = '. '.join(summary_sentences)
        if summary and not summary.endswith('.'):
            summary += '.'

    return summary

def _basic_summarize_text(text, target_words):
    """
    Basic extractive summarization - take first part of text
    """
    words = text.split()
    if len(words) <= target_words:
        return text

    # Take first target_words words
    summary_words = words[:target_words]

    # Try to end at sentence boundary if possible
    summary = ' '.join(summary_words)
    last_sentence_end = max(summary.rfind('.'), summary.rfind('!'), summary.rfind('?'))
    if last_sentence_end > len(summary) * 0.5:  # If sentence end is in latter half
        summary = summary[:last_sentence_end + 1]

    return summary

def _basic_simplify_text(txt, simplify_vocab=True, split_sentences=True, target_words=100):
    """Basic text simplification logic"""
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

# def generate_tts_audio(text, lang='en', speed=1.0):
#     """
#     Generate TTS audio for the given text and language using gTTS.
#     Optionally adjust playback speed using pydub.
#     Returns a BytesIO object containing the audio data.
#     """
#     try:
#         tts = gTTS(text, lang=lang, slow=False)
#         audio_file = io.BytesIO()
#         tts.write_to_fp(audio_file)
#         audio_file.seek(0)

#         # If speed is not 1.0, adjust using pydub
#         if speed != 1.0:
#             # Load audio from BytesIO
#             audio = AudioSegment.from_mp3(audio_file)

#             # Adjust speed (pydub uses frame_rate for speed control)
#             # Higher frame_rate = faster playback, lower = slower
#             original_frame_rate = audio.frame_rate
#             new_frame_rate = int(original_frame_rate * speed)

#             # Apply speed change
#             audio = audio._spawn(audio.raw_data, overrides={
#                 'frame_rate': new_frame_rate
#             }).set_frame_rate(original_frame_rate)

#             # Export back to BytesIO
#             output_audio = io.BytesIO()
#             audio.export(output_audio, format='mp3')
#             output_audio.seek(0)
#             return output_audio

#         return audio_file
#     except Exception as e:
#         raise Exception(f"TTS generation failed: {e}")

def generate_tts_audio(text, lang='en', speed=1.0):
    """
    Generate TTS audio for the given text and language using gTTS.
    Optionally adjust playback speed using pydub.
    Returns a BytesIO object containing the audio data.
    """
    try:
        tts = gTTS(text, lang=lang, slow=False)
        audio_file = io.BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)

        # If speed is not 1.0, adjust using pydub
        if speed != 1.0:
            audio = AudioSegment.from_mp3(audio_file)
            original_frame_rate = audio.frame_rate
            new_frame_rate = int(original_frame_rate * speed)
            audio = audio._spawn(audio.raw_data, overrides={
                'frame_rate': new_frame_rate
            }).set_frame_rate(original_frame_rate)

            output_audio = io.BytesIO()
            audio.export(output_audio, format='mp3')
            output_audio.seek(0)
            return output_audio

        return audio_file
    except Exception as e:
        raise Exception(f"TTS generation failed: {e}")

