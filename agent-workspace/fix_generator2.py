with open('C:/agent-workspace/generate_agent_dll.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and replace specific line ranges
i = 0
while i < len(lines):
    # Fix include
    if '#include <stdarg.h>' in lines[i] and '#include <stdlib.h>' not in lines[i+1]:
        lines.insert(i+1, '#include <stdlib.h>\n')
        i += 2
        continue
    i += 1

# Now write back
with open('C:/agent-workspace/generate_agent_dll.py', 'w', encoding='utf-8', newline='\n') as f:
    f.writelines(lines)

print('includes fixed')

