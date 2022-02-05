import sounddevice as sd
import soundfile as sf
import io
import requests
import base64
import os
import time

duration = 7.0
fs = 48000
mainworker_url = os.environ['MAINWORKER_URL']
sd.default.samplerate = fs
TIME_SLEEP_SECONDS = 10


def step():
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2, blocking=True, device=7)
    rawbytes = io.BytesIO()
    sf.write(rawbytes, myrecording, samplerate=fs, format="FLAC")
    rawbytes.seek(0)

    audio = base64.b64encode(rawbytes.getvalue()).decode()
    response = requests.post(mainworker_url, json={'codec': 'FLAC', 'audio': audio})
    print(response.content)


if __name__ == '__main__':
    while True:
        time.sleep(TIME_SLEEP_SECONDS)
        step()
