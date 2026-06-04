# AI-Drone-system

## Installation

Install runtime dependencies with:

```bash
pip install -r requirements.txt
```

> Note: `pyaudio` is intentionally omitted from `requirements.txt` because it often requires system-level PortAudio headers and fails in hosted Linux build environments.
>
> For local voice capture support, install PyAudio manually:
>
> - Windows: `pip install pipwin && pipwin install pyaudio`
> - Ubuntu/Debian: `sudo apt-get update && sudo apt-get install portaudio19-dev && pip install pyaudio`
>
> If you do not need microphone-based voice control, the app will run without PyAudio.
