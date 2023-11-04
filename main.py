import os

from flask import Flask, render_template, send_from_directory, request, redirect, url_for
from pytube import YouTube

app = Flask(__name__, static_folder='assets', template_folder='templates')

def get_video_list():
    video_folder = 'listvideo'
    video_list = []
    for filename in os.listdir(video_folder):
        if filename.endswith('.mp4') or filename.endswith('.mkv'):
            video_list.append(filename)
    return video_list



# def get_video_list():
#     video_folder = 'listvideo'
#     video_list = []
#     for filename in os.listdir(video_folder):
#         if filename.endswith('.mp4') or filename.endswith('.mkv'):
#             # Hapus ekstensi file
#             video_name = os.path.splitext(filename)[0]
#             video_list.append(video_name)
#     return video_list



@app.route('/')
def index():
    video_list = get_video_list()
    return render_template('index.html', video_list=video_list)



@app.route('/listmusic')
def listmusik():
    video_list = get_video_list()
    return render_template('listmusik.html', video_list=video_list)


# @app.route('/downloadmusic')
# def downloadmusik():
#     video_list = get_video_list()
#     return render_template('download.html', video_list=video_list)


@app.route('/video/<filename>')
def video(filename):
    return send_from_directory('listvideo', filename)


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

            message = "Download is completed successfully"
        except:
            message = "An error has occurred"
    return render_template('download.html', message=message)


# @app.route('/video_list_json')
# def video_list_json():
#     video_list = get_video_list()
#     return jsonify(video_list)


if __name__ == '__main__':
    app.run(debug=True)
