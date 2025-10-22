from flask import Flask, abort, request
from flask_cors import CORS
from tempfile import NamedTemporaryFile
import whisper
import torch
import os

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base", device=DEVICE)

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Whisper Transcriber is Live!"

@app.route("/whisper", methods=["POST"])
def handler():
    if not request.files:
        abort(400)
    results = []
    for filename, handle in request.files.items():
        temp = NamedTemporaryFile()
        handle.save(temp)
        result = model.transcribe(temp.name)
        results.append({'filename': filename, 'transcript': result['text']})
    return {'results': results}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
