# Test single backslash in f-string
s = f'''{{\\""'''
print('s:', repr(s))
print('s bytes:', s.encode('utf-8').hex())

