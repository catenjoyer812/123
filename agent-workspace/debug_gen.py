with open('C:/agent-workspace/generate_agent_dll.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
line = lines[384]
print('line bytes read by Python:', line.encode('utf-8').hex())
print('line repr:', repr(line))

# Check if backslash is present
if chr(92) in line:
    print('backslash FOUND')
else:
    print('backslash NOT found')

# Now let's see what the f-string produces for just the first few chars
prefix = line[:50]
print('prefix:', repr(prefix))
result = eval("f'''" + prefix + "'''")
print('f-string result:', repr(result))
print('f-string result bytes:', result.encode('utf-8').hex())

