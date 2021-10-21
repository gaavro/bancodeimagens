from flask import Flask
from .kenzie import set_directories
from .kenzie.image import list_by_extension, list_all_files, download_zip, download_file, upload_file

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1*1000*1000

set_directories()

@app.get('/download/<file_name>')
def download(file_name):
    return download_file(file_name)

@app.get('/download-zip')
def download_dir_as_zip():
    return download_zip()

@app.get('/files')
def list_files():
    return list_all_files()

@app.get('/files/<extension>')
def list_files_by_extension(extension):
    return list_by_extension(extension)
    
@app.post('/upload')
def upload():
    return upload_file()