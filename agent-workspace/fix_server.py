import re

with open('C:/agent-workspace/c2_server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: return offset as string in upload_init
content = content.replace(
    "return jsonify({'status': 'ok', 'offset': offset})",
    "return jsonify({'status': 'ok', 'offset': str(offset)})"
)

# Fix 2: upload_chunk seek-based writing
old_chunk = '''        mode = 'ab' if offset > 0 else 'wb'
        with open(filepath, mode) as f:
            f.write(chunk)

        upload['received'] = offset + len(chunk)
        if upload['received'] >= upload['total_size']:
            upload['status'] = 'completed'\n'''

new_chunk = '''        if not filepath.exists():
            filepath.write_bytes(b'')
        with open(filepath, 'r+b') as f:
            f.seek(offset)
            f.write(chunk)
            if offset + len(chunk) >= upload['total_size']:
                f.truncate(offset + len(chunk))

        upload['received'] = max(upload['received'], offset + len(chunk))
        if upload['received'] >= upload['total_size']:
            upload['status'] = 'completed'\n'''

content = content.replace(old_chunk, new_chunk)

with open('C:/agent-workspace/c2_server.py', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print('c2_server.py fixed')

