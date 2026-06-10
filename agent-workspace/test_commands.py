import time
import requests

BASE = 'http://127.0.0.1:8443'
GUID = '68C9C8D9-C35D-4CF7-A4FB-88B9DC5B1928'

def send_cmd(cmd):
    r = requests.post(f'{BASE}/api/agents/{GUID}/command', json={'cmd': cmd})
    print(f'  [{cmd}] queued: {r.json()}')
    time.sleep(12)
    out = requests.get(f'{BASE}/api/agents/{GUID}/output').json()
    for line in out:
        if line[1] == cmd and line[2] == 'completed':
            print(f'  [{cmd}] result: {repr(line[3])}')
            return line[3]
    print(f'  [{cmd}] no result yet')
    return None

print('=== Test 1: whoami ===')
send_cmd('whoami')

print('=== Test 2: echo test123 ===')
send_cmd('echo test123')

print('=== Test 3: dir C:/agent-workspace ===')
send_cmd('dir C:/agent-workspace')

print('=== Test 4: upload with forward slashes ===')
with open('C:/agent-workspace/test_upload.txt', 'w') as f:
    f.write('SECRET_CONTENT_12345')
send_cmd('upload C:/agent-workspace/test_upload.txt')
time.sleep(15)
files = requests.get(f'{BASE}/api/files').json()
print(f'  files: {files}')

print('=== Test 5: upload_ext ===')
send_cmd('upload_ext txt')
time.sleep(15)
files2 = requests.get(f'{BASE}/api/files').json()
print(f'  files after ext: {files2}')

