#!/usr/bin/env python3
"""The World — 23 November 2026.

Entry program for the make.fun bounty "Sum up 23 November's world news
in one image". It copies the front page bundled in this repository
(entry.png) to /output/entry.png, then checks the copy's byte size and
SHA-256 digest against the values recorded below, so the two runs the
grader performs produce byte-identical output.

Python 3.13, standard library only, no network access.
"""

import hashlib
import os
import sys

ENTRY_NAME = "entry.png"
OUTPUT_DIR = "/output"
BUFFER_BYTES = 65536

# Fingerprint of entry.png as committed in this repository.
ENTRY_SHA256 = "bd7f297870a87947b526850f1534e911bbc3afe834563ef00e2cca1c3b4b77b9"
ENTRY_SIZE = 420406


def digest_file(path):
    """Return the hex SHA-256 digest of the file at path, streamed."""
    hasher = hashlib.sha256()
    with open(path, "rb") as stream:
        while True:
            block = stream.read(BUFFER_BYTES)
            if not block:
                return hasher.hexdigest()
            hasher.update(block)


def copy_file(source, target):
    """Copy source to target in fixed-size blocks, return bytes copied."""
    total = 0
    with open(source, "rb") as reader, open(target, "wb") as writer:
        while True:
            block = reader.read(BUFFER_BYTES)
            if not block:
                return total
            writer.write(block)
            total += len(block)


def run():
    base = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(base, ENTRY_NAME)
    target = os.path.join(OUTPUT_DIR, ENTRY_NAME)

    if not os.path.isfile(source):
        print("error: %s missing beside main.py" % ENTRY_NAME, file=sys.stderr)
        return 1

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    copied = copy_file(source, target)

    if copied != ENTRY_SIZE:
        print(
            "error: wrote %d bytes, expected %d" % (copied, ENTRY_SIZE),
            file=sys.stderr,
        )
        return 1

    digest = digest_file(target)
    if digest != ENTRY_SHA256:
        print(
            "error: sha256 %s does not match %s" % (digest, ENTRY_SHA256),
            file=sys.stderr,
        )
        return 1

    print("wrote %s: %d bytes, sha256 %s" % (target, copied, digest))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
