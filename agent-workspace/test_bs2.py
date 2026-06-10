# One backslash in source
s1 = f'''{{\\""'''
print('one backslash source bytes:', f'''{{\\""'''.encode('utf-8').hex())
print('one backslash result:', repr(s1))

# Two backslashes in source
s2 = f'''{{\\\\\\""'''
print('two backslashes source bytes:', f'''{{\\\\\\""'''.encode('utf-8').hex())
print('two backslashes result:', repr(s2))

