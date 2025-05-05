import json

def load_world(file_path="locations.json", world_name="Evergreen"):
    with open(file_path, "r") as f:
        worlds = json.load(f)
    for world in worlds:
        if world["world"] == world_name:
            return world
    raise ValueError(f"World '{world_name}' not found.")

def draw_map(world_data, player_location=None, map_size=(15, 15)):
    grid = [["." for _ in range(map_size[0])] for _ in range(map_size[1])]
    locs = world_data["locations"]

    for name, data in locs.items():
        x, y = data["coordinates"]
        if 0 <= x < map_size[0] and 0 <= y < map_size[1]:
            if name == player_location:
                grid[y][x] = "P"  # Mark player location
            else:
                grid[y][x] = "X"  # Generic marker for location

    # Print the grid (row by row)
    print("\n--- World Map ---")
    for row in grid:
        print(" ".join(row))
    print("Legend: X=Location, P=Player, .=Empty\n")

world_data = load_world("locations.json", "Evergreen")

# Get initial player coordinates from location
def get_coords_by_name(world_data, name):
    return world_data["locations"][name]["coordinates"]

def get_location_by_coords(world_data, coords):
    for name, data in world_data["locations"].items():
        if data["coordinates"] == coords:
            return name
    return None  # Not a defined location

def move_player(current_coords, direction, map_size=(15, 15)):
    x, y = current_coords
    if direction == "w" and y > 0:
        y -= 1
    elif direction == "s" and y < map_size[1] - 1:
        y += 1
    elif direction == "a" and x > 0:
        x -= 1
    elif direction == "d" and x < map_size[0] - 1:
        x += 1
    return [x, y]

# Main movement loop
player_coords = get_coords_by_name(world_data, "Marketplace")

while True:
    player_location = get_location_by_coords(world_data, player_coords)
    draw_map(world_data, player_location)
    
    print(f"You are at: {player_location or 'an unknown area'} (coords: {player_coords})")
    command = input("Move (W/A/S/D), or Q to quit: ").lower()
    
    if command == "q":
        break
    elif command in ["w", "a", "s", "d"]:
        new_coords = move_player(player_coords, command)
        player_coords = new_coords
    else:
        print("Invalid command.")
