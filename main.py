import json
import functions

from openai import OpenAI
from cred import open_ai_key


# initialize openai client first to save time
client = OpenAI(api_key=open_ai_key)


if __name__ == "__main__":
    all_npcs = functions.load_all_npcs()
    all_locations = functions.load_all_locations()
    functions.assign_npcs_to_locations(all_npcs, all_locations)

    player = all_npcs["chua"]
    current_location = all_locations.get(player.location)

    if not current_location:
        print(f"⚠️ Player location '{player.location}' not found.")
        exit()

    print(f"\n📍 You are at {current_location.full_name}")

    # Show neighbouring locations
    if current_location.adjacent:
        print("🧭 Neighbouring locations:")
        for i, neighbor in enumerate(current_location.adjacent):
            print(f"  [{i+1}] {neighbor.full_name}")
    else:
        print("🧭 There are no neighbouring locations.")

    # Show people at current location (excluding player)
    npcs_here = [
        npc for npc in current_location.get_available_npcs()
        if npc.npc_id.lower() != player.npc_id.lower()
    ]

    print("👥 People here:")
    if npcs_here:
        for i, npc in enumerate(npcs_here):
            print(f"  [{i+1}] {npc.npc_id}")
    else:
        print("😶 It seems you're the only one here.")

    player_input = input("What do you want to do? (type 'exit' to quit): ")
    if player_input.lower() in ["exit", "quit"]:
        print("Exiting the program.")
        exit()

    functions.interpret_player_intent(client, player_input, current_location, player)
