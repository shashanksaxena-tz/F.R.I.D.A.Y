from flask import Flask, render_template, Response, jsonify, request
import cv2
import numpy as np
import threading
from friday.core import state
from friday.vision import camera

app = Flask(__name__)

# Start Camera
camera.start_camera_thread()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    def gen():
        while True:
            with state.lock:
                if state.outputFrame is None: continue
                _, encoded = cv2.imencode(".jpg", state.outputFrame)
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + bytearray(encoded) + b'\r\n')
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/command', methods=['POST'])
def command_handler():
    data = request.json
    text = data.get('command', '').lower()

    response = {"action": "none", "speech": ""}

    # TODO: Replace with friday.core.brain logic
    if "google" in text:
        response["action"] = "open_window"
        response["url"] = "https://www.google.com"
        response["speech"] = "Accessing Google Database."

    elif "mesh" in text or "draw" in text or "start" in text:
        state.CURRENT_MODE = "mesh"
        response["action"] = "mode_switch"
        response["speech"] = "Creative mode active. Pinch fingers to draw."

    elif "clear" in text:
        state.drawing_canvas = np.zeros((720, 1280, 3), dtype=np.uint8)
        response["speech"] = "Canvas wiped."

    elif "normal" in text or "stop" in text:
        state.CURRENT_MODE = "normal"
        response["action"] = "mode_switch"
        response["speech"] = "Disengaging UI."
    elif "structure" in text or "benzene" in text:
        response["action"] = "open_window"
        response["url"] = "https://app.molview.com/"
        response["speech"] = "this is a 3d structure of benzene"

    elif "scan" in text or "analyze" in text or "friday" in text:
        response["action"] = "scan"
        response["speech"] = "Scanning environment."

    elif "news" in text:
        # Placeholder for integration
        from friday.integrations.news import NewsIntegration
        news = NewsIntegration()
        headlines = news.execute()
        response["speech"] = f"Here are the top headlines: {headlines}"

    return jsonify(response)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    with state.lock:
        if state.outputFrame is None:
            return jsonify({"ui_text": "VIDEO LOSS", "speech_text": "Camera offline.", "is_threat": False})
        frame = state.outputFrame.copy()

    label, confidence = camera.analyze_frame(frame)

    return jsonify({
        "ui_text": f"DETECTED: {label.upper()}",
        "speech_text": f"I see a {label} sir.",
        "confidence": int(confidence * 100),
        "is_threat": (label == "Gun")
    })

def run():
    app.run(host='0.0.0.0', port=5000)
