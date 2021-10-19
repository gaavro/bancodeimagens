from flask import Flask, request, send_from_directory, jsonify
import os

allowed_ext = os.getenv('ALLOWED_EXTENSIONS')
max_size = os.getenv('MAX_CONTENT_LENGTH')
files_directory = os.getenv('FILES_DIRECTORY')
png_ext = os.getenv('PNG_EXT')
jpg_ext = os.getenv('JPG_EXT')
gif_ext = os.getenv('GIF_EXT')


def upload_item():
    file_name = str(request.files['file'].filename)
    file_ext = str(request.files['file'].filename).split(".")
    file_size = len(request.files['file'].read())
    if file_ext[1] not in allowed_ext:
        return {"message": "Formato não suportado"}, 415
    if file_size > 1 * 1000 * 1000:
        return {"message": "Tamanho não suportado"}, 413
    folder_file = os.listdir(f'./files_directory/{file_ext[1]}')
    if file_name in folder_file:
        return {"message": "Arquivo já existe"}, 409
        
    else:
        with open(f'./file', 'wb') as f:
            f.write(request.data)
            first_file = request.files['file']
            first_file.save(f'./files_directory/{file_ext[1]}/{file_name}')

    return {"message": f"Upload do arquivo {file_ext[0]}"},201


def list_files():
    files_png = os.listdir(f'{png_ext}')
    files_jpg = os.listdir(f'{jpg_ext}')
    files_gif = os.listdir(f'{gif_ext}')
    response = jsonify(files_png, files_jpg, files_gif)
    return response, 200


def list_by_type(ext):
    files = os.listdir(f'./files_directory/{ext}')
    return jsonify(files)


def download(file_name):
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
    if len(main_list)== 0:
        return {"msg": "Diretório está vazio"}, 404
    else:
        os.system(f'zip -r /tmp/{ext}-zip ./files_directory/{ext} -{ratio}')
    return send_from_directory(directory=f'/tmp', path=f'{ext}-zip.zip', as_attachment=True), 200