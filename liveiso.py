import os, shutil, sys, subprocess, hashlib

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
DISKENV = ""
IN_CHROOT = False 

class ShellBuiltins:
    def append(f, *a): file = open(f, "a"); file.write(' '.join(a)); file.close()
    def cat(f): file = open(f, "r"); print(file.read()); file.close()
    def ls(d="."): return os.listdir(d)
    def cd(d=SCRIPT_PATH): os.chdir(SCRIPT_PATH) if d in ["~"] else os.chdir(d); print(d)
    def inchroot(): print(IN_CHROOT)
    def pwd(): print(os.getcwd())
    def clear(): os.system("clear") if os.name != "nt" else os.system("cls")
    def exit(): sys.exit()
    
class ISOUtils:
    # binaries that would be seperate files are here
    def mkdir(n): os.makedirs(n, exist_ok=True)
    def rmdir(n): os.removedirs(n)
    def touch(f): file = open(f, "w"); file.close()
    def rmforce(f): shutil.rmtree(f)
    def rm(f): os.remove(f) 
    def chpasswd(pw): file = open(os.path.join(SCRIPT_PATH, "etc", "shadow"), "w"); file.write(hashlib.sha256(pw.encode()).hexdigest()); file.close()

    def chroot(p):
        ISOUtils.chdisk(p)
        subprocess.run([sys.executable, os.path.join(DISKENV, "inos3.py")], env={**os.environ, "RUNNING_AS_SUBPROCESS": "1"})

    def rmdisk(p):
        if input(f"Are you sure you want to remove disk {p}? [y/N] ").lower() in ["y", "yes"]:
            ISOUtils.rmforce(p)

    def chdisk(p):
        global DISKENV
        DISKENV = p

    def mkdisk(p):
        current = os.getcwd()
        ISOUtils.mkdir(p)
        ShellBuiltins.cd(p)
        ISOUtils.mkdir("home")
        ISOUtils.mkdir("etc")
        ISOUtils.mkdir("mnt")
        ISOUtils.mkdir("tmp")
        ISOUtils.mkdir("bin")
        ISOUtils.mkdir("boot")
        ShellBuiltins.cd(current)
        ISOUtils.chdisk(p)

    def ipkg(c, *a):
        if c == "install":
            for pkg in a:
                os.system(f"curl -L https://raw.githubusercontent.com/Typhoonz0/ossim-test/refs/heads/main/{pkg}.py -o {DISKENV}/{pkg}.py")
                if pkg == "base": subprocess.run([sys.executable, os.path.join(DISKENV, "base.py")], env={**os.environ, "RUNNING_AS_SUBPROCESS": "1"})
        elif c == "uninstall":
            for pkg in a:
                ISOUtils.rm(os.path.join(DISKENV, f"{pkg}.py"))

class LiveEnviroment:
    @staticmethod
    def main():
        ShellBuiltins.cd(SCRIPT_PATH)
        while True:
            try:
                line = input("[live-env]$ ").split()
                if not line: continue
                cmd, *args = line
                f = getattr(ShellBuiltins, cmd, None) or getattr(ISOUtils, cmd, None)

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

LiveEnviroment.main()
