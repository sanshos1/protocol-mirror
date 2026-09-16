import hashlib
from conftest import CONTRACT

SOURCES=['https://registry.example/prereg','https://journal.example/paper','https://archive.example/data']
BODIES=[b'Primary outcome: retention. Sample: 300. Analysis: preregistered model.',b'Publication reports retention, sample 300, and the preregistered model.',b'Dataset contains 300 participant records and retention outcomes.']
CLAIM='The preregistered primary outcome, sample method, and analysis plan match the publication and archived dataset.'

def prepared(direct_vm,direct_deploy,direct_alice,audit_result='{"finding":"ALIGNED","divergence_codes":[],"severity":0}'):
 direct_vm.warp('2032-01-01T00:00:00+00:00');direct_vm.sender=direct_alice;c=direct_deploy(CONTRACT);c.file_packet('study-01','Retention intervention replication',CLAIM,SOURCES,600)
 for host,body in zip(('registry.example','journal.example','archive.example'),BODIES):direct_vm.mock_web(host.replace('.',r'\.'),{'status':200,'body':body.decode()})
 direct_vm.mock_llm(r'.*ProtocolMirror audit\..*',audit_result);direct_vm.mock_llm(r'.*ProtocolMirror audit verifier.*','{"valid":true}')
 return c

def test_audit_binds_finding_and_digests(direct_vm,direct_deploy,direct_alice):
 c=prepared(direct_vm,direct_deploy,direct_alice);c.audit('study-01');p=c.get_packet('STUDY-01');assert p['state']=='AUDITED' and p['audit']['finding']=='ALIGNED';assert p['audit']['digests']==[hashlib.sha256(x).hexdigest() for x in BODIES];assert p['response_seconds']==600

def test_duplicate_id_and_origins_fail(direct_vm,direct_deploy,direct_alice):
 c=prepared(direct_vm,direct_deploy,direct_alice)
 with direct_vm.expect_revert('complete three-origin research packet required'):c.file_packet('STUDY-01','Another study packet',CLAIM,SOURCES,600)
 with direct_vm.expect_revert('complete three-origin research packet required'):c.file_packet('other','Another study packet',CLAIM,[SOURCES[0],SOURCES[0]+'?copy=1',SOURCES[2]],600)

def test_owner_bounds_response_window_at_filing(direct_vm,direct_deploy,direct_alice):
 direct_vm.sender=direct_alice;c=direct_deploy(CONTRACT)
 with direct_vm.expect_revert('response window must be 300..604800 seconds'):c.file_packet('short','Another study packet',CLAIM,SOURCES,299)
 with direct_vm.expect_revert('response window must be 300..604800 seconds'):c.file_packet('long','Another study packet',CLAIM,SOURCES,604801)

def test_validator_rejects_forged_digest_and_inconsistent_shape(direct_vm,direct_deploy,direct_alice):
 c=prepared(direct_vm,direct_deploy,direct_alice);result=c._audit(c.packets['STUDY-01']);assert direct_vm.run_validator(leader_result=result) is True
 forged=dict(result);forged['digests']=list(reversed(result['digests']));assert direct_vm.run_validator(leader_result=forged) is False
 forged=dict(result);forged['severity']=3;assert direct_vm.run_validator(leader_result=forged) is False

def test_owner_response_and_permissionless_expiry(direct_vm,direct_deploy,direct_alice,direct_bob):
 c=prepared(direct_vm,direct_deploy,direct_alice,'{"finding":"UNDISCLOSED_DEVIATION","divergence_codes":["PRIMARY_OUTCOME"],"severity":2}');c.audit('study-01')
 direct_vm.sender=direct_bob
 with direct_vm.expect_revert('timely owner response from a new origin required'):c.respond('study-01','The deviation is now explained in a public amendment.','https://response.example/amendment')
 direct_vm.warp('2032-01-01T00:11:00+00:00');c.finalize_expired('study-01');p=c.get_packet('study-01');assert p['final']['ruling']=='UNANSWERED';assert p['final']['finding']==p['audit']['finding'];assert p['final']['review_digests']==p['audit']['digests']

def test_response_review_preserves_original_audit_and_all_digests(direct_vm,direct_deploy,direct_alice):
 c=prepared(direct_vm,direct_deploy,direct_alice,'{"finding":"UNDISCLOSED_DEVIATION","divergence_codes":["PRIMARY_OUTCOME"],"severity":2}');c.audit('study-01');before=c.get_packet('study-01')['audit']
 c.respond('study-01','The corrected public amendment explains the changed primary outcome.','https://response.example/amendment')
 direct_vm.mock_web(r'response\.example',{'status':200,'body':'Public amendment: primary outcome change disclosed and justified.'})
 direct_vm.mock_llm(r'.*ProtocolMirror response review\..*','{"ruling":"CLEARED","finding":"ALIGNED","divergence_codes":[],"severity":0}');direct_vm.mock_llm(r'.*ProtocolMirror response verifier.*','{"valid":true}')
 c.review_response('study-01');p=c.get_packet('study-01');assert p['state']=='FINAL' and p['audit']==before;assert p['final']['ruling']=='CLEARED' and p['final']['finding']=='ALIGNED';assert len(p['final']['review_digests'])==4;assert p['final']['review_digests'][:3]==before['digests']

def test_response_review_rejects_changed_original_source(direct_vm,direct_deploy,direct_alice):
 c=prepared(direct_vm,direct_deploy,direct_alice,'{"finding":"UNDISCLOSED_DEVIATION","divergence_codes":["PRIMARY_OUTCOME"],"severity":2}');c.audit('study-01');c.respond('study-01','The corrected public amendment explains the changed primary outcome.','https://response.example/amendment')
 direct_vm.clear_mocks()
 changed=[b'CHANGED preregistration after audit',BODIES[1],BODIES[2]]
 for host,body in zip(('registry.example','journal.example','archive.example'),changed):direct_vm.mock_web(host.replace('.',r'\.'),{'status':200,'body':body.decode()})
 direct_vm.mock_web(r'response\.example',{'status':200,'body':'Public amendment.'})
 with direct_vm.expect_revert('original evidence changed after audit'):c.review_response('study-01')
