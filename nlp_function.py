import requests
from google.cloud.speech_v1 import SpeechClient
from google.cloud import speech
from google.cloud import language_v1
import os


def hello_world(request):
    sideworker_url = os.getenv("SIDEWORKER_URL", None)
    if sideworker_url is None:
        raise ValueError("Sideworker URL is none")

    # step 1
    # get audio -> sent to speech2text
    request_json = request.get_json()
    audio = request_json['audio']
    codec = request_json['codec']
    codec = speech.RecognitionConfig.AudioEncoding.FLAC if codec == 'FLAC' else speech.RecognitionConfig.AudioEncoding.LINEAR16

    config = speech.RecognitionConfig(
        encoding=codec,
        sample_rate_hertz=48000,
        language_code="en-US",
        enable_separate_recognition_per_channel=False,
        audio_channel_count=2,
        model="video"
    )

    audio = speech.RecognitionAudio(content=audio)

    client = SpeechClient()
    result = client.recognize(config=config, audio=audio)
    phrase = ' '.join(x.alternatives[0].transcript for x in result.results)

    # step 2
    # get s2t answer -> send to GCP NLP
    # Instantiates a client
    client = language_v1.LanguageServiceClient()

    # The text to analyze
    document = language_v1.Document(content=phrase, type_=language_v1.Document.Type.PLAIN_TEXT)
    encoding_type = language_v1.EncodingType.UTF8
    response = client.analyze_entities(document=document, encoding_type=encoding_type)
    entities = sorted([(x.name, x.salience) for x in response.entities], key=lambda x: x[1], reverse=True)

    # entities could be of 2 and more words, so combine them and split by spaces and take first 2 words
    entities = (' '.join(x[0] for x in entities)).split(' ')[:2]
    search_phrase = ' '.join(entities)

    # step 3
    # get NLP answer -> send to sideworker
    response = requests.post(sideworker_url, json={'search_phrase': search_phrase, 'full_phrase': phrase})
    return response.text
