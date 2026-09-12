import json,re,time
from pathlib import Path
from genlayer_py import create_account,create_client
from genlayer_py.chains import studionet
ROOT=Path(__file__).parents[1];ADDRESS='0x807B5Da65f1a3570251F373E4eDade5Eb26C35B0'
def main():
 env=(ROOT.parents[3]/'accounts.env').read_text();key=re.search(r'^ACCOUNT_3_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)',env,re.M).group(1).strip();client=create_client(chain=studionet,account=create_account(account_private_key=key));item='LIVE-'+str(int(time.time()))
 filed=client.write_contract(address=ADDRESS,function_name='file_packet',args=[item,'Documentation fixture comparison','This technical fixture checks whether three reserved documentation records describe the same registered protocol details.',['https://www.iana.org/domains/reserved','https://www.rfc-editor.org/rfc/rfc2606.txt','https://example.com/']],value=0);fr=client.wait_for_transaction_receipt(transaction_hash=filed,status='ACCEPTED',retries=120,interval=5000)
 audit=client.write_contract(address=ADDRESS,function_name='audit',args=[item,120],value=0);ar=client.wait_for_transaction_receipt(transaction_hash=audit,status='ACCEPTED',retries=120,interval=5000);record=client.read_contract(address=ADDRESS,function_name='get_packet',args=[item]);print(json.dumps({'recordId':item,'fileTx':filed,'fileStatus':fr.get('status_name'),'fileResult':fr.get('result_name'),'auditTx':audit,'auditStatus':ar.get('status_name'),'auditResult':ar.get('result_name'),'state':record['state'],'finding':record['finding'],'digestCount':len(record['digests'])},indent=2,default=str))
if __name__=='__main__':main()
