from flask import Flask, request, jsonify, abort
import requests
from tempfile import NamedTemporaryFile

app = Flask(__name__)

@app.route('/whisper', methods=['POST'])
def transcribe():
    if 'file' in request.files:
        audio_file = request.files['file']
        # Process uploaded file
        return jsonify({"results": [{"filename": "file", "transcript": "uploaded file test"}]})
    
    elif 'file' in request.form:
        file_url = request.form['file']
        temp = NamedTemporaryFile(delete=False)
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0'
            }
            with requests.get(file_url, stream=True, headers=headers) as r:
                r.raise_for_status()
                with open(temp.name, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            # Simulate successful transcription
            return jsonify({"results": [{"filename": "remote file", "transcript": "remote URL test"}]})
        
        except Exception as e:
            import traceback
            print(f"Failed to fetch file from URL: {file_url}")
            traceback.print_exc()
            abort(400, description="Could not download file from URL.")
    
    else:
        abort(400, description="No file provided.")

if __name__ == "__main__":
    app.run()
