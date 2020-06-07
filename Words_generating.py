import json

from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('yQZbr4qMQF7OwRyhGtS6ZuiNETJdFkz4cVchY1vAiKwv')
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)

speech_to_text.set_service_url('https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/06d9f170-f928-4ea8-a9d5-68080d178e40')

with open(join(dirname(__file__), './outputs/.', '0.mp3'),'rb') as audio_file:
    speech_recognition_results = speech_to_text.recognize(
        audio=audio_file,
        content_type='audio/mp3',
        model='ar-AR_BroadbandModel',
        word_alternatives_threshold=0.9,
    ).get_result()

test = speech_recognition_results
# print(test)

threshold = 0
word_length = len(test["results"])
for i in range(word_length):
    alt_length = len(test["results"][i]["word_alternatives"])
    for j in range(alt_length):
        if (test["results"][i]["word_alternatives"][j]["alternatives"][0]["confidence"] > threshold):
            print(test["results"][i]["word_alternatives"][j]["alternatives"][0]["word"], end=" ")
            print(test["results"][i]["word_alternatives"][j]["start_time"], end=" ")
            print(test["results"][i]["word_alternatives"][j]["end_time"])