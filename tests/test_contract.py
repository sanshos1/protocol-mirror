from pathlib import Path
TEXT=Path('contracts/contract.py').read_text(); PAGE=Path('docs/index.html').read_text()
def test_surface():
 for name in ('file_packet','audit','respond','review_response','finalize_expired','get_packet'):assert 'def '+name in TEXT
def test_consensus_and_attribution():
 assert 'ProtocolMirror audit verifier' in TEXT and "proposed.get('digests')!=digests" in TEXT and 'sha256' in TEXT
 assert "digests[:3]!=json.loads(packet.audit_digests)" in TEXT
 assert 'MIN_RESPONSE_SECONDS=300' in TEXT and 'MAX_RESPONSE_SECONDS=604800' in TEXT
def test_browser_exposes_complete_revised_lifecycle():
 for method in ('file_packet','audit','respond','review_response','finalize_expired','get_packet'):assert method in PAGE
 assert "status:'FINALIZED'" in PAGE and '0x36eF34db3a43E317408Cc564FC1F6c27ab59B3Ec' in PAGE
 assert 'response window' in PAGE.lower() and 'READ CANONICAL RECORD' in PAGE
