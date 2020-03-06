"""Creates VoiceText class"""
import json
import subprocess
# Disable linting error that package is not found locally
# pylint: disable=E0401
import speech_recognition as sr


class VoiceText:
    """ Handles all the functionality regarding voice to text methods """
    def __init__(self):
        with open("config.json", "r") as file:
            data = json.load(file)
        self.mic_name = data["microphone"]

    def get_device(self):
        """ Finds microphone device ID by looking for the name of the microphone """
        for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
            if microphone_name == self.mic_name:
                device_id = i
                return device_id
        return False

    def voice_to_text(self):
        """ This function converts all audio with Google Speech Recognition into text """
        microphone_device = self.get_device()
        if microphone_device is not None:
            repeat = True
            while repeat:
                recogniser = sr.Recognizer()
                with sr.Microphone(device_index=microphone_device) as source:
                    subprocess.run("clear")
                    recogniser.adjust_for_ambient_noise(source)
                    print("Please say the book details to the microphone.")
                    try:
                        audio = recogniser.listen(source, timeout=1.5)
                    except sr.WaitTimeoutError:
                        print("Listening timed out whilst waiting for phrase to start")
                        quit()
                try:
                    print(
                        "Google Speech Recognition thinks you said '{}'".format(
                            recogniser.recognize_google(audio)
                        )
                    )
                    text = input("Is the speech to text correct? (yes/no): ")
                    while True:
                        if text == "yes":
                            repeat = False
                            return recogniser.recognize_google(audio)
                        if text == "no":
                            print("Sorry about that, we will repeat the process again.")
                            break
                        else:
                            print("Wrong input!")
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as error:
                    print(
                        "Could not request results from Google Speech Recognition service; {0}"
                        .format(error)
                    )
        return False
