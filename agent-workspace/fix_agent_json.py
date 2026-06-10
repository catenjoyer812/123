with open('C:/agent-workspace/agent_dll.cpp', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix init_body line
old1 = '    std::string init_body = "{"" + std::string(fcg) + "":"" + job->guid + "","" + std::string(fcf) + "":"" + sbn + "","" + std::string(fct) + "":" + std::to_string(total) + "}";'
new1 = '    std::string init_body = "{\\"" + std::string(fcg) + "\\":\\"" + job->guid + "\\",\\"" + std::string(fcf) + "\\":\\"" + sbn + "\\",\\"" + std::string(fct) + "\\":" + std::to_string(total) + "}";'
content = content.replace(old1, new1)

# Fix chunk body line
old2 = '        std::string body = "{"" + std::string(fcg) + "":"" + job->guid + "","" + std::string(fcf) + "":"" + sbn + "","" + std::string(fco) + "":" + std::to_string(offset) + ","" + std::string(fcc) + "":"" + chunk_b64 + ""}";'
new2 = '        std::string body = "{\\"" + std::string(fcg) + "\\":\\"" + job->guid + "\\",\\"" + std::string(fcf) + "\\":\\"" + sbn + "\\",\\"" + std::string(fco) + "\\":" + std::to_string(offset) + ",\\"" + std::string(fcc) + "\\":\\"" + chunk_b64 + "\\"}";'
content = content.replace(old2, new2)

with open('C:/agent-workspace/agent_dll.cpp', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print('fixed')

