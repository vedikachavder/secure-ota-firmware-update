from pathlib import Path
import json
from flask import Flask, abort, jsonify, send_from_directory

ROOT = Path(__file__).resolve().parents[1]
FIRMWARE_DIR = ROOT / "firmware"
app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "Secure OTA test server"})

@app.get("/metadata")
def metadata():
    # Prefer ECDSA metadata if present; otherwise RSA metadata.
    for name in ("ecdsa_v1_metadata.json", "rsa_v1_metadata.json"):
        path = FIRMWARE_DIR / name
        if path.is_file():
            return jsonify(json.loads(path.read_text(encoding="utf-8")))
    return jsonify({
        "status": "No signed test package yet",
        "next_step": "Run tools/generate_keys.py and tools/sign_firmware.py"
    }), 404

@app.get("/files/<path:filename>")
def download_file(filename):
    allowed = {p.name for p in FIRMWARE_DIR.iterdir() if p.is_file()}
    if filename not in allowed:
        abort(404)
    return send_from_directory(FIRMWARE_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    print("Starting local Secure OTA test server on port 5000.")
    print("Open http://127.0.0.1:5000/health and /metadata")
    app.run(host="0.0.0.0", port=5000, debug=False)
