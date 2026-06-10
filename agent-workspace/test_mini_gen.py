cpp = f'''std::string init_body = "{{\\"" + std::string(fcg) + "\\":\\"" + job->guid + "\\",\\"" + std::string(fcf) + "\\":\\"" + sbn + "\\",\\"" + std::string(fct) + "\\":" + std::to_string(total) + "}}";'''

with open('C:/agent-workspace/test_mini_out.txt', 'w', encoding='utf-8', newline='\n') as f:
    f.write(cpp)

import re
m = re.search(r'init_body = (.*?);', cpp)
if m:
    print('repr:', repr(m.group(1)))
    print('hex:', m.group(1).encode('utf-8').hex())

