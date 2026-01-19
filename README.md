# F.R.I.D.A.Y. - AI Assistant

This project is a web-based AI assistant interface inspired by Iron Man's F.R.I.D.A.Y. It combines computer vision, voice interaction, and a futuristic UI to create an interactive experience.

## Capabilities

The current system supports the following features:

### 1. Interactive Interface
- **Futuristic HUD**: A sci-fi inspired user interface with animations, statistics (CPU/Memory simulation), and logs.
- **Voice Visualization**: An "Arc Reactor" style visualizer that reacts when the system speaks.

### 2. Voice Interaction
- **Voice Commands**: Uses the Web Speech API to listen to user commands.
- **Speech Synthesis**: Responds to the user using the browser's text-to-speech engine.
- **Supported Commands**:
  - "Google": Opens Google in a new window.
  - "Mesh" / "Draw" / "Start": Activates the hand gesture drawing mode.
  - "Normal" / "Stop": Returns to normal video mode.
  - "Clear": Clears the drawing canvas.
  - "Structure" / "Benzene": Opens a 3D molecule viewer (MolView).
  - "Scan" / "Analyze": Triggers object recognition on the current video frame.

### 3. Computer Vision (Backend)
- **Video Streaming**: Streams live video from the webcam to the web interface.
- **Hand Gesture Recognition**: Uses MediaPipe to detect hands.
  - **Drawing Mode**: Pinching index and thumb allows drawing on the screen.
- **Object Recognition**: Uses OpenAI's CLIP model (if available) to classify objects in the video feed and determine if they are potential "threats".

## Installation & Usage

### Prerequisites
- Python 3.7+
- A webcam

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python friday/app.py
```

Access the interface at `http://127.0.0.1:5000`.

**Note:** For voice recognition to work, you must use a browser that supports the Web Speech API (e.g., Google Chrome).

## Potential Extensions

This project can be significantly expanded. Here are some ideas:

### 1. Enhanced Computer Vision
- **Face Recognition**: Identify specific users and customize the experience.
- **Emotion Detection**: Analyze facial expressions to detect mood.
- **Body Pose Estimation**: Track full-body movements for fitness apps or advanced gesture control.

### 2. Smarter AI Integration
- **LLM Integration**: Connect to Large Language Models (like GPT-4, Claude, or local Llama) to enable natural, conversational interactions instead of simple keyword-based commands.
- **Context Awareness**: Allow the system to remember previous interactions.

### 3. IoT & Home Automation
- **Smart Home Control**: Integrate with Home Assistant or other IoT platforms to control lights, temperature, and devices via voice or gestures.

### 4. Productivity Tools
- **Personal Assistant Features**: Add capabilities to manage calendars, set reminders, and take notes.
- **Real-time Data Visualization**: Fetch and display weather, stocks, or news in the HUD.

### 5. Advanced UI/UX
- **3D Rendering**: Use libraries like Three.js to render 3D models directly in the HUD instead of opening external websites.
- **Customizable Layouts**: Allow users to configure the HUD elements.
