SUBSCRIPTION_KEY = "AtXfS5OQhfotXiriCGovxGE9CihH43cewGpjujg9FVtr6Z0UApYRJQQJ99BDACYeBjFXJ3w3AAAEACOGTe7o"
REGION = "eastus"

import azure.cognitiveservices.speech as speechsdk

def azure_text_to_speech(text, subscription_key, region):
    """
    Converts text to speech using Azure Cognitive Services.

    Args:
        text (str): The text to convert to speech.
        subscription_key (str): Your Azure Speech service subscription key.
        region (str): The Azure region where your Speech service is hosted.
    """
    # Create a speech configuration
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)

    # Set the voice name (optional, can be customized)
    speech_config.speech_synthesis_voice_name = "ko-KR-SunHiNeural"

    # Create a speech synthesizer
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Synthesize the text to speech
    result = synthesizer.speak_text_async(text).get()

    # Check the result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesis succeeded.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.error_details:
            print(f"Error details: {cancellation_details.error_details}")

# Example usage
if __name__ == "__main__":
    # Replace with your Azure Speech service subscription key and region

    # Text to convert to speech
    text = "동해물과 백두산이 마르고 닳도록 하느님이 보우하사 우리나라 만세"

    azure_text_to_speech(text, SUBSCRIPTION_KEY, REGION)