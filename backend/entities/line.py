def add_line(folder, entity):
    start = entity.dxf.start
    end = entity.dxf.end
    folder.newlinestring(
        name=f"Line",
        coords=[(start.x, start.y), (end.x, end.y)],
    )
