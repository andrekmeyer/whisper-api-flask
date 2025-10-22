from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return "Whisper app placeholder - upgrading instance."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets this env var
    app.run(host="0.0.0.0", port=port)
