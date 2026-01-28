from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_video_info', methods=['POST'])
def get_info():
    url = request.form.get('url')
    if not url:
        return jsonify({"error": "URL is missing"}), 400

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # Sirf kaam ki info nikalna
            data = {
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "download_url": info.get('url'), # Direct video stream link
                "duration": info.get('duration_string')
            }
            return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
