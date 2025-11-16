# UK Coastal Walk Tracker

A Python project to track and visualise coastal walks around the UK.

This tool allows you to log GPX walks, generate a map of the coastline you’ve walked, calculate distances, and see your progress as a fraction of the total UK coastline.

## Features

- Automatically detects new GPX files and updates `data/walks.yaml`.  
- Generates interactive **Folium maps** showing walked sections.  
- Calculates total distance walked and fraction of UK coastline completed.  
- Supports journaling for each walk in Markdown (`docs/journals/`).  
- Highlights newly added walks on the map for easy identification.  
- Sidebar TOC shows all walks.

## How to Use This

1. Fork this repo.

2. Place your GPX files in the `gpx` folder following the naming convention:

    `[start]-to-[destination].gpx`
    
    Example: `s-queensferry-to-boness.gpx`

3. Run the map generator:

    ```bash
    python scripts/generate_map.py
    ```

    - New GPX files will automatically be added to `data/walks.yaml`.  
    - Journal Markdown files are automatically created in `docs/journals/`.  
    - The interactive map is generated and saved in `docs/map/index.html`.

    > ⚠️ If you delete a GPX file, you must manually remove the entry from `walks.yaml`.

4. Build the Sphinx documentation:

    ```bash
    cd docs
    make html
    ```

    - The homepage shows the embedded map.  
    - Sidebar displays all walks organised by region.  

5. Verify the output locally by opening:

    ```bash
    open _build/html/index.html  # or navigate in your file browser
    ```

## Output

- Interactive map: `docs/map/index.html`  
- Journals: `docs/journals/`  
- Distance data: `data/distance.json`  

[View Live Map](https://twotogether.github.io/uk-coast-walk-tracker/docs/map/index.html)
