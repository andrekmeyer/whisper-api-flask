elif 'file' in request.form:
    file_url = request.form['file']
    temp = NamedTemporaryFile(delete=False)
    try:
        with requests.get(file_url, stream=True) as r:
            r.raise_for_status()  # will throw if not 200
            with open(temp.name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    except Exception as e:
        print(f"Failed to fetch file from URL: {file_url}")
        print(str(e))
        abort(400, description="Could not download file from URL.")
