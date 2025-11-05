# UK Coastal Walk Tracker

A Python project to track and visualise coastal walks around the UK.

This tool allows you to log GPX walks, generate a map of the coastline you’ve walked, calculate distances, and see your progress as a fraction of the total UK coastline.

## Features

- Automatically detects new GPX files and updates `walks.yaml`.  
- Generates interactive **Folium maps** showing walked sections.  
- Calculates total distance walked and fraction of UK coastline completed.  
- Supports journaling for each walk in Markdown (`journals/`).  
- Highlights newly added walks on the map for easy identification.

## How to Use This

1. Fork this repo.

2. Place your GPX files in the `gpx` folder following the naming convention:

    `[start]-to-[destination].gpx`
    
    Example: s-queensferry-to-boness.gpx

2. Run the map generator.

    `python scripts/generate_map.py`

    New GPX files will automatically be added to `walks.yaml`. 
     
    > NOTE: If you delete a `gpx` file, you must manually remove the entry from `walks.yaml`.

    Journal files are automatically created in the `journals` folder.

3. Add `region` keys to `data/toc.yml`, and organise the files.

4. Verify the output. 

    To verify locally, navigate to the root folder on CLI and run `python -m http.server 8000`, then open http://localhost:8000.

## Output

The map is saved in the `map/` folder.

[View Map](https://twotogether.github.io/uk-coast-walk-tracker/map/index.html)
