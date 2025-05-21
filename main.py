import math

room_width = 10
room_length = 8

walls = [
    ((0, 0), (room_width, 0)), # Bottom wall
    ((room_width, 0), (room_width, room_length)), # Right wall
    ((room_width, room_length), (0, room_length)), # Top wall
    ((0, room_length), (0, 0)), # Left wall
]

sound_source = (room_width / 5, room_length / 21) # Centre of the room just for an easy starting point

def generate_rays(source, angle_step=20):
    rays = []
    for angle in range(0, 360, angle_step):
        rad = math.radians(angle)
        dx = math.cos(rad)
        dy = math.sin(rad)
        rays.append({
            'origin': source,
            'direction': (dx, dy),
            'path': [source]
        })
    return rays

def get_ray_wall_intersection(ray_origin, ray_dir, wall_start, wall_end):
    ray_dx, ray_dy = ray_dir
    wall_dx = wall_end[0] - wall_start[0]
    wall_dy = wall_end[1] - wall_start[1]

    denom = ray_dx * wall_dy - ray_dy * wall_dx
    if denom == 0:
        return None

    t = ((wall_start[0] - ray_origin[0]) * wall_dy - (wall_start[1] - ray_origin[1]) * wall_dx) / denom
    u = ((wall_start[0] - ray_origin[0]) * ray_dy - (wall_start[1] - ray_origin[1]) * ray_dx) / denom

    if t >= 0 and 0 <= u <= 1:
        intersection_x = ray_origin[0] + t * ray_dx
        intersection_y = ray_origin[1] + t * ray_dy
        return (intersection_x, intersection_y, t)
    
    return None

rays = generate_rays(sound_source, angle_step=20)

for ray in rays:
    origin = ray['origin']
    direction = ray['direction']
    closest_hit = None
    closest_distance = float('inf')
    for wall in walls:
        result = get_ray_wall_intersection(origin, direction, wall[0], wall[1])
        if result:
            x, y, t = result
            if t < closest_distance:
                closest_distance = t
                closest_hit = (x, y)

    if closest_hit:
        ray['path'].append(closest_hit)
