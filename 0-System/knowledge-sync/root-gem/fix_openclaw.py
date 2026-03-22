import sys

file_path = "/home/vicki/openclaw-start.js"
with open(file_path, "r") as f:
    content = f.read()

# 确保不重复添加
if "'gateway'" not in content:
    content = content.replace("['dist/entry.js']", "['dist/entry.js', 'gateway']")

with open(file_path, "w") as f:
    f.write(content)
