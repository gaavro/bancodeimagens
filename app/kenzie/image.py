from flask import send_from_directory, jsonify, request
import os
from werkzeug.utils import secure_filename

max_size = os.getenv('MAX_CONTENT_LENGTH')
files_directory = os.getenv('FILES_DIRECTORY')
allowed_ext = os.getenv('ALLOWED_EXTENSIONS')

def download_file(file_name):
    ext = file_name[-3:]
    main_list = os.listdir(path=f'./files_directory/{ext}')
    if file_name not in main_list:
        return {"msg": "O arquivo não existe neste diretório"}, 404
    else:
        return send_from_directory(directory=f"../files_directory/{ext}", path=file_name, as_attachment=True), 200

def download_zip():
    ext = str(request.args.get('file_extension'))
    ratio = int(request.args.get('compression_ratio'))
    main_list = os.listdir(path=f'./files_directory/{ext}')
    if len(main_list) == 0:
        return {"alert": "Diretório vazio"}, 404
    else:
        os.system(f'zip -r /tmp/{ext}-zip ./files_directory/{ext} -{ratio}')
    return send_from_directory(directory='/tmp', path=f'{ext}-zip.zip', as_attachment=True), 200
def list_all_files():
    files_png = os.listdir(f'.{files_directory}/png')
    files_jpg = os.listdir(f'.{files_directory}/jpg')
    files_gif = os.listdir(f'.{files_directory}/gif')
    response = dict(png=files_png, jpg=files_jpg, gif=files_gif)
    return response, 200

def list_by_extension(extension):
    files = os.listdir(f'./files_directory/{extension}')
    return jsonify(files)

def upload_file():
    uploaded_file = request.files['file']
    file_name = secure_filename(uploaded_file.filename)
    file_ext = file_name.split(".")
    if file_ext[1] not in allowed_ext:
        return {"alert": "Formato não suportado"}, 415
    if file_name in os.listdir(f'./files_directory/{file_ext[1]}'):
        return {"alert": "Arquivo já existe na pasta"}, 409
    else:
        uploaded_file.save(os.path.join(f'./files_directory/{file_ext[1]}', file_name))
        return {"message": f"Upload de '{file_name}' concluído"}, 201