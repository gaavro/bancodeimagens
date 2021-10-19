from flask import Flask
import os
from kenzie import make_directory
from kenzie.image import download, download_zip, list_by_type, list_files, upload_item


app = Flask(__name__)


make_directory()


@app.post('/upload')
def upload():
    return upload_item()


@app.get('/files')
def files():
    return list_files()


@app.get('/files/<ext>')
def list_files_by_extension():
    return list_by_type()


@app.get('/download/<file_name>')
def download_file_name(file_name):
    return download(file_name)


@app.get('/download-zip')
def download_dir_as_zip():
    return download_zip()