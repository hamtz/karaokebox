import os
from flask import Flask, render_template, send_from_directory, jsonify

app = Flask(__name__, static_folder='assets', template_folder='templates')

def get_video_list():
    video_folder = 'listvideo'
    video_list = []
    for filename in os.listdir(video_folder):
        if filename.endswith('.mp4') or filename.endswith('.mkv'):
            video_list.append(filename)
    return video_list


@app.route('/')
def index():
    video_list = get_video_list()
    return render_template('index.html', video_list=video_list)


@app.route('/video/<filename>')
def video(filename):
    return send_from_directory('listvideo', filename)


@app.route('/video_list_json')
def video_list_json():
    video_list = get_video_list()
    return jsonify(video_list)


if __name__ == '__main__':
    app.run(debug=True)
