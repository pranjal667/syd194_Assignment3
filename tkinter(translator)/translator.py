from deep_translator import GoogleTranslator

class Translator:
    """This is the class for handling text translation."""

    @staticmethod
    def translate(text, target_language):
        """This function translates the given text to the specified target language."""
        try:
            translated_text = GoogleTranslator(source='auto', target=target_language).translate(text)
            return translated_text
        except Exception as e:
            raise Exception(f"Error during translation: {str(e)}")
