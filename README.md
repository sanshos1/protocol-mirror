# Protocol Mirror

Protocol Mirror is a GenLayer research-integrity primitive. It compares a preregistration, publication, and archived dataset without trusting a caller-written conclusion. Validators fetch all three records, preserve their SHA-256 digests, and agree on a closed-set finding and exact divergence codes.

Lifecycle: `FILED → AUDITED → RESPONDED → FINAL`. An owner can answer a divergence from a fourth, new origin during the stored response window. Otherwise anyone can finalize the unanswered audit after expiry.

```bash
genvm-lint contracts/contract.py
python -m pytest -q
```

Submission URLs are evidence locations, not a claim that their operators are independent authorities. Smoke records are labelled technical fixtures.
