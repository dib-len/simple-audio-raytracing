room_width = 10
room_length = 10

walls = [
    ((0, 0), (room_width, 0)), # Bottom wall
    ((room_width, 0), (room_width, room_length)), # Right wall
    ((room_width, room_length), (0, room_length)), # Top wall
    ((0, room_length), (0, 0)), # Left wall
]