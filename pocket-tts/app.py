import os
import tempfile
from flask import Flask, request, send_file, jsonify
from pocket_tts import TTSModel
import scipy.io.wavfile

app = Flask(__name__)

# ── HuggingFace token (for accessing private/gated voice files on HF) ──────
HF_TOKEN = os.environ.get("HF_TOKEN", "")
if HF_TOKEN:
    os.environ["HF_TOKEN"] = HF_TOKEN

# ── Load model once at startup ──────────────────────────────────────────────
print("Loading TTS model...")
tts_model = TTSModel.load_model()
print("TTS model ready!")

# ── Voice config ─────────────────────────────────────────────────────────────
PRESET_VOICES = ["alba", "marius", "javert", "jean", "fantine", "cosette", "eponine", "azelma"]

voice_cache = {}

def get_voice_state(voice_name):
    """Cache voice states to avoid reloading on every request"""
    if voice_name not in voice_cache:
        print(f"Loading voice: {voice_name}")
        voice_cache[voice_name] = tts_model.get_state_for_audio_prompt(voice_name)
    return voice_cache[voice_name]

# Pre-warm alba voice at startup
print("Pre-loading alba voice...")
try:
    get_voice_state("alba")
    print("Alba voice ready!")
except Exception as e:
    print(f"Warning: Could not load alba voice: {e}")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "preset_voices": PRESET_VOICES,
        "default_voice": "alba"
    })


@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field in request body"}), 400

    text = data["text"].strip()
    voice = data.get("voice", "alba")  # Default to alba

    if not text:
        return jsonify({"error": "Text cannot be empty"}), 400

    if voice not in PRESET_VOICES:
        return jsonify({
            "error": f"Unknown voice '{voice}'. Use one of: {PRESET_VOICES}"
        }), 400

    try:
        voice_state = get_voice_state(voice)
        audio = tts_model.generate_audio(voice_state, text)

        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        scipy.io.wavfile.write(tmp.name, tts_model.sample_rate, audio.numpy())

        return send_file(
            tmp.name,
            mimetype="audio/wav",
            as_attachment=True,
            download_name="tts_output.wav"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)