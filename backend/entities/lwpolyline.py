def add_lwpolyline(folder, entity):
    coords = [(p[0], p[1]) for p in entity.get_points()]
    if len(coords) < 2:
        return

    if entity.is_closed:
        if coords[0] != coords[-1]:
            coords.append(coords[0])
        folder.newpolygon(
            name="Polygon",
            outerboundaryis=coords,
        )
    else:
        folder.newlinestring(
            name="Polyline",
            coords=coords,
        )
