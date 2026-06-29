#!/usr/bin/env python3
"""Scaffold a new Quarto blog post under blog/posts/<slug>/index.qmd.

Usage:
    python scripts/newpost.py "My Post Title" -d "A short summary" -c python,notes
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

POSTS_DIR = Path(__file__).resolve().parent.parent / "blog" / "posts"


def slugify(title):
    """Turn a title into a filesystem/URL-friendly slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug


def parse_categories(raw):
    """Split a comma-separated category string into a clean list."""
    return [c.strip() for c in raw.split(",") if c.strip()]


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("title", help="Post title")
    parser.add_argument("-d", "--description", default="",
                        help="One-line summary shown in the blog listing")
    parser.add_argument("-c", "--category", default="python",
                        help="Comma-separated categories (default: python)")
    args = parser.parse_args()

    slug = slugify(args.title)
    if not slug:
        sys.exit("Error: title produced an empty slug; please use a title with letters or digits.")

    post_dir = POSTS_DIR / slug
    if post_dir.exists():
        sys.exit(f"Error: {post_dir} already exists; refusing to overwrite.")

    categories = parse_categories(args.category)
    post_dir.mkdir(parents=True)
    index = post_dir / "index.qmd"
    index.write_text(
        f'---\n'
        f'title: "{args.title}"\n'
        f'description: "{args.description}"\n'
        f'date: "{date.today().isoformat()}"\n'
        f'categories: [{", ".join(categories)}]\n'
        f'---\n'
        f'\n'
        f'Write your post here.\n'
    )

    print(f"Created {index}")


if __name__ == "__main__":
    main()
