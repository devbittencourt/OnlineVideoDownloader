from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from pytube import YouTube
import os
import tempfile
import subprocess
import platform

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def open_downloads_folder():
    system = platform.system()
    if system == 'Windows':
        downloads_path = os.path.join(os.environ['USERPROFILE'], 'Downloads')
        subprocess.Popen(['explorer', downloads_path])
    elif system == 'Darwin':
        subprocess.Popen(['open', os.path.join(os.path.expanduser('~'), 'Downloads')])
    elif system == 'Linux':
        subprocess.Popen(['xdg-open', os.path.join(os.path.expanduser('~'), 'Downloads')])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        video_link = request.form['video_link']

        if video_link.startswith("https://"):
            try:
                yt = YouTube(video_link)
                video = yt.streams.get_highest_resolution()
                title = yt.title.replace('/', '_')  
                filename = f"{title}.mp4"

                temp_dir = tempfile.mkdtemp()
                filepath = os.path.join(temp_dir, filename)

                video.download(temp_dir)

                open_downloads_folder()

                return send_file(filepath, as_attachment=True)

            except Exception as e:
                flash(f"Error: {str(e)}", 'error')
                return redirect(url_for('index'))

        else:
            flash("The provided link is not valid. Please provide a valid link starting with 'https://'.", 'error')
            return redirect(url_for('index'))

    flash("Invalid method.", 'error')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
