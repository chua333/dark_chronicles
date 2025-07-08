import json
import functions

from classes import NPCManager, LocationManager, AIAgentGerald, AIAgentVorrak, AIAgentFinder


if __name__ == "__main__":
    # loading NPCs and locations
    print("🔄 Loading NPCs and locations...")
    npc_manager = NPCManager()
    location_manager = LocationManager()
    npc_manager.assign_to_locations(location_manager)

    # Set the player to a specific NPC
    print("👤 Setting player to 'chua' NPC...")
    player = npc_manager.get_npc("chua")

    # loading player location
    print("🔄 Loading player location...")
    current_location = location_manager.get_location(player)
    print(f"\n📍 You are at {current_location.full_name}")

    # Show neighbouring locations
    print("Loading map...")
    location_manager.get_adjacent_locations(current_location)

    # Show people at current location (excluding player)
    location_manager.get_all_npcs_in_location(current_location, player)

    # game start
    ai_npc = AIAgentVorrak()
    ai_name_finder = AIAgentFinder()
    print("\n🎮 Game started! Type 'exit' to quit.")
    while True:
        player_input = input("You: ")
        if player_input.lower() in ["exit", "quit"]:
            print("Exiting the program.")
            exit()

        reply = ai_npc.conversation(player_input, current_location, player)
        ai_display_name = ai_npc.name if ai_npc.name_revealed else "?"
        print(f"{ai_display_name}: {reply}")
        ai_npc.check_name_in_reply(reply, ai_name_finder)
            