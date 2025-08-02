from deep_translator import GoogleTranslator

def translate_text(text: str, source_lang="en", target_lang="te"):
    try:
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        return translated
    except Exception as e:
        raise RuntimeError(f"Translation error: {e}")
