from flask import Flask, request, jsonify, send_from_directory
from pytube import YouTube
from flask_cors import CORS
import os
import time

app = Flask(__name__)
CORS(app, resources={r"/download": {"origins": "*"}}, allow_headers="Content-Type")

# Configure the directory for storing downloaded videos
app.config['VIDEO_FOLDER'] = 'downloads'

@app.route("/download", methods=["POST"])
def download_video():
    try:
        video_url = request.json.get("videoUrl")
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        # return stream.download()
        start_time = time.time()
        downloaded_path = stream.download(output_path=app.config['VIDEO_FOLDER'])
        # Record the end time
        end_time = time.time()

        # Calculate the response time
        response_time = end_time - start_time
        # Generate a relative URL for the downloaded video
        video_filename = os.path.basename(downloaded_path)
        video_url = f"/videos/{video_filename}"
        return jsonify({"videoUrl": video_url, "responseTime": response_time})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/videos/<filename>')
def serve_video(filename):
    return send_from_directory(app.config['VIDEO_FOLDER'], filename)



if __name__ == "__main__":
    app.run(debug=True)