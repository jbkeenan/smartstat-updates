import os
import subprocess
import shutil

REPOS = {
    "frontend": "https://x-access-token:{token}@github.com/jbkeenan/smartstatfront.git",
    "backend": "https://x-access-token:{token}@github.com/jbkeenan/smartstatback.git",
}

BRANCH = "main"
GH_TOKEN = os.environ.get("GH_TOKEN")
TARGET_DIR = "/tmp/smartstatdeploy"

def run(cmd, cwd=None):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True, cwd=cwd)

for folder in ("frontend", "backend"):
    path = os.path.join("extracted", folder)
    if os.path.isdir(path):
        repo_url = REPOS[folder].format(token=GH_TOKEN)
        target = os.path.join(TARGET_DIR, folder)

        print(f"\n--- Updating {folder} ---")
        run(f"git clone --branch {BRANCH} {repo_url} {target}")
        run(f"rm -rf {target}/*")
        run(f"cp -r {path}/* {target}/")
        run("git add .", cwd=target)
        run('git commit -m "Automated deploy from smartstat-updates ZIP"', cwd=target)
        run("git push", cwd=target)
