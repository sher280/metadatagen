from flask import Flask, request, render_template, redirect, url_for
from metadata.text_extractor import extract_text
from metadata.llm_generator import generate_metadata
import os
import dotenv

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['OPENROUTER_API_KEY'] = os.getenv('OPENROUTER_API_KEY', 'your_api_key_here')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            text = extract_text(filepath)
            metadata = generate_metadata(text, app.config['OPENROUTER_API_KEY'])
            return render_template('result.html', metadata=metadata)
    return render_template('upload.html')

if __name__ == '__main__':
    print(f"Starting server with API key: {app.config['OPENROUTER_API_KEY']}")
    app.run(debug=True)
