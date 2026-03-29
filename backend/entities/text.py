def add_text(folder, entity):
    pos = entity.dxf.insert
    if entity.dxftype() == "MTEXT":
        label = entity.text
    else:
        label = entity.dxf.text

    folder.newpoint(name=label or "", coords=[(pos.x, pos.y)])
