# Protocol Mirror

[Open the live light table](https://sanshos1.github.io/protocol-mirror/) · [Inspect the StudioNet contract](https://explorer-studio.genlayer.com/address/0x807B5Da65f1a3570251F373E4eDade5Eb26C35B0)

Protocol Mirror is a GenLayer research-integrity primitive. It compares a preregistration, publication, and archived dataset without trusting a caller-written conclusion. Validators fetch all three records, preserve their SHA-256 digests, and agree on a closed-set finding and exact divergence codes.

Lifecycle: `FILED → AUDITED → RESPONDED → FINAL`. An owner can answer a divergence from a fourth, new origin during the stored response window. Otherwise anyone can finalize the unanswered audit after expiry.

```bash
genvm-lint contracts/contract.py
python -m pytest -q
python scripts/verify_deployment.py
```

Submission URLs are evidence locations, not a claim that their operators are independent authorities. Smoke records are labelled technical fixtures.

## Verified deployment

- Contract: [`0x807B…35B0`](https://explorer-studio.genlayer.com/address/0x807B5Da65f1a3570251F373E4eDade5Eb26C35B0)
- Deployment: [`0xe792…ba52`](https://explorer-studio.genlayer.com/transactions/0xe7921337766a3de09e4a29d12b86e3493c9967a6c96d63607859eba89363ba52)
- Live file: [`0x2941…ff81`](https://explorer-studio.genlayer.com/transactions/0x2941871520d9573fd4b82b77547c066de736e9a0ba26ca449b5aa8c2cc9cff81) — FINALIZED / SUCCESS
- Live validator audit: [`0xd2dc…8141`](https://explorer-studio.genlayer.com/transactions/0xd2dc6e4d0f518f90090c96d1c89fa530994c3647dc5cef4a6444a897b2dc8141) — FINALIZED / SUCCESS
- The deployed source matches `contracts/contract.py` byte-for-byte. The technical fixture reached `AUDITED` and stored three evidence digests.
