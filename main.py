import math
import matplotlib.pyplot as plt

room_width = 10
room_length = 8

walls = [
    ((0, 0), (room_width, 0), 0.2), # Bottom wall - low absorption
    ((room_width, 0), (room_width, room_length), 0.5), # Right wall - medium absorption
    ((room_width, room_length), (0, room_length), 0.8), # Top wall - high apsorption
    ((0, room_length), (0, 0), 1.0), # Left wall - fully aborbs
]

source = (room_width / 2, room_length / 2) # Centre of the room just for an easy starting point

def generate_rays(source, angle_step):
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

def reflect_ray(incoming, normal):
    dot_product = incoming[0] * normal[0] + incoming[1] * normal[1]
    reflected = (incoming[0] - 2 * dot_product * normal[0], incoming[1] - 2 * dot_product * normal[1])
    return reflected

def get_wall_normal(wall_start, wall_end):
    wall_dx = wall_end[0] - wall_start[0]
    wall_dy = wall_end[1] - wall_start[1]
    normal = (-wall_dy, wall_dx)
    length = math.hypot(*normal)
    return (normal[0] / length, normal[1] / length)

rays = generate_rays(source, 10)

for ray in rays:
    origin = ray['origin']
    direction = ray['direction']
    energy = 1.0

    while energy > 0.1:
        closest_hit = None
        closest_distance = float('inf')
        closest_wall = None
        wall_absorption = 0.0

        for wall in walls:
            result = get_ray_wall_intersection(origin, direction, wall[0], wall[1])
            if result:
                x, y, t = result
                if t < closest_distance:
                    closest_distance = t
                    closest_hit = (x, y)
                    closest_wall = wall
                    wall_absorption = wall[2]

        if not closest_hit:
            break

        ray['path'].append(closest_hit)
        energy *= (1 - wall_absorption)
        normal = get_wall_normal(closest_wall[0], closest_wall[1])
        direction = reflect_ray(direction, normal)
        epsilon = 1e-6
        origin = (closest_hit[0] + direction[0] * epsilon, closest_hit[1] + direction[1] * epsilon)

        if energy < 0.1:
            ray['death_point'] = origin

fig, ax = plt.subplots()
for wall in walls:
    (x1, y1), (x2, y2), absorption = wall
    wall_thickness = 1 + absorption * 3
    ax.plot([x1, x2], [y1, y2], 'k-', linewidth=wall_thickness)

for ray in rays:
    energy = 1.0
    for i in range(len(ray['path']) - 1):
        x0, y0 = ray['path'][i]
        x1, y1 = ray['path'][i + 1]
        ax.plot([x0, x1], [y0, y1], 'r--', alpha=energy, linewidth=energy * 2)
        energy *= (1 - 0.35)
    if 'death_point' in ray:
        x, y = ray['death_point']
        ax.plot(x, y, 'rx', markersize=10, alpha=1)

ax.plot(source[0], source[1], 'bo', label='Source')

ax.set_aspect('equal')
ax.set_xlim(-1, room_width + 1)
ax.set_ylim(-1, room_length + 1)
plt.title('Audio Ray Tracing in a Room')
plt.legend()
plt.grid(True)
plt.show()