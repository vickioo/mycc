import os
import sys

def add_config(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    with open(file_path, "r") as f:
        content = f.read()

    new_block = """
# Surface via Victory/SJLL Jump Link
Host surface-sjll
        HostName 192.168.1.5
        User vicki
        Port 8822
        ProxyJump victory-sjll
        IdentityFile ~/.ssh/id_ed25519
        IdentityFile ~/.ssh/id_ed25519_vi
        StrictHostKeyChecking no
        UserKnownHostsFile /dev/null
        LogLevel ERROR
"""
    if "Host surface-sjll" not in content:
        with open(file_path, "a") as f:
            f.write("\n" + new_block)
        print(f"Successfully added 'surface-sjll' to {file_path}")
    else:
        print(f"'surface-sjll' already exists in {file_path}")

if __name__ == "__main__":
    add_config(sys.argv[1])
