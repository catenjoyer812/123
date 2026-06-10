# Test with triple-quoted f-string exactly like generator
src1 = f'''{{\\""'''
print('src1 repr:', repr(src1))
print('src1 bytes:', src1.encode('utf-8').hex())

src2 = f'''std::string init_body = "{{\\"" + std::string(fcg) + "\\":\\"" + job->guid + "\\",\\"" + std::string(fcf) + "\\":\\"" + sbn + "\\",\\"" + std::string(fct) + "\\":" + std::to_string(total) + "}}";'''
print('src2 repr:', repr(src2))

# Find init_body part
import re
m = re.search(r'init_body = (.*?);', src2)
if m:
    print('init_body bytes:', m.group(1).encode('utf-8').hex())

