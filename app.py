from flask import Flask, request, send_file
import requests
import base64
import os
import io

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>🎬 Sarvam AI Voice-over</h1>

    <form method="POST" action="/generate">
        <textarea name="text" rows="10" cols="60"
        placeholder="Apni video script yahan paste karo..."></textarea>
        <br><br>

        <select name="language">
            <option value="hi-IN">Hindi</option>
            <option value="od-IN">Odia</option>
            <option value="en-IN">English</option>
        </select>

        <br><br>
        <button type="submit">🔊 Generate Voice</button>
    </form>
    """

@app.route("/generate", methods=["POST"])
def generate():
    text = request.form.get("text", "").strip()
    language = request.form.get("language", "hi-IN")

    if not text:
        return "Script empty hai.", 400

    api_key = os.environ.get("SARVAM_API_KEY")

    if not api_key:
        return "SARVAM_API_KEY missing hai.", 500

    url = "https://api.sarvam.ai/text-to-speech"

    payload = {
        "text": text,
        "target_language_code": language,
        "speaker": "shubh",
        "model": "bulbul:v3"
    }

    headers = {
        "api-subscription-key": api_key,
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=120
    )

    if response.status_code != 200:
        return f"Sarvam API Error: {response.text}", 500

    data = response.json()
    audio_base64 = data["audios"][0]
    audio_bytes = base64.b64decode(audio_base64)

    return send_file(
        io.BytesIO(audio_bytes),
        mimetype="audio/wav",
        as_attachment=True,
        download_name="voiceover.wav"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
