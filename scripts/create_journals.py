from pathlib import Path
import yaml
import json

def create_journals():
    """
    Creates Markdown journal files for each walk in walks.yaml.
    - Only creates missing files.
    - Each file contains a title, a template Route table, and Notes section.
    - Generates journals/index.json for GitHub Pages.
    """
    BASE_DIR = Path(__file__).resolve().parent.parent
    WALKS_YAML = BASE_DIR / "data" / "walks.yaml"
    JOURNALS_DIR = BASE_DIR / "docs" / "journals"
    JOURNALS_DIR.mkdir(exist_ok=True)

    if not WALKS_YAML.exists():
        print("⚠️ walks.yaml not found.")
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

        if not md_path.exists():
            template = f"""# {name}

## Route

| Section Walked  | Distance | Date |
| --------------- | -------- | ---- |
| Start to Destination | X km | DD/MM/YYYY |

## Notes

- Add walk notes, photos, or links to reports here.
- Example: See photos and read the walk report for the Burntisland to Aberdour section [here](https://two-together.com/burntisland-to-aberdour-walk/).
"""
            md_path.write_text(template, encoding="utf-8")
            new_files.append(md_filename)

    # Update index.json
    md_files = [f.name for f in JOURNALS_DIR.glob("*.md")]
    with open(JOURNALS_DIR / "index.json", "w", encoding="utf-8") as f:
        json.dump(md_files, f, indent=2)

    print(f"📁 journals/index.json updated with {len(md_files)} entries.")
    if new_files:
        print(f"📝 Created {len(new_files)} new journal file(s): {', '.join(new_files)}")

if __name__ == "__main__":
    create_journals()
