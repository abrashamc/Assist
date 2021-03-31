import pyaudio
import wave
import speech_recognition
from commands import Commander


running = True


def play_audio(filename):
    """
    Plays audio file.
    :param filename: path to audio file in wav format
    """
    chunk = 1024
    wav_file = wave.open(filename, 'rb')
    py_audio = pyaudio.PyAudio()

    stream = py_audio.open(
        format=py_audio.get_format_from_width(wav_file.getsampwidth()),
        channels=wav_file.getnchannels(),
        rate=wav_file.getframerate(),
        output=True
    )

    data_stream = wav_file.readframes(chunk)

    while data_stream:
        stream.write(data_stream)
        data_stream = wav_file.readframes(chunk)

    stream.close()
    py_audio.terminate()


recognizer = speech_recognition.Recognizer()
cmd = Commander()


def init_speech():
    """
    Starts listening for audio through sound input device.
    Audio is then converted to text using google speech-to-text API.
    Response is sent as audio.
    """

    play_audio("audio/recording_start.wav")

    with speech_recognition.Microphone() as source:
        print("Speak now:")
        audio = recognizer.listen(source)

    play_audio("audio/recording_end.wav")

    command = ""

    try:
        command = recognizer.recognize_google(audio)
    except Exception as e:
        print("Couldn't understand you!\n", e)

    print("Your command: " + command)
    if command in ["quit", "exit", "bye", "goodbye", "stop"]:
        global running
        running = False
    else:
        cmd.discover(command)


if __name__ == '__main__':
    while running:
        init_speech()
