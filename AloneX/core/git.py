import asyncio
import os
import shlex
from typing import Tuple

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

import config
from ..logging import LOGGER


def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    return asyncio.get_event_loop().run_until_complete(install_requirements())


def git():
    """
    CRASH-PROOF git updater.
    Heroku/Render me .git nahi hota + auth prompt aata hai.
    Isliye updater fail ho to bot ko boot hone do.
    """

    REPO_LINK = getattr(config, "UPSTREAM_REPO", None)
    BRANCH = getattr(config, "UPSTREAM_BRANCH", "main")
    TOKEN = getattr(config, "GIT_TOKEN", None)

    # If repo link not set, updater disabled
    if not REPO_LINK or not isinstance(REPO_LINK, str):
        LOGGER(__name__).warning("UPSTREAM_REPO not set. Git updater disabled.")
        return

    # Build upstream repo URL (token optional)
    if TOKEN:
        try:
            git_username = REPO_LINK.split("com/")[1].split("/")[0]
            temp_repo = REPO_LINK.split("https://", 1)[1]
            upstream_repo = f"https://{git_username}:{TOKEN}@{temp_repo}"
        except Exception as e:
            LOGGER(__name__).warning(f"Failed to build token repo url: {e}")
            upstream_repo = REPO_LINK
    else:
        upstream_repo = REPO_LINK

    # Try to open repo from current working directory (safe for local/vps)
    try:
        repo = Repo(os.getcwd(), search_parent_directories=True)
        LOGGER(__name__).info("Git repository detected. Updater available.")
    except InvalidGitRepositoryError:
        # On Heroku slug there is no git repo; don't init/fetch, just skip
        LOGGER(__name__).warning("No git repo in runtime (Heroku/Render). Skipping git updater.")
        return
    except GitCommandError as e:
        LOGGER(__name__).warning(f"Git command error, skipping updater: {e}")
        return
    except Exception as e:
        LOGGER(__name__).warning(f"Git init error, skipping updater: {e}")
        return

    # Remote setup (never crash)
    try:
        if "origin" in [r.name for r in repo.remotes]:
            origin = repo.remote("origin")
        else:
            origin = repo.create_remote("origin", upstream_repo)
    except Exception as e:
        LOGGER(__name__).warning(f"Remote setup failed, skipping updater: {e}")
        return

    # Fetch/Pull (never crash; auth issues will be caught)
    try:
        origin.fetch(BRANCH)
    except GitCommandError as e:
        LOGGER(__name__).warning(f"Git fetch failed (auth/private repo?). Skipping updater: {e}")
        return
    except Exception as e:
        LOGGER(__name__).warning(f"Git fetch error, skipping updater: {e}")
        return

    try:
        # Ensure branch exists locally
        if BRANCH not in repo.heads:
            repo.create_head(BRANCH, origin.refs[BRANCH])

        repo.heads[BRANCH].set_tracking_branch(origin.refs[BRANCH])
        repo.heads[BRANCH].checkout(True)

        try:
            origin.pull(BRANCH)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")

        # Optional: install requirements after successful update
        install_req("pip3 install --no-cache-dir -r requirements.txt")
        LOGGER(__name__).info("Upstream update applied successfully.")

    except Exception as e:
        LOGGER(__name__).warning(f"Update apply failed, skipping updater: {e}")
        return
