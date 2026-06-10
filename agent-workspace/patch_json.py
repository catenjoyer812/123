with open('generate_agent_dll.py', 'r', encoding='utf-8') as f:
    s = f.read()
old = "            p += klen + 1; while(*p && (*p == ' ' || *p == ':' || *p == ' ')) p++;"
new = "            p += klen + 1; if(*p == '\"') p++; while(*p && (*p == '\"' || *p == ' ' || *p == ':')) p++;"
s = s.replace(old, new)
with open('generate_agent_dll.py', 'w', encoding='utf-8', newline='\n') as f:
    f.write(s)
print('patched')

