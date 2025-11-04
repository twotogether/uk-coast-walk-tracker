# create_toc.py
from pathlib import Path
import yaml

def create_toc():
    BASE_DIR = Path(__file__).resolve().parent.parent
    JOURNALS_DIR = BASE_DIR / "journals"
    TOC_YML = BASE_DIR / "data" / "toc.yml"

    # Create data folder if it doesn't exist
    TOC_YML.parent.mkdir(exist_ok=True)

    # Load existing toc.yml if it exists
    if TOC_YML.exists():
        with open(TOC_YML, "r", encoding="utf-8") as f:
            toc_data = yaml.safe_load(f) or {"All Walk Sections": []}
    else:
        toc_data = {"All Walk Sections": []}

    # Build a set of existing walk names for fast lookup
    existing_walks = set()
    for region_block in toc_data["All Walk Sections"]:
        existing_walks.update(region_block.get("walks", []))

    # Scan markdown files
    md_files = sorted(JOURNALS_DIR.glob("*.md"))

    DEFAULT_REGION = "Unknown"
    new_walks_count = 0

    # Ensure there is a block for the default region
    region_block = next((r for r in toc_data["All Walk Sections"] if r["region"] == DEFAULT_REGION), None)
    if not region_block:
        region_block = {"region": DEFAULT_REGION, "walks": []}
        toc_data["All Walk Sections"].append(region_block)

    # Add new walks
    for md_file in md_files:
        if md_file.name.lower() == "index.json":
            continue  # skip JSON index
        stem = md_file.stem
        walk_name = stem.replace("-", " ").title()

        if walk_name not in existing_walks:
            region_block["walks"].append(walk_name)
            existing_walks.add(walk_name)
            new_walks_count += 1
            print(f"➕ Appended new walk to TOC: {walk_name}")

    # Sort walks alphabetically within each region
    for region_block in toc_data["All Walk Sections"]:
        region_block["walks"] = sorted(region_block.get("walks", []), key=lambda w: w.lower())

    # Sort regions alphabetically
    toc_data["All Walk Sections"] = sorted(toc_data["All Walk Sections"], key=lambda r: r["region"].lower())

    # Write toc.yml
    with open(TOC_YML, "w", encoding="utf-8") as f:
        yaml.dump(toc_data, f, sort_keys=False)

    print(f"\n✅ toc.yml updated. {new_walks_count} new walk(s) added.")
    print("✅ Regions and walks sorted alphabetically.")

if __name__ == "__main__":
    create_toc()
