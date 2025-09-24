import subprocess
import shutil
import os
import sys

# -------- Utility to run shell commands --------
def run_command(cmd, cwd=None):
    try:
        print(f"> Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=cwd, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {' '.join(cmd)}")
        print(e.stderr)
        sys.exit(1)
        
def git_checkout(repo_dir, default_branch, git_branch, commit_message):
    
    # stash all other changes
    run_command(["git", "stash"], cwd=repo_dir)

    # Checkout branch
    run_command(["git", "checkout", default_branch], cwd=repo_dir)

    # create a new branch
    run_command(["git", "branch", "-b", git_branch], cwd=repo_dir)


def git_push(repo_dir, default_branch, git_branch, commit_message):
        
    # -------- Step 2: Git operations --------

    # Add file
    run_command(["git", "add", "."], cwd=repo_dir)

    # Commit
    run_command(["git", "commit", "-m", commit_message], cwd=repo_dir)

    # Push
    run_command(["git", "push", "origin", git_branch], cwd=repo_dir)

    print("🚀 Deployment completed successfully.")
