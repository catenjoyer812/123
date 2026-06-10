# We want C++ output to contain: backslash + quote
# Let's construct the Python source programmatically to avoid any confusion

for num_backslashes in range(1, 8):
    # Construct source with {{ followed by num_backslashes backslashes, then ""
    src = '{{' + chr(92) * num_backslashes + '""'
    # Evaluate as f-string
    result = eval("f'''" + src + "'''")
    print(f'{num_backslashes} backslashes in source:')
    print(f'  source bytes: {src.encode("utf-8").hex()}')
    print(f'  result repr: {repr(result)}')
    print(f'  result bytes: {result.encode("utf-8").hex()}')
    print()

