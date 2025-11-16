import json
from pathlib import Path

def create_journals():
    """
    Create missing Markdown journals and update journals/index.json.
    Only scans inside docs/journals/, respects subfolders, avoids duplicates.
    """
    BASE_DIR = Path(__file__).resolve().parent.parent
    JOURNALS_DIR = BASE_DIR / "docs" / "journals"
    JOURNALS_DIR.mkdir(parents=True, exist_ok=True)

    new_files = []

    # Recursively find all .md files inside docs/journals/
    md_files = list(JOURNALS_DIR.rglob("*.md"))

    seen = set()
    for md_file in md_files:
        # Path relative to JOURNALS_DIR
        rel_path = md_file.relative_to(JOURNALS_DIR).as_posix()
        if rel_path in seen:
            continue
        seen.add(rel_path)

        # Create template if file is empty
        if md_file.stat().st_size == 0:
            md_file.write_text(
                f"# {md_file.stem.replace('-', ' ').title()}\n\n"
                "## Route\n\n"
                "| Section Walked  | Distance | Date |\n"
                "| --------------- | ------- | ---- |\n\n"
                "## Notes\n\n"
                "- Add notes, photos, and links here.\n",
                encoding="utf-8"
            )
            new_files.append(rel_path)

    # Update index.json
    md_files_unique = sorted(seen)
    with open(JOURNALS_DIR / "index.json", "w", encoding="utf-8") as f:
        json.dump(md_files_unique, f, indent=2)

    print(f"📁 journals/index.json updated with {len(md_files_unique)} entries.")
    if new_files:
        print(f"📝 Created {len(new_files)} new journal(s): {', '.join(new_files)}")
