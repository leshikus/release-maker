import subprocess
import tempfile
import time


def git(*args, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def make_release():
    git("submodule", "update", "--init", "--remote", "release-descriptor")
    git("reset", "--hard", cwd="release-descriptor")
    last_sha = git("rev-parse", "HEAD", cwd="release-descriptor")
    with open("release-descriptor/version") as f:
        a, _ = f.read().split()
    with open("release-descriptor/version", "w") as f:
        f.write(f"{int(a) + 1} {last_sha}\n")
    git("add", "version", cwd="release-descriptor")
    git("-c", "user.name=Alexei Fedotov", "-c", "user.email=alexei.fedotov@gmail.com",
        "commit", "-m", f"release {int(a) + 1}", cwd="release-descriptor")
    git("push", "origin", "HEAD:master", cwd="release-descriptor")
    print(f"create release version {int(a) + 1} {last_sha}")


def dev_build():
    with tempfile.TemporaryDirectory() as tmp:
        git("clone", "https://github.com/leshikus/release-descriptor.git", tmp)
        with open(f"{tmp}/version") as f:
            print(f"build in dev env version {f.read()}", end="")


if __name__ == "__main__":
    while True:
        make_release()
        dev_build()
        time.sleep(1)
