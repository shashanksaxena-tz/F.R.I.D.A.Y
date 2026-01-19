# Architecture Overview

## Goal
Transform the monolithic `friday/app.py` into a modular, extensible "Jarvis-like" system capable of handling voice commands, vision tasks, LLM processing, and external integrations.

## New Structure

```
friday/
├── __init__.py
├── main.py              # Entry point
├── core/                # The Brain & Configuration
│   ├── brain.py         # LLM Interface (OpenAI/Local)
│   ├── config.py        # Settings management
│   └── state.py         # Context/State management
├── vision/              # Eyes
│   ├── camera.py        # Video capture & Threading
│   ├── gestures.py      # Hand tracking logic
│   └── scanning.py      # 3D scanning logic
├── integrations/        # Hands & Tools
│   ├── base.py          # Abstract Integration Class
│   ├── gmail.py
│   ├── outlook.py
│   ├── news.py
│   └── ...
└── web/                 # Face (UI)
    ├── server.py        # Flask App
    └── templates/
        └── index.html
```

## Data Flow
1. **Input**:
    - **Vision**: Camera -> `vision.camera` -> `vision.gestures` -> `state`.
    - **Voice**: Browser -> `web.server` (`/api/command`) -> `core.brain`.
2. **Processing**:
    - `core.brain` analyzes text command + current visual context.
    - Decides Action: "Search Google", "Fetch Emails", "Rotate 3D Model".
3. **Execution**:
    - `core.brain` calls `integrations.gmail.fetch_emails()` or updates `state`.
4. **Output**:
    - Response sent back to Browser (JSON).
    - TTS (Browser) speaks response.
    - HUD updates (Javascript).
