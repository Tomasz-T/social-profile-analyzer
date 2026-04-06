# /// script
# requires-python = ">=3.10"
# ///
"""Strip private content from a social media data export.

Creates a copy of the export with private data removed.
Never modifies the original.

Usage:
    uv run strip_private.py /path/to/export                    # strip message content only (keep metadata)
    uv run strip_private.py /path/to/export --remove-messages  # remove message folders entirely
    uv run strip_private.py /path/to/export --remove-search    # also remove search history
    uv run strip_private.py /path/to/export --remove-messages --remove-search
    uv run strip_private.py /path/to/export --dry-run          # show what would be removed
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path


# Folders to remove entirely with --remove-messages
MESSAGE_FOLDERS = [
    "**/messages/inbox",
    "**/messages/filtered_threads",
    "**/messages/message_requests",
]

# Files to remove with --remove-search
SEARCH_FILES = [
    "**/your_search_history.json",
    "**/search_history.json",
]


def find_matching_paths(root: Path, patterns: list[str]) -> list[Path]:
    """Find all paths matching glob patterns under root."""
    found = []
    for pattern in patterns:
        found.extend(root.glob(pattern))
    return sorted(set(found))


def dir_size(path: Path) -> int:
    """Total size of a directory in bytes."""
    total = 0
    for f in path.rglob("*"):
        if f.is_file():
            total += f.stat().st_size
    return total


def fmt_size(nbytes: int) -> str:
    """Format bytes as human-readable."""
    for unit in ("B", "KB", "MB", "GB"):
        if nbytes < 1024:
            return f"{nbytes:.1f} {unit}"
        nbytes /= 1024
    return f"{nbytes:.1f} TB"


def strip_message_content(msg_folder: Path, dry_run: bool) -> tuple[int, int]:
    """Replace message text with '[removed]' but keep metadata (participants, timestamps, sender).
    Returns (files_processed, messages_stripped)."""
    files_processed = 0
    messages_stripped = 0

    for json_file in sorted(msg_folder.rglob("message_*.json")):
        if dry_run:
            files_processed += 1
            continue

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for msg in data.get("messages", []):
            if "content" in msg:
                msg["content"] = "[removed]"
                messages_stripped += 1
            # remove media references
            msg.pop("photos", None)
            msg.pop("videos", None)
            msg.pop("audio_files", None)
            msg.pop("files", None)
            msg.pop("gifs", None)
            msg.pop("sticker", None)
            msg.pop("share", None)

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        files_processed += 1

    return files_processed, messages_stripped


def main():
    parser = argparse.ArgumentParser(
        description="Strip private content from a social media data export"
    )
    parser.add_argument("export_path", type=Path, help="Path to the export folder")
    parser.add_argument(
        "--remove-messages",
        action="store_true",
        help="Remove message folders entirely (default: strip content but keep metadata)",
    )
    parser.add_argument(
        "--remove-search",
        action="store_true",
        help="Also remove search history files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be removed without doing it",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output path for stripped copy (default: {export_path}-stripped)",
    )
    args = parser.parse_args()

    src = args.export_path.resolve()
    if not src.is_dir():
        print(f"Error: {src} is not a directory", file=sys.stderr)
        sys.exit(1)

    dst = (args.output or Path(f"{src}-stripped")).resolve()

    if dst.exists():
        print(f"Error: {dst} already exists. Remove it first or use --output.", file=sys.stderr)
        sys.exit(1)

    # Copy
    print(f"Source:  {src}")
    print(f"Output:  {dst}")
    print(f"Mode:    {'dry run' if args.dry_run else 'live'}")
    print()

    if not args.dry_run:
        print("Copying export... ", end="", flush=True)
        shutil.copytree(src, dst)
        print("done")
    else:
        print("[dry run] Would copy to:", dst)

    target = dst if not args.dry_run else src
    removed_bytes = 0
    actions = []

    # Handle messages
    msg_paths = find_matching_paths(target, MESSAGE_FOLDERS)

    if args.remove_messages:
        # Remove entire folders
        for p in msg_paths:
            if p.is_dir():
                size = dir_size(p)
                removed_bytes += size
                actions.append(f"  REMOVE {p.relative_to(target)}/ ({fmt_size(size)})")
                if not args.dry_run:
                    shutil.rmtree(p)
    else:
        # Strip content but keep structure
        for p in msg_paths:
            if p.is_dir():
                files, msgs = strip_message_content(p, args.dry_run)
                actions.append(
                    f"  STRIP  {p.relative_to(target)}/ ({files} files, {msgs} messages)"
                )

        # Also remove media from message folders
        media_patterns = [
            "**/messages/inbox/*/photos",
            "**/messages/inbox/*/videos",
            "**/messages/inbox/*/gifs",
            "**/messages/inbox/*/files",
            "**/messages/inbox/*/audio",
        ]
        media_paths = find_matching_paths(target, media_patterns)
        for p in media_paths:
            if p.is_dir():
                size = dir_size(p)
                removed_bytes += size
                actions.append(f"  REMOVE {p.relative_to(target)}/ ({fmt_size(size)})")
                if not args.dry_run:
                    shutil.rmtree(p)

    # Handle search history
    if args.remove_search:
        search_paths = find_matching_paths(target, SEARCH_FILES)
        for p in search_paths:
            if p.is_file():
                size = p.stat().st_size
                removed_bytes += size
                actions.append(f"  REMOVE {p.relative_to(target)} ({fmt_size(size)})")
                if not args.dry_run:
                    p.unlink()

    # Report
    print()
    if actions:
        print("Actions:")
        for a in actions:
            print(a)
        print()
        print(f"Space reclaimed: {fmt_size(removed_bytes)}")
    else:
        print("Nothing to remove.")

    if not args.dry_run and not args.remove_messages:
        print()
        print("Message metadata preserved (participants, timestamps, sender names).")
        print("Message text replaced with '[removed]'. Media files deleted.")

    if args.dry_run:
        print()
        print("[dry run] No changes made.")


if __name__ == "__main__":
    main()
