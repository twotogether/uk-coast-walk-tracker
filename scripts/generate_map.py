import sys
import yaml
import folium
import json
import gpxpy
from pathlib import Path
from geopy.distance import geodesic

# --- Setup paths ---
BASE_DIR = Path(__file__).resolve().parent.parent  # project root
GPX_COAST_DIR = BASE_DIR / "gpx"
WALKS_YAML = BASE_DIR / "data" / "walks.yaml"
DATA_DIR = BASE_DIR / "data"

# Updated: map inside Sphinx _static
MAP_DIR = BASE_DIR / "docs" / "map"
MAP_DIR.mkdir(parents=True, exist_ok=True)

# --- Make scripts importable ---
SCRIPTS_DIR = BASE_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
from create_journals import create_journals

# --- Helper functions ---
def path_length(coords):
    """Compute length of a path in kilometers."""
    total = 0.0
    for i in range(1, len(coords)):
        total += geodesic(coords[i - 1], coords[i]).kilometers
    return total

def update_coastal_walks():
    """Scan GPX coast folder and update walks.yml with any new GPX files."""
    if not GPX_COAST_DIR.exists():
        print(f"⚠️  GPX folder does not exist: {GPX_COAST_DIR}")
        return []

    with open(WALKS_YAML, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if "walks" not in data:
        data["walks"] = []

    existing_gpx = {str(Path(w["gpx"]).as_posix()) for w in data["walks"]}
    new_walks_added = []

    for gpx_file in GPX_COAST_DIR.glob("*.gpx"):
        relative_path = str(gpx_file.relative_to(BASE_DIR).as_posix())
        if relative_path not in existing_gpx:
            name = gpx_file.stem.replace("-", " ").title()
            journal_path = Path("docs/journals") / (gpx_file.stem + ".md")

            new_walk = {
                "name": name,
                "gpx": relative_path,
                "journal": f"journals/{gpx_file.stem}.md"  # Sphinx expects relative to docs/
            }

            data["walks"].append(new_walk)
            new_walks_added.append(new_walk)

    if new_walks_added:
        with open(WALKS_YAML, "w", encoding="utf-8") as f:
            yaml.dump(data, f, sort_keys=False)
        print(f"✅ walks.yml updated with {len(new_walks_added)} new GPX file(s).")
    else:
        print("ℹ️ No new GPX files found.")

    return new_walks_added

# --- Step 1: Update walks.yml ---
new_walks = update_coastal_walks()

# --- Step 2: Create journals ---
create_journals()

# --- Step 3: Load all walks ---
with open(WALKS_YAML, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

# --- Step 4: Initialize map ---
m = folium.Map(location=[54.5, -3.0], zoom_start=6, tiles="OpenStreetMap")
total_walked_km = 0.0

# --- Step 5: Parse GPX and add to map ---
SITE_ROOT = "https://twotogether.github.io/uk-coast-walk-tracker"

for walk in data.get("walks", []):
    name = walk["name"]
    journal = walk.get("journal", "")

    coords = []
    gpx_path = BASE_DIR / walk["gpx"]
    if gpx_path.exists():
        with open(gpx_path, "r", encoding="utf-8") as gpx_file:
            gpx = gpxpy.parse(gpx_file)
            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        coords.append([point.latitude, point.longitude])
    else:
        print(f"⚠️  GPX file not found: {gpx_path}")

    if coords:
        walked_km = path_length(coords)
        total_walked_km += walked_km

        journal_html = Path(journal).with_suffix(".html").as_posix()
        journal_url = f"{SITE_ROOT}/{journal_html}"
        popup_html = f"<b>{name}</b><br><a href='{journal_url}' target='_blank'>View Journal</a>"
        color = "green" if walk in new_walks else "blue"

        folium.PolyLine(coords, color=color, weight=4, popup=popup_html).add_to(m)
        print(f"✅ Added: {name} — {walked_km:.2f} km")

# --- Step 6: Save distance info ---
UK_COASTLINE_KM = 19000
fraction_covered = total_walked_km / UK_COASTLINE_KM

distance_info = {
    "totalKm": total_walked_km,
    "fraction": fraction_covered
}

with open(DATA_DIR / "distance.json", "w", encoding="utf-8") as f:
    json.dump(distance_info, f, indent=2)

print(f"\n🌊 Total distance walked: {total_walked_km:.2f} km")
print(f"🌊 Fraction of coastline walked: {fraction_covered:.2%}")

# --- Step 7: Save map ---
MAP_DIR.mkdir(exist_ok=True)
map_out = MAP_DIR / "index.html"
m.save(map_out)
print(f"\n✅ Map saved to {map_out}")

# --- Summary of new walks ---
if new_walks:
    print("\n🆕 Newly added GPX walks this run:")
    for w in new_walks:
        print(f" - {w['gpx']}")
