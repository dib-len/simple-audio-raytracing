import math

room_width = 10
room_length = 10

walls = [
    ((0, 0), (room_width, 0)), # Bottom wall
    ((room_width, 0), (room_width, room_length)), # Right wall
    ((room_width, room_length), (0, room_length)), # Top wall
    ((0, room_length), (0, 0)), # Left wall
]

sound_source = (room_width / 2, room_length / 2) # Centre of the room just for an easy starting point

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

