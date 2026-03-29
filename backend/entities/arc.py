import math


def add_arc(folder, entity, num_points=36):
    cx = entity.dxf.center.x
    cy = entity.dxf.center.y
    radius = entity.dxf.radius
    start_angle = entity.dxf.start_angle
    end_angle = entity.dxf.end_angle

    if end_angle < start_angle:
        end_angle += 360.0

    coords = []
    for i in range(num_points + 1):
        angle = math.radians(start_angle + (end_angle - start_angle) * i / num_points)
        coords.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))

    folder.newlinestring(name="Arc", coords=coords)
