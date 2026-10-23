import argparse
import hashlib
import json
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIRMWARE = ROOT / "firmware" / "demo_firmware.bin"
KEYS = ROOT / "keys"
OUT = ROOT / "firmware"

def main():
    parser = argparse.ArgumentParser(description="Sign exact firmware bytes for OTA testing.")
    parser.add_argument("--algorithm", choices=["ecdsa", "rsa"], required=True)
    parser.add_argument("--version", type=int, required=True)
    parser.add_argument("--firmware", type=Path, default=DEFAULT_FIRMWARE)
    args = parser.parse_args()

    if args.version < 1:
        raise SystemExit("Version must be a positive integer.")
    if not args.firmware.is_file():
        raise SystemExit(f"Firmware file not found: {args.firmware}")

    key_path = KEYS / f"{args.algorithm}_private.pem"
    if not key_path.is_file():
        raise SystemExit("Private key missing. Run: python tools/generate_keys.py")

    data = args.firmware.read_bytes()
    private_key = serialization.load_pem_private_key(key_path.read_bytes(), password=None)

    if args.algorithm == "ecdsa":
        signature = private_key.sign(data, ec.ECDSA(hashes.SHA256()))
    else:
        signature = private_key.sign(
            data,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )

    sig_path = OUT / f"{args.algorithm}_v{args.version}.sig"
    sig_path.write_bytes(signature)
    metadata = {
        "version": args.version,
        "algorithm": args.algorithm.upper(),
        "hash": "SHA-256",
        "firmware_file": args.firmware.name,
        "signature_file": sig_path.name,
        "firmware_size_bytes": len(data),
        "firmware_sha256": hashlib.sha256(data).hexdigest(),
        "signature_encoding": "ECDSA DER" if args.algorithm == "ecdsa" else "RSA-PSS",
        "status": "TEST PACKAGE — verify on device before accepting"
    }
    meta_path = OUT / f"{args.algorithm}_v{args.version}_metadata.json"
    meta_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"Signed {args.firmware.name} using {args.algorithm.upper()}.")
    print(f"Signature: {sig_path}")
    print(f"Metadata:  {meta_path}")
    print(f"SHA-256:   {metadata['firmware_sha256']}")

if __name__ == "__main__":
    main()
