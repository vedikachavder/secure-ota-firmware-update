from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.hazmat.primitives import serialization

ROOT = Path(__file__).resolve().parents[1]
KEYS = ROOT / "keys"
KEYS.mkdir(exist_ok=True)

# ECDSA P-256 test key pair
ec_private = ec.generate_private_key(ec.SECP256R1())
(KEYS / "ecdsa_private.pem").write_bytes(
    ec_private.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
)
(KEYS / "ecdsa_public.pem").write_bytes(
    ec_private.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
)

# RSA 2048-bit test key pair
rsa_private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
(KEYS / "rsa_private.pem").write_bytes(
    rsa_private.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
)
(KEYS / "rsa_public.pem").write_bytes(
    rsa_private.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
)

print("Test key pairs created in keys/. Keep private keys secret and out of Git.")
print("ECDSA: P-256 with SHA-256. RSA: 2048-bit with RSA-PSS/SHA-256.")
