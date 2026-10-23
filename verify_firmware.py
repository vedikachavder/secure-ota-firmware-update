import argparse
from pathlib import Path
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding

ROOT = Path(__file__).resolve().parents[1]
FIRMWARE = ROOT / "firmware" / "demo_firmware.bin"
KEYS = ROOT / "keys"

def main():
    parser = argparse.ArgumentParser(description="Verify a firmware file using its public key.")
    parser.add_argument("--algorithm", choices=["ecdsa", "rsa"], required=True)
    parser.add_argument("--firmware", type=Path, default=FIRMWARE)
    parser.add_argument("--signature", type=Path, default=None)
    args = parser.parse_args()

    sig_path = args.signature or (ROOT / "firmware" / f"{args.algorithm}_v1.sig")
    pub_path = KEYS / f"{args.algorithm}_public.pem"
    if not args.firmware.is_file() or not sig_path.is_file() or not pub_path.is_file():
        raise SystemExit("Missing firmware/signature/public key. Generate keys and sign first.")

    public_key = serialization.load_pem_public_key(pub_path.read_bytes())
    data = args.firmware.read_bytes()
    signature = sig_path.read_bytes()

    try:
        if args.algorithm == "ecdsa":
            public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))
        else:
            public_key.verify(
                signature, data,
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256(),
            )
        print("PASS: signature is valid for these exact file bytes.")
    except InvalidSignature:
        print("FAIL: signature invalid; file may be modified or signature/key mismatched.")
        raise SystemExit(1)

if __name__ == "__main__":
    main()
