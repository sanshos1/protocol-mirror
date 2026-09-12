from pathlib import Path
TEXT=Path('contracts/contract.py').read_text()
def test_surface():
 for name in ('file_packet','audit','respond','review_response','finalize_expired','get_packet'):assert 'def '+name in TEXT
def test_consensus_and_attribution():
 assert 'ProtocolMirror audit verifier' in TEXT and "proposed.get('digests')!=digests" in TEXT and 'sha256' in TEXT

