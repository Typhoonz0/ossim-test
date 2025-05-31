import binascii, os
root = os.path.dirname(os.path.abspath(__file__))

files = {
    'mkdir': 'aW1wb3J0IG9zLCBzeXM7IG4gPSBzeXMuYXJndlsxXTsgb3MubWFrZWRpcnMobiwgZXhpc3Rfb2s9VHJ1ZSk=',
    'rmdir': 'aW1wb3J0IG9zLHN5cwpuID0gc3lzLmFyZ3ZbMV0Kb3MucmVtb3ZlZGlycyhuKSAgICAK',
    'touch': 'aW1wb3J0IHN5cwpuID0gc3lzLmFyZ3ZbMV0KZmlsZSA9IG9wZW4obiwgInciKTsgZmlsZS5jbG9zZSgp',
    'rmforce': 'aW1wb3J0IHN5cywgc2h1dGlsCm4gPSBzeXMuYXJndlsxXQpzaHV0aWwucm10cmVlKG4p',
    'rm': 'aW1wb3J0IG9zLCBzeXMKbiA9IHN5cy5hcmd2WzFdCm9zLnJlbW92ZShuKQ==',
    'chpasswd': 'aW1wb3J0IG9zLCBzeXMsIGhhc2hsaWIKcHcgPSBzeXMuYXJndlsxXQpTQ1JJUFRfUEFUSCA9IG9zLnBhdGguZGlybmFtZShvcy5wYXRoLmRpcm5hbWUob3MucGF0aC5hYnNwYXRoKF9fZmlsZV9fKSkpCmZpbGUgPSBvcGVuKG9zLnBhdGguam9pbihTQ1JJUFRfUEFUSCwgImV0YyIsICJzaGFkb3ciKSwgInciKTsgZmlsZS53cml0ZShoYXNobGliLnNoYTI1Nihwdy5lbmNvZGUoKSkuaGV4ZGlnZXN0KCkpOyBmaWxlLmNsb3NlKCk=='
}

for file_name, hex_content in files.items():
    decoded_content = binascii.a2b_base64(hex_content).decode()
    with open(os.path.join(root, "bin", f"{file_name}.py"), "w") as file:
        file.write(decoded_content)
        file.flush()

print(f"Files have been written to {root}")
