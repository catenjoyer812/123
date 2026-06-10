import urllib.request
import json

guid = "AA3D63EA-7814-4A0B-AB29-6A2091C3B78B"
cmd = r"upload C:\agent-workspace\test_secret.txt"
print("Sending command:", repr(cmd))
req = urllib.request.Request(
    f"http://127.0.0.1:8443/api/agents/{guid}/command",
    data=json.dumps({"cmd": cmd}).encode(),
    headers={"Content-Type": "application/json"}
)
resp = urllib.request.urlopen(req)
print(resp.read().decode())

