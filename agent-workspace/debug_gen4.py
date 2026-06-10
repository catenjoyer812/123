with open('C:/agent-workspace/generate_agent_dll.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the init_body line in the file
idx = content.find('std::string init_body = ')
snippet = content[idx:idx+60]
print('snippet from file:', repr(snippet))
print('snippet bytes:', snippet.encode('utf-8').hex())

# Now create an f-string with this snippet as LITERAL text (not variable)
# We need to embed it in the source code
with open('C:/agent-workspace/test_embed.py', 'w', encoding='utf-8', newline='\n') as f:
    f.write("result = f'''" + snippet + "'''\n")
    f.write("print('embed result:', repr(result))\n")
    f.write("print('embed bytes:', result.encode('utf-8').hex())\n")

print('wrote test_embed.py')

