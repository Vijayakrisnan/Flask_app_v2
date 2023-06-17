from flask import Flask, render_template, request
import sqlite3
import time

app = Flask(__name__, template_folder='template')

# Set up SQLite database
conn = sqlite3.connect('audio_db.sqlite',check_same_thread=False)
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS audios
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              speaker TEXT,
              text_input TEXT,
              audio_file TEXT)''')
conn.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get user inputs from the form
        speaker = request.form['speaker']
        text_input = request.form['text_input']
        #audio_file = f"{speaker.replace(' ', '_')}.mp3"

        # Insert the data into the database
        c.execute("INSERT INTO audios (speaker, text_input) VALUES (?, ?)",
                  (speaker, text_input))
        conn.commit()

        # Render the template with the audio player
        return render_template('player.html')
    # Fetch existing speakers from the database
    c.execute("SELECT DISTINCT speaker FROM audios")
    speakers = [row[0] for row in c.fetchall()]

    return render_template('gptindex.html', speakers=speakers)


if __name__ == '__main__':
    app.run(debug=True)
