from flask import Flask, render_template, request
import pyttsx3
import os

app = Flask(__name__,template_folder='somethingnew')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get user inputs from the form
        speaker = request.form['speaker']
        text_input = request.form['text_input']

        # Generate audio file
        audio_file = generate_audio(speaker, text_input)

        # Render the template with the audio player
        return render_template('player.html', audio_file=audio_file)

    return render_template('index.html')


def generate_audio(speaker, text_input):
    # Initialize text-to-speech engine
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Adjust speech rate if needed

    # Set the speaker voice
    voices = engine.getProperty('voices')
    for voice in voices:
        if voice.name == speaker:
            engine.setProperty('voice', voice.id)
            break

    # Generate audio file
    output_file = 'static/generated_audio.mp3'
    engine.save_to_file(text_input, output_file)
    engine.runAndWait()

    return output_file


if __name__ == '__main__':
    app.run(debug=True)
