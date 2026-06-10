# Test simple patterns
patterns = [
    "f'''{{\\\\\\""'''",
    "f'''{{\\\\\\"'''",
    "f'''{{\\\\\\\"'''",
]
for p in patterns:
    print(f'pattern: {p}')
    result = eval(p)
    print(f'  repr: {repr(result)}')
    print(f'  bytes: {result.encode("utf-8").hex()}')
    print()

