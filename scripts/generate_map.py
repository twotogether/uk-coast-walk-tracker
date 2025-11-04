import yaml
import folium
import gpxpy
from pathlib import Path
from geopy.distance import geodesic

# --- Setup paths ---
BASE_DIR = Path(__file__).resolve().parent.parent  # project root
GPX_COAST_DIR = BASE_DIR / "gpx"
WALKS_YAML = BASE_DIR / "data" / "walks.yaml"
MAP_DIR = BASE_DIR / "map"

# --- Helper functions ---
def path_length(coords):
    """Compute length of a path in kilometers."""
    total = 0.0
    for i in range(1, len(coords)):
        total += geodesic(coords[i-1], coords[i]).kilometers
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

    # Normalize existing gpx paths for comparison
    existing_gpx = {str(Path(walk["gpx"]).as_posix()) for walk in data["walks"]}
    new_walks_added = []

    for gpx_file in GPX_COAST_DIR.glob("*.gpx"):
        relative_path = str(gpx_file.relative_to(BASE_DIR).as_posix())
        if relative_path not in existing_gpx:
            # Generate walk name from filename
            name = gpx_file.stem.replace("-", " ").replace(" to ", " to ").title()
            journal_path = Path("journals") / (gpx_file.stem + ".md")

            new_walk = {
                "name": name,
                "gpx": relative_path,
                "journal": str(journal_path)
            }
            data["walks"].append(new_walk)
            new_walks_added.append(new_walk)

    # Save updated YAML if any new walks were added
    if new_walks_added:
        with open(WALKS_YAML, "w", encoding="utf-8") as f:
            yaml.dump(data, f, sort_keys=False)
        print(f"\n✅ walks.yml updated with {len(new_walks_added)} new coastal GPX file(s).")
    else:
        print("\nℹ️ No new coastal GPX files found.")

    return new_walks_added

# --- Step 1: Update walks.yml ---
new_walks = update_coastal_walks()

# --- Step 1b: Create journal Markdown files for any new walks ---
from create_journals import create_journals
create_journals()

# --- Step 1c: Generate or update TOC ---
from create_toc import create_toc
create_toc()  # <-- This will update toc.yml based on the journals folder

# --- Step 2: Load all walks ---
with open(WALKS_YAML, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

# --- Step 3: Initialize map ---
m = folium.Map(location=[54.5, -3.0], zoom_start=6, tiles="OpenStreetMap")
total_walked_km = 0.0

# --- Step 4: Parse GPX walks ---
for walk in data.get("walks", []):
    name = walk["name"]
    journal = walk.get("journal", "")
    coords = []

    # GPX file
    if "gpx" in walk:
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

        # Correct site-relative link
        journal_url = "/" + str(Path(journal).as_posix())
        popup_html = f"<b>{name}</b><br><a href='{journal_url}' target='_blank'>View Journal</a>"

        # Highlight newly added walks in green, existing walks in blue
        color = "green" if walk in new_walks else "blue"
        folium.PolyLine(coords, color=color, weight=4, popup=popup_html).add_to(m)
        print(f"✅ Added: {name} — {walked_km:.2f} km")
    else:
        print(f"⚠️  No coordinates found for: {name}")

# --- Step 5: Fraction of coastline walked ---
UK_COASTLINE_KM = 19000  # rough estimate
fraction_covered = total_walked_km / UK_COASTLINE_KM
print(f"\n🌊 Total distance walked: {total_walked_km:.2f} km")
print(f"🌊 Fraction of UK coastline walked: {fraction_covered:.2%}")

# --- Step 6: Save map ---
MAP_DIR.mkdir(exist_ok=True)
m.save(MAP_DIR / "index.html")
print(f"\n✅ Map saved to {MAP_DIR / 'index.html'}")

# --- Step 7: List only newly added GPX files ---
if new_walks:
    print("\n🆕 Newly added GPX walks this run:")
    for w in new_walks:
        print(f" - {w['gpx']}")
