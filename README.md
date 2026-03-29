# DXF to KMZ Converter

A web application that converts Drawing Exchange Format (`.dxf`) files into Keyhole Markup Language (`.kml`/`.kmz`) files. Upload one or more DXF files through the browser and download the converted KMZ files.

## Requirements

- Python 3.9+
- pip

## Installation

```bash
# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

```bash
cd backend
uvicorn main:app --reload
```

Open `http://localhost:8000` in your browser.

## Usage

1. Drag and drop one or more `.dxf` files onto the upload area, or click to browse.
2. Click **Convert to KMZ**.
3. The browser will automatically download the result:
   - Single file → `.kmz`
   - Multiple files → `.zip` containing one `.kmz` per input file

## Architecture

```
dxf-to-kmz/
├── backend/
│   ├── main.py              # FastAPI app — serves the UI and handles /convert requests
│   ├── converter.py         # Core pipeline: reads DXF, groups entities by layer, writes KMZ
│   └── entities/
│       ├── line.py          # LINE        → KML LineString
│       ├── lwpolyline.py    # LWPOLYLINE  → KML LineString or Polygon (if closed)
│       ├── arc.py           # ARC         → KML LineString (36-point approximation)
│       ├── text.py          # TEXT/MTEXT  → KML Point with text as label
│       ├── point.py         # POINT       → KML Point (node marker)
│       └── insert.py        # INSERT      → KML Point with block name (symbol)
├── frontend/
│   └── index.html           # Single-page upload UI — no build step required
├── requirements.txt
├── AGENTS.md
└── README.md
```

### Conversion Pipeline

1. DXF file is written to a temporary directory.
2. `ezdxf` parses the file and iterates over modelspace entities.
3. Entities are grouped into KML folders by their DXF layer name.
4. Each supported entity type is dispatched to its handler, which appends the appropriate KML geometry.
5. `simplekml` saves the result as a `.kmz` (zipped KML).
6. The file is returned to the browser and the temp directory is cleaned up.

### Coordinate System

DXF files must be in **WGS84** (EPSG:4326) with X = longitude and Y = latitude. No reprojection is performed.

### Supported Entity Types

| DXF Type | KML Output |
|---|---|
| `LINE` | LineString |
| `LWPOLYLINE` | LineString, or Polygon if closed |
| `ARC` | LineString (approximated) |
| `TEXT` / `MTEXT` | Point with text label |
| `POINT` | Point (node marker) |
| `INSERT` | Point with block name as label |

Unsupported entity types are silently skipped.

## Adding a New Entity Type

1. Create `backend/entities/<type>.py`:

   ```python
   def add_<type>(folder, entity):
       # folder: simplekml folder — call folder.newpoint(), folder.newlinestring(), etc.
       # entity: ezdxf entity — access attributes via entity.dxf.*
       pass
   ```

2. Register it in `backend/converter.py`:

   ```python
   from entities.<type> import add_<type>
   HANDLERS["DXFTYPENAME"] = add_<type>
   ```

   The key must match the string returned by `entity.dxftype()`.

## Dependencies

| Package | Purpose |
|---|---|
| `ezdxf` | DXF file parsing |
| `simplekml` | KML/KMZ file generation |
| `fastapi` | Web framework |
| `uvicorn` | ASGI server |
| `python-multipart` | Multipart file upload support |
