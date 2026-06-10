# Test patterns by constructing them programmatically
patterns = [
    '{{\\\\\\""',   # {{\\""
    '{{\\\\\\"',    # {{\\"
    '{{\\\\\\\\\\""', # {{\\\\\\""
]
for src in patterns:
    print(f'source repr: {repr(src)}')
    result = eval(f"f'''{src}'''")
    print(f'result repr: {repr(result)}')
    print(f'result bytes: {result.encode("utf-8").hex()}')
    print()

