# commiting in progress liveenv just to check

import os, shutil, sys

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

class ShellBuiltins:
    def mkdir(n): os.makedirs(n, exist_ok=True)
    def rmdir(n): os.removedirs(n)
    def touch(f): open(f, "w").close()
    def rm(f): shutil.rmtree(f)
    def ls(d="."): return os.listdir(d)
    def cd(d=SCRIPT_PATH): os.chdir(SCRIPT_PATH) if d in ["", "~"] else os.chdir(d) 
    def pwd(): print(os.getcwd())
    def clear(): os.system("clear") if os.name != "nt" else os.system("cls")
    def exit(): sys.exit()

class ISOUtils:
    def mkdisk(p): 
        ShellBuiltins.mkdir(p)

    def ipkg(c, *a):
        if c == "install":
            for pkg in a:
                os.system("git clone") 

class LiveEnviroment:
    @staticmethod
    def main():
        while True:
            try:
                line = input("[live-env]$ ").split()
                if not line: continue
                cmd, *args = line
                f = getattr(ShellBuiltins, cmd, None) or getattr(ISOUtils, cmd, None)
                if not f:
                    print(f"Command not found: {cmd}")
                    continue

                def conv(x):
                    if x.lower() == "true": return True
                    if x.lower() == "false": return False
                    if x.isdigit(): return int(x)
                    return x

                args = [conv(a) for a in args]
                r = f(*args)
                if r is not None:
                    print('\n'.join(r) if isinstance(r, (list, tuple)) else r)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    LiveEnviroment.main()
