import sys
import yaml
import folium
import json
import gpxpy
from pathlib import Path
from geopy.distance import geodesic

# --- Setup paths ---
BASE_DIR = Path(__file__).resolve().parent.parent  # project root
GPX_DIR = BASE_DIR / "gpx"
WALKS_YAML = BASE_DIR / "data" / "walks.yaml"
DATA_DIR = BASE_DIR / "data"
MAP_DIR = BASE_DIR / "docs" / "_static" / "map"
JOURNALS_DIR = BASE_DIR / "docs" / "journals"

MAP_DIR.mkdir(parents=True, exist_ok=True)
JOURNALS_DIR.mkdir(parents=True, exist_ok=True)

# Make scripts importable
SCRIPTS_DIR = BASE_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
from create_journals import create_journals


# ---------------------------------
# Helper function: compute distance
# ---------------------------------
def path_length(coords):
    """Compute length of a path in kilometers."""
    total = 0.0
    for i in range(1, len(coords)):
        total += geodesic(coords[i - 1], coords[i]).kilometers
    return total


# ---------------------------------
# Step 1 — Update walks.yaml
# ---------------------------------
def update_coastal_walks():
    """Scan all GPX subfolders and update walks.yaml."""
    if not GPX_DIR.exists():
        print(f"⚠️ GPX folder does not exist: {GPX_DIR}")
        return []

    with open(WALKS_YAML, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if "walks" not in data:
        data["walks"] = []

    existing_gpx = {walk["gpx"] for walk in data["walks"]}
    new_walks_added = []

    # Recursive GPX scan
    for gpx_file in GPX_DIR.rglob("*.gpx"):
        relative_path = gpx_file.relative_to(BASE_DIR).as_posix()

        if relative_path not in existing_gpx:
            name = gpx_file.stem.replace("-", " ").title()

            # Determine region folder based on GPX subfolder
            region_folder = gpx_file.relative_to(GPX_DIR).parent.as_posix()
            journal_md = f"journals/{region_folder}/{gpx_file.stem}.md"

            new_walk = {
                "name": name,
                "gpx": relative_path,
                "journal": journal_md,
            }

            data["walks"].append(new_walk)
            new_walks_added.append(new_walk)

    # Save updates
    if new_walks_added:
        with open(WALKS_YAML, "w", encoding="utf-8") as f:
            yaml.dump(data, f, sort_keys=False)
        print(f"✅ walks.yaml updated with {len(new_walks_added)} new GPX file(s).")
    else:
        print("ℹ️ No new GPX files found.")

    return new_walks_added


new_walks = update_coastal_walks()


# ---------------------------------
# Step 2 — Generate journals
# ---------------------------------
create_journals()


# ---------------------------------
# Step 3 — Load updated YAML
# ---------------------------------
with open(WALKS_YAML, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)


# ---------------------------------
# Step 4 — Initialize map
# ---------------------------------
m = folium.Map(location=[54.5, -3.0], zoom_start=6, tiles="OpenStreetMap")

total_walked_km = 0.0
SITE_ROOT = "https://twotogether.github.io/uk-coast-walk-tracker"


# ---------------------------------
# Step 5 — Load GPX, add to map
# ---------------------------------
for walk in data.get("walks", []):
    name = walk["name"]
    coords = []

    gpx_path = BASE_DIR / walk["gpx"]

    if not gpx_path.exists():
        print(f"⚠️ Missing GPX file: {gpx_path}")
        continue

    # Parse GPX
    with open(gpx_path, "r", encoding="utf-8") as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    coords.append([point.latitude, point.longitude])

    if not coords:
        continue

    walked_km = path_length(coords)
    total_walked_km += walked_km

    # Build journal URL (Sphinx builds .html versions)
    journal_html = walk["journal"].replace(".md", ".html")
    journal_url = f"{SITE_ROOT}/{journal_html}"

    popup_html = f"<b>{name}</b><br><a href='{journal_url}' target='_blank'>View Journal</a>"

    color = "green" if walk in new_walks else "blue"

    folium.PolyLine(coords, color=color, weight=4, popup=popup_html).add_to(m)

    print(f"✅ Added: {name} — {walked_km:.2f} km")


# ---------------------------------
# Step 6 — Save Distance JSON
# ---------------------------------
UK_COASTLINE_KM = 19000
fraction_covered = total_walked_km / UK_COASTLINE_KM

distance_info = {
    "totalKm": total_walked_km,
    "fraction": fraction_covered
}

with open(DATA_DIR / "distance.json", "w", encoding="utf-8") as f:
    json.dump(distance_info, f, indent=2)

print(f"\n🌊 Walked: {total_walked_km:.2f} km")
print(f"🌊 Fraction of coastline walked: {fraction_covered:.2%}")


# ---------------------------------
# Step 7 — Save Map
# ---------------------------------
map_out = MAP_DIR / "index.html"
m.save(map_out)
print(f"\n✅ Map saved to {map_out}")


# ---------------------------------
# Summary
# ---------------------------------
if new_walks:
    print("\n🆕 Newly added GPX files:")
    for w in new_walks:
        print(f" - {w['gpx']}")
