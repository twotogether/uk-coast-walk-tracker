import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
WALKS_YAML = BASE_DIR / "data" / "walks.yml"
COAST_GPX_FOLDER = BASE_DIR / "gpx"

# Load existing walks.yml
with open(WALKS_YAML, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f) or {}

if "walks" not in data:
    data["walks"] = []

# Set of existing gpx entries, normalised
existing_gpx = {Path(w["gpx"]).as_posix() for w in data["walks"]}
new_walks_added = False

def make_human_name(stem: str) -> str:
    """Convert filename into readable title."""
    name = stem.replace("-", " ")
    name = name.replace("  ", " ")
    # Capitalise first letter of each word but keep apostrophes correct
    return " ".join(word.capitalize() for word in name.split())

# Scan all GPX recursively
for gpx_file in COAST_GPX_FOLDER.rglob("*.gpx"):
    relative_gpx = gpx_file.relative_to(BASE_DIR).as_posix()  # POSIX
    if relative_gpx not in existing_gpx:

        # Name comes from gpx filename
        name = make_human_name(gpx_file.stem)

        # Build journal path mirroring gpx/ structure
        gpx_rel = gpx_file.relative_to(COAST_GPX_FOLDER)  # e.g. lothian/leith-to-granton.gpx
        journal_rel = Path("journals") / gpx_rel.with_suffix(".md")

        new_walk = {
            "name": name,
            "gpx": relative_gpx,
            "journal": journal_rel.as_posix()
        }

        data["walks"].append(new_walk)
        print(f"➕ Added new walk: {relative_gpx}")
        new_walks_added = True

# Save walks.yml only if modified
if new_walks_added:
    with open(WALKS_YAML, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

    print("\n✅ walks.yml updated with new coastal GPX files")
else:
    print("\nℹ️ No new coastal GPX files found")
