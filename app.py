import os
import subprocess
from flask import Flask, request, send_file, Response

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/clean', methods=['POST'])
def clean_metadata():
    if 'video' not in request.files:
        return Response("Erro: Nenhum arquivo de vídeo enviado.", status=400)

    file = request.files['video']
    if file.filename == '':
        return Response("Erro: Nenhum arquivo selecionado.", status=400)

    # Salva o arquivo temporariamente
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(temp_path)

    # Roda o comando exiftool para limpar os metadados
    try:
        subprocess.run(
            ['exiftool', '-overwrite_original', '-all=', temp_path],
            check=True
        )
    except subprocess.CalledProcessError as e:
        return Response(f"Erro ao executar o exiftool: {e}", status=500)

    # Envia o arquivo limpo de volta e depois o remove
    return send_file(temp_path, as_attachment=True, download_name=file.filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
