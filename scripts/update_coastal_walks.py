import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
WALKS_YAML = BASE_DIR / "data" / "walks.yml"
COAST_GPX_FOLDER = BASE_DIR / "gpx"

# Load existing walks.yml
with open(WALKS_YAML, "r") as f:
    data = yaml.safe_load(f)

if "walks" not in data:
    data["walks"] = []

existing_gpx = {walk["gpx"] for walk in data["walks"]}
new_walks_added = False

# Scan coastal GPX folder
for gpx_file in COAST_GPX_FOLDER.glob("*.gpx"):
    relative_path = str(gpx_file.relative_to(BASE_DIR))
    if relative_path not in existing_gpx:
        # Generate name from filename: s-queensferry-to-boness.gpx -> S Queensferry to Boness
        name = gpx_file.stem.replace("-", " ").replace(" to ", " to ").title()
        
        # Generate journal filename
        journal_path = Path("journals") / (gpx_file.stem + ".md")
        
        # Create new walk entry
        new_walk = {
            "name": name,
            "gpx": relative_path,
            "journal": str(journal_path)
        }
        data["walks"].append(new_walk)
        print(f"➕ Added new walk: {relative_path}")
        new_walks_added = True

# Save updated YAML if any new walks were added
if new_walks_added:
    with open(WALKS_YAML, "w") as f:
        yaml.dump(data, f, sort_keys=False)
    print("\n✅ walks.yml updated with new coastal GPX files")
else:
    print("\nℹ️ No new coastal GPX files found")
