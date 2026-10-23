# Secure OTA — Member 2 starter (Server & Signing)

This starter implements the laptop-side foundation for the Secure OTA project:
- Flask server for metadata and firmware downloads
- ECDSA and RSA test-key generation
- Signing exact firmware file bytes and verifying signatures on the laptop
- Version metadata

IMPORTANT:
- `firmware/demo_firmware.bin` is a harmless text placeholder, NOT compiled ESP32 firmware.
- Never flash the placeholder to an ESP32.
- Keep private keys out of GitHub and do not share them. The ESP32 should contain only the matching public verification key.
- This starter is not yet the complete device-side OTA implementation. Coordinate signature encoding, algorithm parameters, hash, version format, and package paths with Member 1 before integration.
- The Flask development server is for a controlled local lab/demo, not production deployment.

## 1. Requirements
Install Python 3.11+ from https://www.python.org/downloads/ if not already installed.

Open a terminal in this folder and run:

Windows:
```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

If `py` is not recognized, try `python` instead.

## 2. Create test keys
```powershell
python tools\generate_keys.py
```
This creates test keys in `keys/`. They are ignored by Git.

## 3. Sign and verify the demo file
```powershell
python tools\sign_firmware.py --algorithm ecdsa --version 1
python tools\verify_firmware.py --algorithm ecdsa
python tools\sign_firmware.py --algorithm rsa --version 1
python tools\verify_firmware.py --algorithm rsa
```

To demonstrate tamper detection, make a COPY of the firmware file, change one byte/character in the copy, and verify that copy using the matching signature. Do not edit your only known-good file.

## 4. Start the server
```powershell
python server\app.py
```
Open http://127.0.0.1:5000/health and http://127.0.0.1:5000/metadata in a browser.
To test from another device on the same trusted Wi-Fi, use the laptop's LAN IP instead of 127.0.0.1 and ensure the firewall permits the port. Do not expose this demo server to the public internet.

## 5. Expected outputs / evidence
Save screenshots of:
1. Python and pip versions
2. Key generation completed (do not show or upload private key contents)
3. Valid ECDSA verification
4. Valid RSA verification
5. Tampered-file verification failure
6. Flask `/health` and `/metadata` pages
7. Firmware file downloaded from the server

## 6. Important integration notes
- Signatures cover the exact bytes of the firmware file.
- ECDSA uses SHA-256 and a DER-encoded ECDSA signature from the `cryptography` library.
- RSA uses RSA-PSS with SHA-256 and MGF1-SHA256; signature length depends on the key size.
- Member 1 must use a compatible verifier and the same encoding/parameters. If the ESP32 API expects a different signature format, agree on a conversion or use a compatible scheme consistently.
- The `version` field is metadata only in this starter. Member 1 must enforce persistent anti-rollback on the device; merely hosting a version number does not implement anti-rollback.
- The demo file is not a real firmware image. Replace it with the compiled ESP32 `.bin` only after the device build is available.
