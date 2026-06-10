with open('C:/agent-workspace/generate_agent_dll.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the init_body line
idx = content.find('std::string init_body = ')
print('found at index:', idx)
snippet = content[idx:idx+200]
print('snippet repr:', repr(snippet))
print('snippet bytes:', snippet.encode('utf-8').hex())

# Now evaluate the entire file as f-string to see what happens
# Actually, let's just extract the cpp variable assignment
start = content.find("cpp = f'''")
end = content.find("'''\n\nwith open('agent_dll.cpp'")
cpp_code = content[start:end+3]
print('cpp assignment starts with:', repr(cpp_code[:50]))

# Execute just the cpp assignment
exec(cpp_code)
print('cpp variable type:', type(cpp))
print('cpp init_body part:', repr(cpp[idx:idx+200]))

