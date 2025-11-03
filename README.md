# UK Coastal Walk Tracker

A Python project to track and visualise coastal walks around the UK.  
This tool allows you to log GPX walks, generate an interactive map of the coastline you’ve walked, calculate distances, and see your progress as a fraction of the total UK coastline.

## Features

- Automatically detects new GPX files and updates `walks.yml`.  
- Generates interactive **Folium maps** showing walked sections.  
- Calculates total distance walked and fraction of UK coastline completed.  
- Supports journaling for each walk in Markdown (`journals/`).  
- Highlights newly added walks on the map for easy identification.

## How to use this

### Add your GPX Files and Generate the Map

1. Place your GPX files in the `gpx` folder following the naming convention:

    `[start]-to-[destination].gpx`
    
    Example: s-queensferry-to-boness.gpx

2. Run the map generator

    `python scripts/generate_map.py`

     New GPX files will automatically be added to `walks.yml`.

The map will be saved in the map/ folder.

[View Map](map/index.html)
