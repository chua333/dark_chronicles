import keyboard
import time

def real_time_movement_loop():
    player_coords = [7, 4]  # Starting coords

    print("Use WASD to move. Press Q to quit.\n")

    while True:
        if keyboard.is_pressed("q"):
            break
        elif keyboard.is_pressed("w"):
            player_coords[1] -= 1
        elif keyboard.is_pressed("s"):
            player_coords[1] += 1
        elif keyboard.is_pressed("a"):
            player_coords[0] -= 1
        elif keyboard.is_pressed("d"):
            player_coords[0] += 1

        # Clear screen and redraw
        print("\033[H\033[J", end="")  # ANSI clear screen (works in most terminals)
        print(f"Player at: {player_coords}")
        time.sleep(0.15)  # Prevent key spamming from flooding the output


real_time_movement_loop()
