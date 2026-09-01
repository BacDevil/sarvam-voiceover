from flask import Flask, request, send_file
from sarvamai import SarvamAI
import base64
import os

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>🎬 Sarvam AI Voice-over</h1>
    <form method="POST" action="/generate">
        <textarea name="text" rows="10" cols="50"
        placeholder="Apni script yahan paste karo..."></textarea><br><br>

        <select name="language">
            <option value="hi-IN">Hindi</option>
            <option value="od-IN">Odia</option>
            <option value="en-IN">English</option>
        </select><br><br>

        <button type="submit">🔊 Generate Voice</button>
    </form>
    """

@app.route("/generate", methods=["POST"])
def generate():
    text = request.form["text"]
    language = request.form["language"]

    client = SarvamAI(
        api_subscription_key=os.environ["SARVAM_API_KEY"]
    )

    response = client.text_to_speech.convert(
        model="bulbul:v3",
        text=text,
        target_language_code=language,
        speaker="shubh"
    )

    audio = response.audios[0]

    with open("/tmp/voiceover.wav", "wb") as f:
        f.write(base64.b64decode(audio))

    return send_file(
        "/tmp/voiceover.wav",
        as_attachment=True,
        download_name="voiceover.wav"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
