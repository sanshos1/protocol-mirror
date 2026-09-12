import base64,json,re
from pathlib import Path
from genlayer_py import create_account,create_client
from genlayer_py.chains import studionet
ROOT=Path(__file__).parents[1];ADDRESS='0x807B5Da65f1a3570251F373E4eDade5Eb26C35B0';TX={'deployment':'0xe7921337766a3de09e4a29d12b86e3493c9967a6c96d63607859eba89363ba52','file':'0x2941871520d9573fd4b82b77547c066de736e9a0ba26ca449b5aa8c2cc9cff81','audit':'0xd2dc6e4d0f518f90090c96d1c89fa530994c3647dc5cef4a6444a897b2dc8141'}
def main():
 env=(ROOT.parents[3]/'accounts.env').read_text();key=re.search(r'^ACCOUNT_3_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)',env,re.M).group(1).strip();account=create_account(account_private_key=key);client=create_client(chain=studionet,account=account);items={name:client.get_transaction(transaction_hash=value) for name,value in TX.items()};record=client.read_contract(address=ADDRESS,function_name='get_packet',args=['LIVE-1789230055']);source=base64.b64decode(items['deployment']['data']['contract_code']).decode();print(json.dumps({'transactions':{name:{'status':tx['status'],'execution':tx['consensus_data']['leader_receipt'][0]['execution_result']} for name,tx in items.items()},'walletMatches':all(tx['from_address'].lower()==account.address.lower() for tx in items.values()),'sourceMatches':source==(ROOT/'contracts'/'contract.py').read_text(),'record':{'id':record['id'],'state':record['state'],'finding':record['finding'],'digestCount':len(record['digests'])}},indent=2))
if __name__=='__main__':main()
