import os
import time
import requests

BASE = 'http://127.0.0.1:8443'

def get_guid():
    agents = requests.get(f'{BASE}/api/agents').json()
    if agents:
        return list(agents.keys())[0]
    return None

def send_cmd(guid, cmd):
    r = requests.post(f'{BASE}/api/agents/{guid}/command', json={'cmd': cmd})
    return r.json()

def get_result(guid, cmd):
    out = requests.get(f'{BASE}/api/agents/{guid}/output').json()
    for line in out:
        if line[1] == cmd and line[2] == 'completed':
            return line[3]
    return None

def wait_for_result(guid, cmd, timeout=60):
    for _ in range(timeout // 5):
        time.sleep(5)
        result = get_result(guid, cmd)
        if result is not None:
            return result
    return None

print('=== Final C2 Test ===')

# Wait for agent
print('Waiting for agent...')
for _ in range(10):
    guid = get_guid()
    if guid:
        print(f'Agent found: {guid}')
        break
    time.sleep(2)
else:
    print('No agent found')
    exit(1)

# Test 1: whoami
print('\n[Test 1] whoami')
send_cmd(guid, 'whoami')
result = wait_for_result(guid, 'whoami')
print(f'  Result: {repr(result)}')
assert result and 'Admin' in result, 'whoami failed'
print('  PASS')

# Test 2: echo
print('\n[Test 2] echo hello')
send_cmd(guid, 'echo hello')
result = wait_for_result(guid, 'echo hello')
print(f'  Result: {repr(result)}')
assert result and 'hello' in result, 'echo failed'
print('  PASS')

# Test 3: upload small file with forward slashes
print('\n[Test 3] Upload small file')
test_path = 'C:/agent-workspace/test_small.txt'
with open(test_path, 'w') as f:
    f.write('SECRET_CONTENT_SMALL')
send_cmd(guid, f'upload {test_path}')
result = wait_for_result(guid, f'upload {test_path}')
print(f'  Result: {repr(result)}')
assert result and 'started' in result, 'upload command failed'
time.sleep(10)
files = requests.get(f'{BASE}/api/files').json()
uploaded = [f for f in files if f.get('filename') == 'test_small.txt']
assert uploaded, 'file not found in uploads'
assert uploaded[0]['status'] == 'completed', 'upload not completed'
uploaded_path = f'C:/agent-workspace/uploads/{guid}/test_small.txt'
with open(uploaded_path, 'r') as f:
    content = f.read()
assert content == 'SECRET_CONTENT_SMALL', 'upload content mismatch'
print('  PASS')

# Test 4: upload large file with connection drop
print('\n[Test 4] Upload large file with connection drop')
big_path = 'C:/agent-workspace/test_big.bin'
with open(big_path, 'wb') as f:
    f.write(os.urandom(1024 * 1024))
file_size = os.path.getsize(big_path)
print(f'  Created {file_size} bytes file')
send_cmd(guid, f'upload {big_path}')
time.sleep(8)
files = requests.get(f'{BASE}/api/files').json()
big_files = [f for f in files if f.get('filename') == 'test_big.bin']
if big_files:
    print(f'  Before kill: received={big_files[0]["received"]}')
else:
    print('  Before kill: not started yet')

# Kill server
print('  Killing server...')
os.system('taskkill /F /IM python.exe >nul 2>&1')
time.sleep(3)

# Restart server
print('  Restarting server...')
os.system('cd /c/agent-workspace && python c2_server.py > server_test.log 2>&1 &')
time.sleep(5)

# Poll for completion
print('  Polling for completion...')
completed = False
for i in range(15):
    time.sleep(5)
    try:
        files = requests.get(f'{BASE}/api/files').json()
        for f in files:
            if f.get('filename') == 'test_big.bin':
                print(f'    progress: {f["received"]}/{f["total_size"]} status={f["status"]}')
                if f['status'] == 'completed':
                    completed = True
                    break
        if completed:
            break
    except Exception as e:
        print(f'    connection error: {type(e).__name__}')

assert completed, 'upload did not complete after server restart'
uploaded_big = f'C:/agent-workspace/uploads/{guid}/test_big.bin'
assert os.path.exists(uploaded_big), 'uploaded file not found'
uploaded_size = os.path.getsize(uploaded_big)
assert uploaded_size == file_size, f'size mismatch: {uploaded_size} != {file_size}'
with open(big_path, 'rb') as f:
    original = f.read()
with open(uploaded_big, 'rb') as f:
    uploaded = f.read()
assert original == uploaded, 'content mismatch'
print('  PASS')

# Test 5: upload_ext
print('\n[Test 5] upload_ext txt')
send_cmd(guid, 'upload_ext txt')
result = wait_for_result(guid, 'upload_ext txt')
print(f'  Result: {repr(result)}')
assert result and 'scanning' in result, 'upload_ext failed'
print('  PASS')

print('\n=== ALL TESTS PASSED ===')

