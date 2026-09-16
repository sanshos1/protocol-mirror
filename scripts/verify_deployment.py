import base64,json,re
from pathlib import Path
from genlayer_py import create_account,create_client
from genlayer_py.chains import studionet

ROOT=Path(__file__).parents[1]
manifest=json.loads((ROOT/'deployment.json').read_text())
run=json.loads((ROOT/'evidence'/'remediation-run.json').read_text())

def execution(tx):
 rows=(tx.get('consensus_data') or {}).get('leader_receipt') or []
 return rows[0].get('execution_result') if rows else None

def main():
 env=(ROOT.parents[3]/'accounts.env').read_text();key=re.search(r'^ACCOUNT_3_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)',env,re.M).group(1).strip();account=create_account(account_private_key=key);client=create_client(chain=studionet,account=account)
 hashes={'deployment':manifest['deploymentTransaction'],**run['transactions']};transactions={name:client.get_transaction(transaction_hash=value) for name,value in hashes.items()};record=client.read_contract(address=manifest['contractAddress'],function_name='get_packet',args=[run['recordId']]);deployed=base64.b64decode(transactions['deployment']['data']['contract_code']).decode();local=(ROOT/'contracts'/'contract.py').read_text()
 checks={'walletMatches':all(tx['from_address'].lower()==account.address.lower() for tx in transactions.values()),'sourceMatches':deployed==local,'allFinalized':all(tx.get('status_name')=='FINALIZED' for tx in transactions.values()),'allAgree':all(tx.get('result_name')=='MAJORITY_AGREE' for tx in transactions.values()),'allSuccessful':all(execution(tx)=='SUCCESS' for tx in transactions.values()),'canonicalFinal':record['state']=='FINAL','auditPreserved':len(record['audit']['digests'])==3,'responseDigestsComplete':len(record['final']['review_digests'])==4 and record['final']['review_digests'][:3]==record['audit']['digests']}
 if not all(checks.values()):raise RuntimeError('verification failed: '+json.dumps(checks))
 print(json.dumps({'contract':manifest['contractAddress'],'recordId':run['recordId'],'checks':checks,'audit':record['audit'],'final':record['final'],'transactions':{name:{'hash':hashes[name],'status':tx.get('status_name'),'consensus':tx.get('result_name'),'execution':execution(tx)} for name,tx in transactions.items()}},indent=2))

if __name__=='__main__':main()
