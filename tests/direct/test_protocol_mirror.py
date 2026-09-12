import hashlib
from conftest import CONTRACT

SOURCES=['https://registry.example/prereg','https://journal.example/paper','https://archive.example/data']
BODIES=[b'Primary outcome: retention. Sample: 300. Analysis: preregistered model.',b'Publication reports retention, sample 300, and the preregistered model.',b'Dataset contains 300 participant records and retention outcomes.']
CLAIM='The preregistered primary outcome, sample method, and analysis plan match the publication and archived dataset.'

def prepared(direct_vm,direct_deploy,direct_alice):
 direct_vm.warp('2032-01-01T00:00:00+00:00');direct_vm.sender=direct_alice;c=direct_deploy(CONTRACT);c.file_packet('study-01','Retention intervention replication',CLAIM,SOURCES)
 for host,body in zip(('registry.example','journal.example','archive.example'),BODIES):direct_vm.mock_web(host.replace('.',r'\.'),{'status':200,'body':body.decode()})
 direct_vm.mock_llm(r'.*ProtocolMirror audit\..*','{"finding":"ALIGNED","divergence_codes":[],"severity":0}');direct_vm.mock_llm(r'.*ProtocolMirror audit verifier.*','{"valid":true}')
 return c

def test_audit_binds_finding_and_digests(direct_vm,direct_deploy,direct_alice):
 c=prepared(direct_vm,direct_deploy,direct_alice);c.audit('study-01',600);p=c.get_packet('STUDY-01');assert p['state']=='AUDITED' and p['finding']=='ALIGNED';assert p['digests']==[hashlib.sha256(x).hexdigest() for x in BODIES]

def test_duplicate_id_and_origins_fail(direct_vm,direct_deploy,direct_alice):
 c=prepared(direct_vm,direct_deploy,direct_alice)
 with direct_vm.expect_revert('complete three-origin research packet required'):c.file_packet('STUDY-01','Another study packet',CLAIM,SOURCES)
 with direct_vm.expect_revert('complete three-origin research packet required'):c.file_packet('other','Another study packet',CLAIM,[SOURCES[0],SOURCES[0]+'?copy=1',SOURCES[2]])

def test_validator_rejects_forged_digest_and_inconsistent_shape(direct_vm,direct_deploy,direct_alice):
 c=prepared(direct_vm,direct_deploy,direct_alice);result=c._audit(c.packets['STUDY-01']);assert direct_vm.run_validator(leader_result=result) is True
 forged=dict(result);forged['digests']=list(reversed(result['digests']));assert direct_vm.run_validator(leader_result=forged) is False
 forged=dict(result);forged['severity']=3;assert direct_vm.run_validator(leader_result=forged) is False

def test_owner_response_and_permissionless_expiry(direct_vm,direct_deploy,direct_alice,direct_bob):
 c=prepared(direct_vm,direct_deploy,direct_alice);direct_vm.mock_llm(r'.*ProtocolMirror audit\..*','{"finding":"UNDISCLOSED_DEVIATION","divergence_codes":["PRIMARY_OUTCOME"],"severity":2}');c.audit('study-01',600)
 direct_vm.sender=direct_bob
 with direct_vm.expect_revert('timely owner response from a new origin required'):c.respond('study-01','The deviation is now explained in a public amendment.','https://response.example/amendment')
 direct_vm.warp('2032-01-01T00:11:00+00:00');c.finalize_expired('study-01');assert c.get_packet('study-01')['ruling']=='UNANSWERED'

