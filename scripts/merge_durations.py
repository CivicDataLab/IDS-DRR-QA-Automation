#!/usr/bin/env python3
"""
Merge per-shard `.test_durations` fragments into one file.

`pytest --store-durations` only records the tests that ran in *that* shard, so an
8-way split produces 8 partial files. Merging them is a plain dict update - the
node ids are disjoint by construction, since a test belongs to exactly one shard.

Tests that no longer exist are dropped: a duration file that accumulates ids
forever skews pytest-split's average, which is what it assigns to every test it
has never seen.

Usage:
    merge_durations.py --out .test_durations --collected collected.txt frag1 frag2 ...
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("fragments", nargs="+", type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument(
        "--collected",
        type=Path,
        help="File of currently-collected node ids; entries outside it are dropped.",
    )
    args = ap.parse_args()

    merged: dict[str, float] = {}
    for frag in args.fragments:
        if not frag.is_file():
            print(f"skip (missing): {frag}", file=sys.stderr)
            continue
        data = json.loads(frag.read_text() or "{}")
        merged.update(data)
        print(f"{frag}: {len(data)} entries")

    if not merged:
        print("no durations collected - refusing to write an empty file", file=sys.stderr)
        return 1

    if args.collected:
        keep = {ln.strip() for ln in args.collected.read_text().splitlines() if ln.strip()}
        dropped = [k for k in merged if k not in keep]
        for k in dropped:
            del merged[k]
        print(f"dropped {len(dropped)} entries for tests that no longer exist")
        missing = len(keep) - len(merged)
        if missing > 0:
            print(f"warning: {missing} collected tests still have no duration", file=sys.stderr)

    args.out.write_text(json.dumps(dict(sorted(merged.items())), indent=2) + "\n")
    total = sum(merged.values())
    print(f"wrote {args.out}: {len(merged)} entries, {total / 60:.1f} min total")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
