import sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    lines = f.readlines()

old_func_start = 'static char* _json_field(const char* json, const char* key) {'
new_func = '''static char* _json_field(const char* json, const char* key) {
    static char buf[4096];
    std::string j(json);
    std::string k = std::string("\"") + key + "\"";
    size_t pos = j.find(k);
    if(pos == std::string::npos) return NULL;
    size_t start = pos + k.length();
    if(start < j.length() && j[start] == '"') start++;
    while(start < j.length() && (j[start] == ' ' || j[start] == ':')) start++;
    if(start >= j.length() || j[start] != '"') return NULL;
    start++;
    size_t i = 0;
    while(start < j.length() && j[start] != '"' && i < sizeof(buf)-1) { buf[i++] = j[start++]; }
    buf[i] = '\0'; return buf;
}
'''

start_idx = None
for i, line in enumerate(lines):
    if old_func_start in line:
        start_idx = i
        break

if start_idx is None:
    print('Function not found')
    sys.exit(1)

# Find end of function (closing brace at same indent level)
end_idx = start_idx + 1
brace_count = 1
while end_idx < len(lines) and brace_count > 0:
    stripped = lines[end_idx].strip()
    if stripped.startswith('{'): brace_count += 1
    if stripped.startswith('}'): brace_count -= 1
    if stripped == '}' and brace_count == 0:
        break
    end_idx += 1

new_lines = lines[:start_idx] + [new_func] + lines[end_idx+1:]
with open(sys.argv[1], 'w', encoding='utf-8', newline='\n') as f:
    f.writelines(new_lines)
print(f'Replaced lines {start_idx+1}-{end_idx+1}')

