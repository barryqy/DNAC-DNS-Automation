from config import  DNAC_FQDN, \
                    DNAC_PORT, \
                    DNAC_USER, \
                    DNAC_PASSWORD, \
                    SCOPE
import requests
import sys
import json
from requests.auth import HTTPBasicAuth
    
def get_token():
    requests.packages.urllib3.disable_warnings()
    login_url = "https://{0}:{1}/api/system/v1/auth/token".format(DNAC_FQDN, DNAC_PORT) 
    result = requests.post(url=login_url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASSWORD), verify=False)
    result.raise_for_status()
    return result.json()["Token"]

def create_url(path, controller_ip=DNAC_FQDN):
    ### Helper function to create a DNAC API endpoint URL
    if "dna/" in path:
        return "https://%s:%s/%s" % (controller_ip, DNAC_PORT, path)
    else:
        return "https://%s:%s/api/v1/%s" % (controller_ip, DNAC_PORT, path)


def get_url(url,headers={}):

    url = create_url(path=url)
    headers['X-auth-token'] = get_token()
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print("Error processing request", cerror)
        sys.exit(1)

    return response.json()

def update_device(oldip, newip):

    payload = {
	"type": "NETWORK_DEVICE",
	"computeDevice": False,
	"snmpVersion": "NODATACHANGE",
	"snmpROCommunity": "NO!$DATA!$",
	"snmpRWCommunity": "NO!$DATA!$",
	"snmpRetry": "-1",
	"snmpTimeout": "-1",
	"cliTransport": "NO!$DATA!$",
	"userName": "NO!$DATA!$",
	"password": "NO!$DATA!$",
	"enablePassword": "NO!$DATA!$",
	"netconfPort": "-1",
	"ipAddress": [oldip],
	"updateMgmtIPaddressList": [{
		"newMgmtIpAddress": newip,
		"existMgmtIpAddress": oldip
	}]
}
    #print(json.dumps(payload,indent=2))
    #return

    response = put_and_wait("dna/intent/api/v1/network-device", data=payload)
    if response == False:
        print ("Operation failed, exiting...")
        return False
    task = response['id']
    time.sleep(5)
    tree = get_url("dna/intent/api/v1/task/{}/tree".format(task))
    logging.debug(json.dumps(tree,indent=2))

    for t in tree['response']:
        if 'failureReason' in t:
            print(t['failureReason'])
        else:
            #progress = json.loads(t['progress'])

            #print (" ".join(['{}:{}'.format(k, progress[k]) for k in progress.keys()]))
            print(t['progress'])

def put_and_wait(url, data):

    token = get_token()
    url = create_url(path=url)
    #headers= { 'x-auth-token': token['token'], 'content-type' : 'application/json'}
    headers= { 'x-auth-token': token, 'content-type' : 'application/json'}

    try:
        response = requests.put(url, headers=headers, data=json.dumps(data), verify=False)
    except requests.exceptions.RequestException  as cerror:
        print ("Error processing request", cerror)
        sys.exit(1)
    if response.status_code == 403:
        sep ("Unauthorized to make a change! Existing...")
        return False
    taskid = response.json()['response']['taskId']
    print ("Waiting for Task %s" % taskid)
    task_result = wait_on_task(taskid, token)

    return task_result
 
def confirm():
    """
    Ask user to enter Y or N (case-insensitive).
    :return: True if the answer is Y.
    :rtype: bool
    """
    answer = ""
    while answer not in ["y", "n"]:
        answer = input("Confirm to update devices [Y/N]? ").lower()
    return answer

def sep(string):
    print ("=" * 80)
    print (string)
    print ("=" * 80)