from flask import Flask, render_template_string, request, send_file, flash, redirect, url_for
from pytube import YouTube
import os
import tempfile
import subprocess
import platform

app = Flask(__name__)
app.secret_key = 'your_secret_key'

index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YT Video Downloader</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .form-container {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .form-container label {
            font-weight: bold;
        }
        .form-container input[type="text"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-sizing: border-box;
        }
        .form-container button {
            width: 100%;
            padding: 10px;
            background-color: #007bff;
            color: #ffffff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .form-container button:hover {
            background-color: #0056b3;
        }
        .error-message {
            color: red;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="form-container">
            <h1>YT Video Downloader</h1>
            <form action="{{ url_for('download') }}" method="post">
                <label for="video_link">Enter YT video link:</label><br>
                <input type="text" id="video_link" name="video_link" placeholder="Paste your video link here"><br>
                <button type="submit">Download Now</button>
            </form>
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="error-message">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
        </div>
    </div>
    <footer style="text-align: center; margin-top: 20px;">By DevBittencourt</footer>
</body>
</html>
"""

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
    return render_template_string(index_html)

@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        video_link = request.form['video_link']

        if video_link.startswith("https://"):
            try:
                yt = YouTube(video_link)
                video = yt.streams.get_highest_resolution()
                title = yt.title.replace('/', '_')  # Remove slashes from the title to avoid filename issues
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
