# Test what source text produces what output
source_text = '{{\\\\\\""'
print('source repr:', repr(source_text))
s = f'''{source_text}'''
print('output repr:', repr(s))
print('output bytes:', s.encode('utf-8').hex())

