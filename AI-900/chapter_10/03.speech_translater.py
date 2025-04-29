SUBSCRIPTION_KEY = "{SUBSCRIPTION_KEY}"
REGION = "{REGION}"

import azure.cognitiveservices.speech as speechsdk

def azure_speech_translator(subscription_key, region, from_language, to_language):
    """
    Translates speech from one language to another using Azure Cognitive Services.

    Args:
        subscription_key (str): Your Azure Speech service subscription key.
        region (str): The Azure region where your Speech service is hosted.
        from_language (str): The language of the input speech (e.g., 'ko-KR' for Korean).
        to_language (str): The target language for translation (e.g., 'en' for English).
    """
    # Create a speech translation configuration
    translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=subscription_key, region=region
    )

    # Set the source and target languages
    translation_config.speech_recognition_language = from_language
    translation_config.add_target_language(to_language)

    # Create a translation recognizer
    recognizer = speechsdk.translation.TranslationRecognizer(translation_config=translation_config)

    print("Speak into your microphone in Korean...")

    # Start speech translation
    result = recognizer.recognize_once()

    # Check the result
    if result.reason == speechsdk.ResultReason.TranslatedSpeech:
        print(f"Recognized (Korean): {result.text}")
        print(f"Translated (English): {result.translations[to_language]}")
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech translation canceled: {cancellation_details.reason}")
        if cancellation_details.error_details:
            print(f"Error details: {cancellation_details.error_details}")

# Example usage
if __name__ == "__main__":

    # Source and target languages
    from_language = "ko-KR"  # Korean
    to_language = "en"       # English

    azure_speech_translator(SUBSCRIPTION_KEY, REGION, from_language, to_language)