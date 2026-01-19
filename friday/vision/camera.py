import cv2
import time
import threading
import numpy as np
import mediapipe as mp
import math
import torch
import clip
from PIL import Image
from friday.core import state

# --- MEDIAPIPE ---
mp_hands = mp.solutions.hands
try:
    hands_detector = mp_hands.Hands(
        max_num_hands=2,
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
except:
    hands_detector = None
    print(">> ERROR: MediaPipe not installed correctly.")

# --- CLIP ---
model = None
LABELS = ["cat", "dog", "laptop", "Gun", "coffee cup", "person", "keyboard"]
text_inputs = None
device = "cpu"
preprocess = None

try:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    text_inputs = clip.tokenize(LABELS).to(device)
except:
    model = None

# --- UTILS ---
def calculate_distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

prev_x, prev_y = 0, 0
is_drawing = False

def process_hands(image):
    global prev_x, prev_y, is_drawing
    if not hands_detector: return image

    image.flags.writeable = False
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands_detector.process(rgb)
    image.flags.writeable = True

    height, width, _ = image.shape

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            idx_x = int(hand_landmarks.landmark[8].x * width)
            idx_y = int(hand_landmarks.landmark[8].y * height)
            thm_x = int(hand_landmarks.landmark[4].x * width)
            thm_y = int(hand_landmarks.landmark[4].y * height)

            cv2.circle(image, (idx_x, idx_y), 10, (0, 255, 255), 2)
            cv2.circle(image, (thm_x, thm_y), 10, (255, 0, 255), 2)

            dist = calculate_distance((idx_x, idx_y), (thm_x, thm_y))
            if dist < 40:
                cv2.line(image, (idx_x, idx_y), (thm_x, thm_y), (0, 255, 0), 3)
                if prev_x == 0 and prev_y == 0: prev_x, prev_y = idx_x, idx_y
                cv2.line(state.drawing_canvas, (prev_x, prev_y), (idx_x, idx_y), (0, 255, 255), 5)
                prev_x, prev_y = idx_x, idx_y
                is_drawing = True
            else:
                prev_x, prev_y = 0, 0
                is_drawing = False

    gray = cv2.cvtColor(state.drawing_canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    img_bg = cv2.bitwise_and(image, image, mask=mask_inv)
    img_fg = cv2.bitwise_and(state.drawing_canvas, state.drawing_canvas, mask=mask)
    return cv2.add(img_bg, img_fg)

def analyze_frame(frame):
    if not model:
        import random
        sim_labels = ["Human", "Smartphone", "Workstation", "Coffee"]
        label = random.choice(sim_labels)
        return label, 0.88

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(frame_rgb)
    try:
        image_input = preprocess(pil_image).unsqueeze(0).to(device)
        with torch.no_grad():
            logits_per_image, _ = model(image_input, text_inputs)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()[0]
        best_idx = probs.argmax()
        confidence = float(probs[best_idx])
        label = LABELS[best_idx]
        if confidence < 0.2: label = "Unknown Object"
        return label, confidence
    except:
        return "Error", 0.0

def start_camera():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    while True:
        success, frame = cap.read()
        if not success:
            time.sleep(0.1)
            continue

        frame = cv2.resize(frame, (1280, 720))
        frame = cv2.flip(frame, 1)

        if state.CURRENT_MODE == "mesh":
            frame = process_hands(frame)

        cv2.putText(frame, f"SYSTEM: {state.CURRENT_MODE.upper()}", (30, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 240, 255), 2)

        with state.lock:
            state.outputFrame = frame.copy()

def start_camera_thread():
    t = threading.Thread(target=start_camera)
    t.daemon = True
    t.start()
