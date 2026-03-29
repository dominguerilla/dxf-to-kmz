def add_insert(folder, entity):
    pos = entity.dxf.insert
    block_name = entity.dxf.name
    folder.newpoint(
        name=block_name,
        description=f"Symbol: {block_name} | Layer: {entity.dxf.layer}",
        coords=[(pos.x, pos.y)],
    )
