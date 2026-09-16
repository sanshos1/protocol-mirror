# Protocol Mirror

[Open the live application](https://sanshos1.github.io/protocol-mirror/) · [Inspect the corrected StudioNet contract](https://explorer-studio.genlayer.com/address/0x36eF34db3a43E317408Cc564FC1F6c27ab59B3Ec)

Protocol Mirror is a GenLayer research-integrity primitive. It compares a preregistration, publication, and archived dataset without trusting a caller-written conclusion. Validators fetch all three records, preserve their SHA-256 digests, and agree on a closed-set finding with exact divergence codes.

## Immutable lifecycle

1. The owner files three distinct HTTPS origins and chooses a response window bounded to 300–604,800 seconds.
2. Validators fetch and classify the original evidence. The finding, codes, severity, three digests, audit time, and response deadline become an immutable `audit` record.
3. Only the packet owner may submit a timely response, and it must come from a fourth origin.
4. Before reviewing the response, validators re-fetch all originals. Any changed original digest rejects the review.
5. A successful response review stores a separate `final` ruling and all four digests without overwriting the original audit. If no response arrives, anyone may finalize after the deadline.

The public application exposes filing, audit, response, response review, permissionless expiry, transaction finalization, and canonical readback. Every write waits for `FINALIZED`, not merely `ACCEPTED`.

## Verify

```bash
genvm-lint contracts/contract.py
python -m pytest -q
python scripts/verify_deployment.py
```

The direct suite covers bounded response windows, owner-only response, permissionless expiry, immutable audit preservation, every response-review digest, and rejection when an original source changes.

## Verified remediation deployment

- Contract: [`0x36eF…B3Ec`](https://explorer-studio.genlayer.com/address/0x36eF34db3a43E317408Cc564FC1F6c27ab59B3Ec)
- Deployment: [`0x0e9b…fc32`](https://explorer-studio.genlayer.com/transactions/0x0e9b96244b4d9ae7312ec938c1c870d1156d50a6cbac48da2a9cbfbbfadafc32) — FINALIZED / MAJORITY_AGREE / SUCCESS
- File packet: [`0x3b61…47a6`](https://explorer-studio.genlayer.com/transactions/0x3b613dee359e03993f16a592c43e8bb00d00548c7c8bc014d42513cf1c0747a6)
- Audit originals: [`0x2277…7227`](https://explorer-studio.genlayer.com/transactions/0x22770240fd5f5796ef8fea0acf6cdb2632cca96f5d203821d00f0f8b01ca7227)
- Owner response: [`0x7af1…151`](https://explorer-studio.genlayer.com/transactions/0x7af117e96ea77faa6001668619217f7c792c5204bf4f5638cdab9ccc27588151)
- Review response: [`0x69b8…a7ae`](https://explorer-studio.genlayer.com/transactions/0x69b816508b6d744542b16be1e1bf8270e4249fafd2cb4f41ba14635b1f87a7ae)

Record `REMEDIATION-1789588049` reached `FINAL`. Its immutable audit holds three original digests and the final response ruling holds four digests whose first three exactly match the audit. The fixture finding moved from `UNDISCLOSED_DEVIATION` to `DISCLOSED_DEVIATION` without rewriting the original audit.

The evidence URLs are operator-created deterministic fixtures for technical verification; they are not represented as independent research authorities.
