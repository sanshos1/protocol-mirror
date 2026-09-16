# Steward remediation matrix

| Steward requirement | Implementation | Test or live proof | Status |
|---|---|---|---|
| Preserve the original audit | `Packet.audit_*` fields are never overwritten by response review | `test_response_review_preserves_original_audit_and_all_digests` and record `REMEDIATION-1789588049` | PASS |
| Preserve every source digest used for the response ruling | `final.review_digests` stores all four fetched digests | Direct test plus canonical record with 4 digests | PASS |
| Reject changed originals | Response review requires its first three digests to equal `audit_digests` | `test_response_review_rejects_changed_original_source` | PASS |
| Bound who sets the response window and its maximum | Packet owner chooses it during filing; contract enforces 300–604,800 seconds | `test_owner_bounds_response_window_at_filing` | PASS |
| Expose full workflow in the repository app | Public UI implements file, audit, respond, review response, finalize expired, and readback | Static frontend test; production verification after GitHub Pages deployment | PENDING DEPLOYMENT |
| Focused success and changed-content tests | Direct suite covers successful review and changed-original rejection | 10-test suite | PASS |
| Verify a complete network lifecycle | File, audit, response, and review transactions all finalized successfully | `evidence/remediation-run.json` | PASS |
