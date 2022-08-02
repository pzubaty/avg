#!/usr/bin/env python3
"""Handle ingress requests
"""

import os

from pathlib import Path
from flask import Flask, request, render_template, send_file, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.relpath('/var/www/html')  # /tmp
Path(app.config['UPLOAD_FOLDER'] + '/pptx').mkdir(parents=True, exist_ok=True)

# TODO: empty spaces, pptx, current status...

def get_files(main_dir):
    p = Path(main_dir)
    for item in sorted(p.glob('**/*.*')):
        if item.is_file():
            yield str(item.resolve())

@app.route('/')
def index():
    files = get_files(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', **locals())

@app.route('/upload', methods=['GET', 'POST'])
def handleFileUpload():
    """Handle file upload

    Note: https://zetcode.com/python/requests/
    """
    msg = 'failed to upload presentation'
    print(request)

    if request.method == 'POST':
        f = request.files['file']
        if f.filename != '' and f.filename.split('.')[-1] == 'pptx':
            upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], "pptx")
            input_file = os.path.join(upload_dir, f.filename)
            f.save(input_file)

            msg = (f'Presentation {f.filename} uploaded successfully. '
                   f'It will be converted to video.')
    return msg

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    #full_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    #return send_from_directory(full_path, filename)
    print(f"/{filename}")
    return send_file(os.path.relpath(f"/{filename}"), as_attachment=True)

if __name__ == '__main__':
    main()
