with open('C:/agent-workspace/generate_agent_dll.py', 'r', encoding='utf-8') as f:
    c = f.read()

# In the generator source, we currently have: find_last_of("/\\");
# In Python string, \\ becomes \. We want the output to be \\ in the C++ file.
# To get \\ in C++ file, Python string content must be \\.
# To get \\ in Python string content, source must have \\\\\\.
# Let's just replace the exact substring.
old = 'find_last_of("/\\\\");'
new = 'find_last_of("/\\\\\\\\");'
c = c.replace(old, new)

with open('C:/agent-workspace/generate_agent_dll.py', 'w', encoding='utf-8', newline='\n') as f:
    f.write(c)

print('fixed')

