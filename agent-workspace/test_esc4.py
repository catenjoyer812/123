# Test literal f-string behavior
# In f-string, {{ becomes { and }} becomes }
# We want C++ output: "{\\""
# Let's test different source patterns

s1 = f'''{{\\""'''
print('s1 repr:', repr(s1))
print('s1 bytes:', s1.encode('utf-8').hex())

s2 = f'''{{\\\\\\""'''
print('s2 repr:', repr(s2))
print('s2 bytes:', s2.encode('utf-8').hex())

s3 = f'''{{\\\\\\\\\\\\\\""'''
print('s3 repr:', repr(s3))
print('s3 bytes:', s3.encode('utf-8').hex())

