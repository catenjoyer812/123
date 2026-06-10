import os
import time
import requests

BASE = 'http://127.0.0.1:8443'
GUID = '68C9C8D9-C35D-4CF7-A4FB-88B9DC5B1928'

# Create 1MB test file
path = 'C:/agent-workspace/test_big.bin'
with open(path, 'wb') as f:
    f.write(os.urandom(1024 * 1024))
file_size = os.path.getsize(path)
print(f'Created test_big.bin ({file_size} bytes)')

# Send upload command
r = requests.post(f'{BASE}/api/agents/{GUID}/command', json={'cmd': f'upload {path}'})
print(f'Upload queued: {r.json()}')

# Wait 10 seconds for upload to start processing
print('Waiting 10s...')
time.sleep(10)

# Check upload state
files = requests.get(f'{BASE}/api/files').json()
print(f'Files before kill: {files}')

# Kill server
print('Killing server...')
os.system('taskkill /F /IM python.exe >nul 2>&1')
time.sleep(3)

# Restart server
print('Restarting server...')
os.system('cd /c/agent-workspace && python c2_server.py > server_test.log 2>&1 &')
time.sleep(5)

# Poll for completion
print('Polling for completion...')
completed = False
for i in range(15):
    time.sleep(5)
    try:
        files = requests.get(f'{BASE}/api/files').json()
        for f in files:
            if f.get('filename') == 'test_big.bin':
                print(f'  progress: {f["received"]}/{f["total_size"]} status={f["status"]}')
                if f['status'] == 'completed':
                    print('UPLOAD COMPLETED SUCCESSFULLY')
                    completed = True
                    break
        if completed:
            break
    except Exception as e:
        print(f'  connection error (server still starting?): {type(e).__name__}')

if completed:
    uploaded_path = f'C:/agent-workspace/uploads/{GUID}/test_big.bin'
    if os.path.exists(uploaded_path):
        uploaded_size = os.path.getsize(uploaded_path)
        print(f'Uploaded file size: {uploaded_size} bytes')
        if uploaded_size == file_size:
            print('SIZE MATCH: OK')
            # Verify content
            with open(path, 'rb') as f:
                original = f.read()
            with open(uploaded_path, 'rb') as f:
                uploaded = f.read()
            if original == uploaded:
                print('CONTENT MATCH: OK')
            else:
                print('CONTENT MISMATCH: FAIL')
        else:
            print('SIZE MISMATCH: FAIL')
    else:
        print('UPLOADED FILE NOT FOUND')
else:
    print('Upload did not complete within 75s')

