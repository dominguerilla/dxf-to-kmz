import ezdxf
import simplekml

from entities.line import add_line
from entities.lwpolyline import add_lwpolyline
from entities.arc import add_arc
from entities.text import add_text
from entities.point import add_point
from entities.insert import add_insert

HANDLERS = {
    "LINE": add_line,
    "LWPOLYLINE": add_lwpolyline,
    "ARC": add_arc,
    "TEXT": add_text,
    "MTEXT": add_text,
    "POINT": add_point,
    "INSERT": add_insert,
}


def convert_dxf_to_kmz(dxf_path: str, kmz_path: str) -> None:
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()

    kml = simplekml.Kml()
    folders: dict = {}

    for entity in msp:
        entity_type = entity.dxftype()
        handler = HANDLERS.get(entity_type)
        if handler is None:
            continue

        layer = entity.dxf.layer or "Default"
        if layer not in folders:
            folders[layer] = kml.newfolder(name=layer)

        try:
            handler(folders[layer], entity)
        except Exception:
            # Skip malformed entities without aborting the whole file
            continue

    kml.savekmz(kmz_path)
