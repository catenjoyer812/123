with open('C:/agent-workspace/agent_dll.cpp', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: add stdlib.h
content = content.replace(
    '#include <stdarg.h>\n',
    '#include <stdarg.h>\n#include <stdlib.h>\n'
)

# Fix 2: basename extraction
old_basename = "char sbn[64]; { char* p = strrchr((char*)job->filepath.c_str(), '\\'); s_copy(sbn, _e_s_empty, sizeof(_e_s_empty)); strcat(sbn, p ? p+1 : job->filepath.c_str()); }"
new_basename = "size_t bn_pos = job->filepath.find_last_of(\"\\/\");\n    std::string basename = (bn_pos != std::string::npos) ? job->filepath.substr(bn_pos + 1) : job->filepath;\n    char sbn[256]; s_copy(sbn, _e_s_empty, sizeof(_e_s_empty)); strncat(sbn, basename.c_str(), sizeof(sbn)-1);"
content = content.replace(old_basename, new_basename)

# Fix 3: parse offset from init response and seek
old_init = '''    bool inited = false;
    if(!resp.empty()) {
        char* st = _json_field(resp.c_str(), "status");
        char sok[8]; s_copy(sok, _e_status_ok, sizeof(_e_status_ok));
        if(st && strcmp(st, sok) == 0) inited = true;
    }
    if(!inited) { CloseHandle(hFile); _log("upload: init failed"); return; }
    _log("upload: started %s (%lld bytes)", sbn, total);
    LONGLONG offset = 0;
    int retry_count = 0;
    _log("upload: entering chunk loop offset=%lld total=%lld", offset, total);'''
new_init = '''    bool inited = false;
    LONGLONG offset = 0;
    if(!resp.empty()) {
        char* st = _json_field(resp.c_str(), "status");
        char sok[8]; s_copy(sok, _e_status_ok, sizeof(_e_status_ok));
        if(st && strcmp(st, sok) == 0) {
            inited = true;
            char* off_str = _json_field(resp.c_str(), "offset");
            if(off_str) offset = strtoll(off_str, NULL, 10);
        }
    }
    if(!inited) { CloseHandle(hFile); _log("upload: init failed"); return; }
    if(offset > 0) {
        LARGE_INTEGER off; off.QuadPart = offset;
        if(!SetFilePointerEx(hFile, off, NULL, FILE_BEGIN)) {
            _log("upload: seek failed"); CloseHandle(hFile); return;
        }
        _log("upload: resuming from offset %lld", offset);
    }
    _log("upload: started %s (%lld bytes)", sbn, total);
    int retry_count = 0;'''
content = content.replace(old_init, new_init)

with open('C:/agent-workspace/agent_dll.cpp', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print('agent_dll.cpp fixed')

