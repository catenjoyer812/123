# Test 1: f-string with literal text
result1 = f'''{{\\""'''
print('literal f-string:', repr(result1))
print('literal bytes:', result1.encode('utf-8').hex())

# Test 2: f-string with variable containing same text
text = '{{\\""'
result2 = f'''{text}'''
print('variable f-string:', repr(result2))
print('variable bytes:', result2.encode('utf-8').hex())

# Test 3: read from file and use as variable
with open('C:/agent-workspace/generate_agent_dll.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
line = lines[384]
prefix = line[:15]
print('prefix from file:', repr(prefix))
result3 = f'''{prefix}'''
print('file variable f-string:', repr(result3))
print('file variable bytes:', result3.encode('utf-8').hex())

