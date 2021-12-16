#!/usr/bin/env python3
"""Handle ingress requests
"""

import os
from run_command import run_command
from flask import Flask, request, send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.relpath('/tmp')

#def main():
    #app.run(port=5000)

#def copy_file_to_remote(f, location, password):
    #"""Copy file to the remote location specified

    #TODO: WIP
    #:param str f: file to copy
    #:param str location: URL of the server
    #:param str password: password to the server
    #"""
    #cmd =
    #return_code, stdout, stderr = run_command(cmd, timeout=1800)

@app.route('/')
def home():
    return 'This is home page'

@app.route('/upload', methods=['POST'])
def handleFileUpload():
    """Handle file upload

    Note: https://zetcode.com/python/requests/
    TODO: add werkzeug.utils.secure_filename() method
    """

    msg = 'failed to upload presentation'

    print(request)
    print(request.files)
    if 'file' in request.files:

        f = request.files['file']

        if f.filename != '':
            input_file = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            f.save(input_file)
            msg = 'presentation uploaded successfully'

            os.environ["AVG_INPUT"] = input_file # TODO: include timestamp in the filename
            os.environ["AVG_OUTPUT"] = os.path.splitext(input_file)[0] + ".mp4"
            return_code, stdout, stderr = run_command(["/opt/pptx2ari.sh"])

            if return_code != 0:
                raise RuntimeError('pptx2ari failed')
            # TODO: provide result

            #return_code, stdout, stderr = run_command(cmd, timeout=1800)

    return msg

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)

if __name__ == '__main__':
    main()
