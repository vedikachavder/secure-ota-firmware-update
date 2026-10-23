# Member 2 — today's deliverables checklist

- [ ] Python and pip versions recorded
- [ ] Flask and cryptography installed in a virtual environment
- [ ] Key-generation script runs
- [ ] ECDSA test signature created and laptop verification passes
- [ ] RSA test signature created and laptop verification passes
- [ ] Tampered-copy test fails verification
- [ ] Flask health endpoint works
- [ ] Metadata endpoint works after signing
- [ ] Firmware and signature files download from the server
- [ ] Screenshots saved (do not reveal private-key contents)
- [ ] Member 1 agrees on signature encoding, hash, algorithm parameters, metadata names, and version policy
- [ ] GitHub repository contains source only; private keys and generated secret files excluded

## Questions to ask Member 1
1. What exact ESP32 board and framework are being used?
2. What compiled firmware `.bin` file will be signed?
3. Which device-side crypto API will verify ECDSA and RSA?
4. Does it expect ECDSA DER or raw `r || s` signature bytes?
5. How will metadata be authenticated, and where will version state be stored?
6. What HTTP endpoint and package naming format should the ESP32 use?
