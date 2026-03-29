# Agent Instructions — DXF to KMZ Converter

## Project Overview
A web application that converts DXF files (WGS84 coordinates) to KMZ files.
Users upload one or more `.dxf` files via a browser UI and receive `.kmz` files (or a `.zip` of multiple KMZ files) as a download.

## Stack
- **Backend**: Python, FastAPI, uvicorn
- **DXF parsing**: `ezdxf`
- **KML/KMZ output**: `simplekml`
- **Frontend**: Plain HTML/CSS/JS (`frontend/index.html`) — no build step

## Installation

```bash
pip install -r requirements.txt
```

A virtual environment is recommended:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Server

Run from the project root:

```bash
cd backend
uvicorn main:app --reload
```

The app is served at `http://localhost:8000`.

## Project Structure

```
backend/
  main.py           # FastAPI app — serves UI, handles /convert POST endpoint
  converter.py      # Orchestrates DXF → KMZ: reads file, groups by layer, dispatches entities
  entities/
    line.py         # LINE → KML LineString
    lwpolyline.py   # LWPOLYLINE → KML LineString or Polygon (closed)
    arc.py          # ARC → KML LineString (36-point approximation)
    text.py         # TEXT / MTEXT → KML Point with text as label
    point.py        # POINT → KML Point (node)
    insert.py       # INSERT (block reference) → KML Point with block name
frontend/
  index.html        # Single-page upload UI
requirements.txt
```

## Adding a New Entity Type

1. Create `backend/entities/<type>.py` with an `add_<type>(folder, entity)` function.
   - `folder` is a `simplekml` folder object (call `folder.newpoint(...)`, `folder.newlinestring(...)`, etc.)
   - `entity` is an `ezdxf` entity object (use `entity.dxf.*` for attributes)
2. Register the handler in `backend/converter.py`:
   ```python
   from entities.<type> import add_<type>
   HANDLERS["TYPENAME"] = add_<type>
   ```
   The entity type string must match the DXF type name returned by `entity.dxftype()`.

## Coordinate System
DXF files are expected to be in **WGS84** (EPSG:4326) with X = longitude and Y = latitude.
No reprojection is performed. If a file uses a projected CRS, coordinates will be wrong.

## Dependencies
All dependencies are in `requirements.txt`. To add a new dependency:
1. Install it: `pip install <package>`
2. Add it to `requirements.txt` (pinning a version is optional but recommended for production)

## Key Behaviours
- Entities are grouped into KML **folders by DXF layer name**.
- Malformed individual entities are silently skipped — they do not abort conversion.
- Non-`.dxf` files submitted to `/convert` return HTTP 422 with an error message shown in the UI.
- Single-file upload returns a `.kmz` directly; multi-file upload returns a `.zip` of KMZ files.
- Temporary files are written to `tempfile.mkdtemp()` and cleaned up automatically after the response is sent.
