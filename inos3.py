import os, sys, subprocess, hashlib

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
DISKENV = ""
IN_CHROOT = False 

class ShellBuiltins:
    def append(f, *a): file = open(f, "a"); file.write(' '.join(a)); file.close()
    def cat(f): file = open(f, "r"); print(file.read()); file.close()
    def ls(d="."): return os.listdir(d)
    def cd(d=SCRIPT_PATH): os.chdir(SCRIPT_PATH) if d in ["", "~"] else os.chdir(d) 
    def inchroot(): print(IN_CHROOT)
    def pwd(): print(os.getcwd())
    def clear(): os.system("clear") if os.name != "nt" else os.system("cls")
    def exit(): sys.exit()

class inOS3:
    def login():
        f = open(os.path.join(SCRIPT_PATH, "etc", "shadow")) 
        storedpw = f.read()
        pw = input()
        hashedpw = hashlib.sha256(pw.encode()).hexdigest()
        if storedpw == hashedpw:
            inOS3.main()
        else:
            print("Incorrect.")
            inOS3.login()

    @staticmethod
    def main():
        while True:
            ShellBuiltins.cd(SCRIPT_PATH)
            try:
                line = input("[live-env]$ ").split()
                if not line: continue
                cmd, *args = line
                f = getattr(ShellBuiltins, cmd, None)

                def conv(x):
                    if x.lower() == "true": return True
                    if x.lower() == "false": return False
                    if x.isdigit(): return int(x)
                    return x

                args = [conv(a) for a in args]

                if f:
                    r = f(*args)
                    if r is not None:
                        print('\n'.join(r) if isinstance(r, (list, tuple)) else r)
                else:
                    cmd = cmd.strip(".py")
                    path = os.path.join(SCRIPT_PATH, "bin", cmd)
                    if os.path.isfile(path+".py"):
                        subprocess.run([sys.executable, path+".py", *map(str, args)])
                    else:
                        print(f"Command not found: {cmd}")
            except Exception as e:
                print(f"Error: {e}")

if os.getenv("RUNNING_AS_SUBPROCESS") == "1":
    IN_CHROOT = True


inOS3.main()
