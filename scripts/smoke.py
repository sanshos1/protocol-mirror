import json,re,time
from pathlib import Path
from genlayer_py import create_account,create_client
from genlayer_py.chains import studionet

ROOT=Path(__file__).parents[1]
ADDRESS='0x36eF34db3a43E317408Cc564FC1F6c27ab59B3Ec'

def execution(receipt):
 rows=(receipt.get('consensus_data') or {}).get('leader_receipt') or []
 return rows[0].get('execution_result') if rows else None

def write(client,function,args):
 tx=client.write_contract(address=ADDRESS,function_name=function,args=args,value=0)
 print(function+'_tx='+str(tx),flush=True)
 receipt=client.wait_for_transaction_receipt(transaction_hash=tx,status='FINALIZED',retries=180,interval=5000)
 print(function+'_receipt='+json.dumps({'status':receipt.get('status_name'),'result':receipt.get('result_name'),'execution':execution(receipt)},default=str),flush=True)
 if receipt.get('status_name')!='FINALIZED' or receipt.get('result_name')!='MAJORITY_AGREE' or execution(receipt)!='SUCCESS':raise RuntimeError(function+' did not finalize successfully')
 return tx

def main():
 env=(ROOT.parents[3]/'accounts.env').read_text();key=re.search(r'^ACCOUNT_3_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)',env,re.M).group(1).strip();client=create_client(chain=studionet,account=create_account(account_private_key=key));item='REMEDIATION-'+str(int(time.time()))
 commit='3d32ad185cdbb0a25dd203039701f00b942c5037';sources=[f'https://raw.githubusercontent.com/sanshos1/protocol-mirror/{commit}/evidence/preregistration.txt',f'https://cdn.jsdelivr.net/gh/sanshos1/protocol-mirror@{commit}/evidence/publication.txt',f'https://github.com/sanshos1/protocol-mirror/raw/{commit}/evidence/dataset.txt']
 txs={};txs['file']=write(client,'file_packet',[item,'Preregistration divergence audit','The preregistered primary outcome, sample method, exclusions, analysis plan, and stopping rule match the publication and dataset.',sources,3600]);txs['audit']=write(client,'audit',[item]);record=client.read_contract(address=ADDRESS,function_name='get_packet',args=[item])
 if record['state']!='AUDITED':raise RuntimeError('audit receipt finalized but canonical state is '+record['state'])
 if record['audit']['finding']=='ALIGNED':raise RuntimeError('fixture unexpectedly aligned; response path was not exercised')
 response=f'https://raw.githack.com/sanshos1/protocol-mirror/{commit}/evidence/response.txt';txs['respond']=write(client,'respond',[item,'The owner acknowledges every detected divergence and publishes a corrective disclosure without changing the original records.',response]);txs['reviewResponse']=write(client,'review_response',[item]);record=client.read_contract(address=ADDRESS,function_name='get_packet',args=[item])
 if record['state']!='FINAL' or len(record['audit']['digests'])!=3 or len(record['final']['review_digests'])!=4:raise RuntimeError('canonical final record is incomplete')
 print(json.dumps({'contract':ADDRESS,'recordId':item,'transactions':txs,'state':record['state'],'immutableAudit':record['audit'],'final':record['final']},indent=2,default=str))

if __name__=='__main__':main()
