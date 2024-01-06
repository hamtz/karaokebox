import os

from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session
from pytube import YouTube

app = Flask(__name__, static_folder='assets', template_folder='templates')
app.secret_key = '1'
ALLOWED_EXTENSIONS = {'mp4', 'mkv'}


def get_video_list():
    video_folder = 'listvideo'
    # video_folder = '/media/ilham/SONG' // ubah semua path sesuai path yg digunakan
    video_list = []
    for filename in os.listdir(video_folder):
        if filename.endswith('.mp4') or filename.endswith('.mkv'):
            video_list.append(filename)
    return video_list


def get_audio_list():
    audio_folder = 'listaudio'
    # audio_folder = '/media/ilham/SONG' // ubah semua path sesuai path yg digunakan
    audio_list = []
    for filename in os.listdir(audio_folder):
        if filename.endswith('.mp3') or filename.endswith('.wav'):
            audio_list.append(filename)
    return audio_list


@app.route('/')
def index():
    video_list = get_video_list()
    return render_template('index.html', video_list=video_list)


@app.route('/musik')
def musik():
    audio_list = get_audio_list()
    return render_template('indexaudio.html', audio_list=audio_list)


@app.route('/listmusic')
def listmusik():
    video_list = get_video_list()
    message = session.pop('message', '')  # Ambil pesan dari session (jika ada)
    return render_template('listmusik.html', video_list=video_list, message=message)


@app.route('/video/<filename>')
def video(filename):
    return send_from_directory('listvideo', filename)


@app.route('/audio/<filename>')
def audio(filename):
    return send_from_directory('listaudio', filename)


@app.route('/downloadmusic', methods=['GET', 'POST'])
def download():
    message = ""
    if request.method == 'POST':
        link = request.form['link']
        try:
            youtube_object = YouTube(link)
            youtube_stream = youtube_object.streams.get_by_resolution("360p")

            # Tentukan folder penyimpanan
            output_path = 'listvideo/'
            youtube_stream.download(output_path=output_path)

            message = "Download selesai"
        except:
            message = "An error has occurred"
    return render_template('download.html', message=message)


@app.route('/edit_video/<filename>', methods=['GET', 'POST'])
def edit_video(filename):
    # Jika metode adalah GET, tampilkan formulir pengubahan nama
    if request.method == 'GET':
        return render_template('edit_video.html', video_filename=filename)

    # Jika metode adalah POST, tangani permintaan pengubahan nama
    if request.method == 'POST':
        new_filename = request.form.get('new_filename')

        # Lakukan validasi nama file baru jika diperlukan

        # Ubah nama file
        try:
            old_path = os.path.join('listvideo', filename)
            new_path = os.path.join('listvideo', new_filename)
            os.rename(old_path, new_path)

            return redirect(url_for('listmusik'))
        except Exception as e:
            error_message = "Gagal mengubah nama file: " + str(e)
            return render_template('edit_video.html', video_filename=filename, error=error_message)


@app.route('/delete_video/<filename>')
def delete_video(filename):
    try:
        file_path = os.path.join('listvideo', filename)
        os.remove(file_path)
        message = "File berhasil dihapus"
    except Exception as e:
        message = "Gagal menghapus file: " + str(e)

    session['message'] = message  # Simpan pesan dalam session
    return redirect(url_for('listmusik'))


# Fungsi untuk memeriksa ekstensi file yang diterima
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    message = ""
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file and allowed_file(uploaded_file.filename):
            try:
                # Simpan file yang diunggah di folder "listvideo"
                uploaded_file.save('listvideo/' + uploaded_file.filename)
                message = "Upload Berhasil"
            except Exception as e:
                message = "Upload Gagal: " + str(e)
        else:
            message = "Upload Gagal: Format file tidak didukung"

    session['message'] = message  # Simpan pesan dalam session
    return redirect(url_for('listmusik'))


# @app.route('/video_list_json')
# def video_list_json():
#     video_list = get_video_list()
#     return jsonify(video_list)


if __name__ == '__main__':
    app.run(debug=True)
