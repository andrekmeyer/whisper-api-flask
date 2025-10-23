from flask import Flask, request, jsonify, abort
import requests
from tempfile import NamedTemporaryFile
import os

app = Flask(__name__)

@app.route('/whisper', methods=['POST'])
def transcribe():
    # Case 1: File uploaded directly
    if 'file' in request.files:
        audio_file = request.files['file']
        # Simulate processing the uploaded file
        print(f"Received uploaded file: {audio_file.filename}")
        return jsonify({
            "results": [
                {
                    "filename": audio_file.filename,
                    "transcript": "uploaded file test"
                }
            ]
        })

    # Case 2: File provided as a remote URL
    elif 'file' in request.form:
        file_url = request.form['file']
        print(f"Received remote file URL: {file_url}")
        
        # Create a temporary file to store the download
        temp = NamedTemporaryFile(delete=False)
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            with requests.get(file_url, stream=True, headers=headers, timeout=10) as r:
                r.raise_for_status()
                with open(temp.name, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            print("File downloaded successfully.")
            return jsonify({
                "results": [
                    {
                        "filename": "remote file",
                        "transcript": "remote URL test"
                    }
                ]
            })

        except Exception as e:
            import traceback
            print(f"[ERROR] Failed to fetch file from URL: {file_url}")
            traceback.print_exc()
            abort(400, description="Could not download file from URL.")

        finally:
            # Clean up the temporary file
            if os.path.exists(temp.name):
                os.remove(temp.name)

    # Case 3: Neither file nor URL provided
    else:
        print("No valid 'file' field in request.")
        abort(400, description="No file provided.")


# Ensure it works when deployed (important for Render)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
