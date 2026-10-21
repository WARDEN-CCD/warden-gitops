"""digest-only guard (ADR-013, threat T12).

A promotion-bot PR may change exactly one line: the digest of the service's own image in
apps/<svc>/rollout.yaml. Anything else fails. Non-bot PRs pass (they get human review instead).

Env: PR_AUTHOR, BOT_LOGIN, BASE_SHA, ORG. Expects the PR head at refs/remotes/pr/head.
"""

import os
import re
import subprocess
import sys

HEAD = "refs/remotes/pr/head"
PATH_RE = re.compile(r"^apps/([a-z0-9-]+)/rollout\.yaml$")
IMAGE_LINE_RE = re.compile(r"^(?P<prefix>\s*image:\s*)(?P<name>[^@\s]+)@sha256:(?P<digest>[0-9a-f]{64})\s*$")


def git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def fail(msg: str) -> int:
    print(f"digest-only: FAIL - {msg}")
    return 1


def main() -> int:
    if os.environ["PR_AUTHOR"] != os.environ["BOT_LOGIN"]:
        print("digest-only: not a promotion-bot PR; normal review rules apply")
        return 0

    base = os.environ["BASE_SHA"]
    files = [f for f in git("diff", "--name-only", f"{base}...{HEAD}").splitlines() if f]
    if len(files) != 1:
        return fail(f"bot PR must change exactly one file, changed {len(files)}: {files}")
    m = PATH_RE.match(files[0])
    if not m:
        return fail(f"bot PR may only change apps/<svc>/rollout.yaml, changed {files[0]}")
    svc = m.group(1)

    removed, added = [], []
    for line in git("diff", "--unified=0", f"{base}...{HEAD}", "--", files[0]).splitlines():
        if line.startswith("---") or line.startswith("+++"):
            continue
        if line.startswith("-"):
            removed.append(line[1:])
        elif line.startswith("+"):
            added.append(line[1:])
    if len(removed) != 1 or len(added) != 1:
        return fail(f"expected one line replaced, got -{len(removed)} +{len(added)}")

    old, new = IMAGE_LINE_RE.match(removed[0]), IMAGE_LINE_RE.match(added[0])
    if not old or not new:
        return fail("changed line is not an `image: name@sha256:<digest>` line")
    if old.group("prefix") != new.group("prefix") or old.group("name") != new.group("name"):
        return fail("only the digest may change, not the image name or indentation")
    expected = f"ghcr.io/{os.environ['ORG'].lower()}/svc-{svc}"
    if new.group("name") != expected:
        return fail(f"image {new.group('name')} is not this service's image ({expected})")

    print(f"digest-only: OK - {svc}: {old.group('digest')[:12]} -> {new.group('digest')[:12]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
