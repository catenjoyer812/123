# Exact pattern from generator
cpp = f'''std::string init_body = "{{\\"" + std::string(fcg) + "\\":\\"" + job->guid + "\\",\\"" + std::string(fcf) + "\\":\\"" + sbn + "\\",\\"" + std::string(fct) + "\\":" + std::to_string(total) + "}}";'''
print('cpp repr:', repr(cpp))
print('---')
# Find the init_body part
import re
m = re.search(r'init_body = (.*?);', cpp)
if m:
    print('init_body part:', repr(m.group(1)))
    print('init_body bytes:', m.group(1).encode('utf-8').hex())

