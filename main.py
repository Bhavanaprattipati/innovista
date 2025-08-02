
import streamlit as st
from utils.rewrite import rewrite_text
from utils.tts import generate_audio, get_speakers_and_languages
from utils.helpers import initialize_session, save_to_history, display_history
from utils.translate import translate_text


st.set_page_config(page_title="EchoVerse", layout="wide")
initialize_session()

st.title("🎙 EchoVerse – Generative AI Audiobook Creator")

# Input Section
st.header("📄 Input Text")
input_method = st.radio("Choose input method:", ["Paste Text", "Upload .txt File"])
if input_method == "Paste Text":
    original_text = st.text_area("Enter your content here", height=300, key="original_input")
else:
    uploaded_file = st.file_uploader("Upload a .txt file", type="txt")
    if uploaded_file:
        original_text = uploaded_file.read().decode("utf-8")
    else:
        original_text = ""

# Tone selection
tone = st.selectbox("🎭 Choose tone for rewriting", ["Neutral", "Suspenseful", "Inspiring", "Sarcastic"])

# Rewrite button
if st.button("✍ Rewrite Text") and original_text.strip():
    with st.spinner("Rewriting using FLAN-T5..."):
        rewritten_text = rewrite_text(original_text, tone)
        st.session_state["rewritten_text"] = rewritten_text
else:
    rewritten_text = st.session_state.get("rewritten_text", "")

# Side-by-side comparison after rewrite
if original_text.strip() and rewritten_text:
    st.markdown("### 🆚 Side-by-Side Comparison")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📥 Uploaded / Input Text")
        st.text_area("Original Text", original_text, height=300, key="display_original", disabled=True)

    with col2:
        st.subheader("📝 Rewritten Text")
        st.text_area("Rewritten Text", rewritten_text, height=300, key="display_rewritten", disabled=True)

# Audio generation
if rewritten_text:
    st.subheader("🔊 Audio Generation")
    speakers, languages = get_speakers_and_languages()
    speaker = st.selectbox("🧑‍🎤 Choose speaker", speakers)
    language = st.selectbox("🌍 Choose language", languages)

    if st.button("🎧 Generate Audio"):
        with st.spinner("Generating audio..."):
            audio_bytes = generate_audio(rewritten_text, speaker, language)
            st.audio(audio_bytes, format="audio/wav")
            st.download_button("⬇ Download Audio", audio_bytes, file_name="echoverse_narration.wav")
            save_to_history(original_text, rewritten_text, audio_bytes)

# History panel
display_history()
# -----------------------------------------------
# 🌐 Standalone Translation Tool (Separate Section)
# -----------------------------------------------
with st.expander("🌐 Text Translation Tool (Separate Utility)"):
    st.markdown("Use this section to translate text from one language to another without affecting the rewriting or audio generation workflow.")

    translation_input = st.text_area("Enter text to translate", height=200, key="separate_translate_input")

    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.text_input("Source Language Code (e.g., 'en')", value="en", key="separate_source_lang")
    with col2:
        lang_display = {
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Gujarati": "gu",
    "Marathi": "mr",
    "Bengali": "bn",
    "Punjabi": "pa",
    "Urdu": "ur"
    }

    selected_lang_name = st.selectbox("Target Language", list(lang_display.keys()), key="separate_target_lang")
    target_lang = lang_display[selected_lang_name]

    if st.button("🌍 Translate Text (Standalone Tool)", key="separate_translate_button"):
        if translation_input.strip():
            with st.spinner("Translating..."):
                try:
                    translated_output = translate_text(translation_input, source_lang, target_lang)
                    st.text_area("Translated Output", translated_output, height=200, disabled=True)
                except Exception as e:
                    st.error(f"⚠️ Translation failed: {e}")
        else:
            st.warning("Please enter text to translate.")

