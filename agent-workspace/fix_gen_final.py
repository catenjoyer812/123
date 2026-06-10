with open('C:/agent-workspace/generate_agent_dll.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Remove old duplicate _up() lines 370-384 (0-indexed 369:384)
# These are the lines from "static void _up(_uj* job) {{" to "    std::string resp = _http_json(host, pui, init_body);"
# Actually let's find the exact range
start_old = None
end_old = None
for i, line in enumerate(lines):
    if 'static void _up(_uj* job) {{' in line and i < 380:
        start_old = i
    if start_old is not None and 'std::string resp = _http_json(host, pui, init_body);' in line and i < 390:
        end_old = i + 1
        break

if start_old is not None and end_old is not None:
    del lines[start_old:end_old]
    print(f'removed old _up lines {start_old+1}-{end_old}')
else:
    print('old _up not found')

# Find where to insert _he and _sd declarations
# After the new _up() which ends with "CloseHandle(hFile);\n" and "}}\n"
insert_idx = None
for i in range(len(lines)-1):
    if lines[i].strip() == 'CloseHandle(hFile);' and lines[i+1].strip() == '}}':
        # Make sure this is after the new _up() (check for strncat earlier)
        insert_idx = i + 2
        break

if insert_idx:
    new_funcs = '''\nstatic bool _he(const std::string& path, const std::string& ext) {{
    size_t p = path.find_last_of('.');
    if(p == std::string::npos) return false;
    std::string e = path.substr(p + 1);
    if(e.length() != ext.length()) return false;
    return _stricmp(e.c_str(), ext.c_str()) == 0;
}}

static void _sd(const std::string& dir, const std::string& ext, std::vector<std::string>& out) {{
'''
    lines.insert(insert_idx, new_funcs)
    print(f'inserted _he and _sd at line {insert_idx+1}')
else:
    print('insert point not found')

with open('C:/agent-workspace/generate_agent_dll.py', 'w', encoding='utf-8', newline='\n') as f:
    f.writelines(lines)

print('generator fixed')

