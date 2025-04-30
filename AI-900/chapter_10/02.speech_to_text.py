SUBSCRIPTION_KEY = "AtXfS5OQhfotXiriCGovxGE9CihH43cewGpjujg9FVtr6Z0UApYRJQQJ99BDACYeBjFXJ3w3AAAEACOGTe7o"
REGION = "eastus"

import azure.cognitiveservices.speech as speechsdk

def azure_speech_to_text(subscription_key, region):
    """
    Converts speech to text using Azure Cognitive Services.

    Args:
        subscription_key (str): Your Azure Speech service subscription key.
        region (str): The Azure region where your Speech service is hosted.
    """
    # Create a speech configuration
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)

    # Create a speech recognizer
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Speak into your microphone...")

    # Start speech recognition
    result = recognizer.recognize_once()

    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized: {result.text}")
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech recognition canceled: {cancellation_details.reason}")
        if cancellation_details.error_details:
            print(f"Error details: {cancellation_details.error_details}")

# Example usage
if __name__ == "__main__":
    # Replace with your Azure Speech service subscription key and region
    
    azure_speech_to_text(SUBSCRIPTION_KEY, REGION)