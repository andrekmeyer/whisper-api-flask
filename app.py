import requests

@app.route('/whisper', methods=['POST'])
def handler():
    if 'file' in request.files:
        # Handle file uploads (as before)
        handle = request.files['file']
        temp = NamedTemporaryFile(delete=False)
        handle.save(temp.name)
    elif 'file' in request.form:
        # Handle external URL (Zoho case)
        file_url = request.form['file']
        temp = NamedTemporaryFile(delete=False)
        with requests.get(file_url, stream=True) as r:
            r.raise_for_status()
            with open(temp.name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    else:
        abort(400, description="No file provided.")

    # Transcribe
    result = model.transcribe(temp.name)
    return {'results': [{'filename': 'remote_file', 'transcript': result['text']}]}
