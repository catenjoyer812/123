# Test what generator source text produces correct C++ output
source = '{{\\""'
print('source:', repr(source))
out = f'''{source}'''
print('output:', repr(out))
print('output bytes:', out.encode('utf-8').hex())

# What we need for C++: "{\\""
# In Python f-string, to get {\\"", we need {{\\\\\\""
source2 = '{{\\\\\\\\\\""'
print('source2:', repr(source2))
out2 = f'''{source2}'''
print('output2:', repr(out2))
print('output2 bytes:', out2.encode('utf-8').hex())

