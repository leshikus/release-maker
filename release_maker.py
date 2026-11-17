import subprocess
import tempfile
import time

URL = "https://github.com/leshikus/release-descriptor.git"
SUBMODULE = "release-descriptor"


def git(*args, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def make_release():
    git("submodule", "update", "--init", "--remote", SUBMODULE)
    last_sha = git("rev-parse", "HEAD", cwd=SUBMODULE)
    with open(f"{SUBMODULE}/version") as f:
        a, _ = f.read().split()
    with open(f"{SUBMODULE}/version", "w") as f:
        f.write(f"{int(a) + 1} {last_sha}\n")
    git("add", "version", cwd=SUBMODULE)
    git("-c", "user.name=Alexei Fedotov", "-c", "user.email=alexei.fedotov@gmail.com",
        "commit", "-m", f"release {int(a) + 1}", cwd=SUBMODULE)
    git("push", "origin", "HEAD:master", cwd=SUBMODULE)
    print(f"create release version {int(a) + 1} {last_sha}")


def dev_build():
    with tempfile.TemporaryDirectory() as tmp:
        git("clone", URL, tmp)
        with open(f"{tmp}/version") as f:
            print(f"build in dev env version {f.read()}", end="")


if __name__ == "__main__":
    while True:
        make_release()
        dev_build()
        time.sleep(60)
