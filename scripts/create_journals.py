from pathlib import Path
import yaml
import json

def create_journals():
    """
    Creates Markdown journal files for each walk in walks.yaml.
    - Only creates missing files.
    - Does NOT overwrite or modify existing ones.
    - Also generates journals/index.json for GitHub Pages.
    """
    BASE_DIR = Path(__file__).resolve().parent.parent
    WALKS_YAML = BASE_DIR / "data" / "walks.yaml"
    JOURNALS_DIR = BASE_DIR / "journals"

    JOURNALS_DIR.mkdir(exist_ok=True)

    if not WALKS_YAML.exists():
        print("⚠️  walks.yaml not found.")
        return

    with open(WALKS_YAML, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    new_files = []

    for walk in data.get("walks", []):
        gpx_path = Path(walk.get("gpx", ""))
        if not gpx_path:
            continue

        name = walk.get("name", gpx_path.stem.replace("-", " ").title())
        md_filename = gpx_path.stem + ".md"
        md_path = JOURNALS_DIR / md_filename

        # Markdown template
        md_template = (
f"# {name}\n\n"
"## Route\n\n"
"| Section Walked   | Distance | Date |\n"
"| -------- | ------- | ---- |\n"
"|   |    | \n"
"|   |    | \n\n"
"## Notes\n"
        )

        # Create only if it doesn’t exist
        if not md_path.exists():
            md_path.write_text(md_template, encoding="utf-8")
            new_files.append(md_filename)

    # --- Create JSON index for GitHub Pages ---
    md_files = [f.name for f in JOURNALS_DIR.glob("*.md")]
    index_file = JOURNALS_DIR / "index.json"
    index_file.write_text(json.dumps(md_files, indent=2), encoding="utf-8")

    print(f"📁 journals/index.json updated with {len(md_files)} entries.")

    if new_files:
        print(f"📝 Created {len(new_files)} new journal file(s):")
        for f in new_files:
            print(f"   - {f}")
    else:
        print("\nℹ️ No new journal files created (all exist already).")

# Run automatically when imported in your main script
if __name__ == "__main__":
    create_journals()
