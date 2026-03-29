def add_point(folder, entity):
    loc = entity.dxf.location
    folder.newpoint(name="Node", coords=[(loc.x, loc.y)])
