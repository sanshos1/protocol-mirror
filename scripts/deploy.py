import json,re
from pathlib import Path
from genlayer_py import create_account,create_client
from genlayer_py.chains import studionet
ROOT=Path(__file__).parents[1]
def main():
 env=(ROOT.parents[3]/'accounts.env').read_text();match=re.search(r'^ACCOUNT_3_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)',env,re.M)
 if not match:raise RuntimeError('ACCOUNT_3_GENLAYER_PRIVATE_KEY is missing')
 client=create_client(chain=studionet,account=create_account(account_private_key=match.group(1).strip()));tx=client.deploy_contract(code=(ROOT/'contracts'/'contract.py').read_text(),args=[]);print('deployment_tx='+str(tx),flush=True);receipt=client.wait_for_transaction_receipt(transaction_hash=tx,status='FINALIZED',retries=180,interval=5000);address=receipt.get('data',{}).get('contract_address')
 if not address:raise RuntimeError('deployment address missing')
 execution=((receipt.get('consensus_data') or {}).get('leader_receipt') or [{}])[0].get('execution_result')
 if receipt.get('status_name')!='FINALIZED' or execution!='SUCCESS':raise RuntimeError('deployment did not finalize successfully')
 print(json.dumps({'contract':address,'deploymentTx':tx,'network':'StudioNet','status':receipt.get('status_name'),'result':receipt.get('result_name'),'execution':execution},default=str),flush=True)
if __name__=='__main__':main()
