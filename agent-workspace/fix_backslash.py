with open('C:/agent-workspace/generate_clean.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("add_null('\')", "add_null(chr(92))")
content = content.replace("enc_len('\')", "enc_len(chr(92))")

with open('C:/agent-workspace/generate_clean.py', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print('fixed')

