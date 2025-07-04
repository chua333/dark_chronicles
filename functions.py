import json

from classes import NPC, Location


def npc_finder(client, choose_npc_phrase):
    system_prompt = "you are to find the name from the phrase and only return the name, do not add any other text, if there is multiple, return the name followed by a comma"
    choose_npc_phrase = [{"role": "user", "content": f"find the name from the phrase: {choose_npc_phrase}"}]
    messages = [{"role": "system", "content": system_prompt}] + choose_npc_phrase

    response = client.chat.completions.create(
        model='gpt-4',
        messages = messages
    )
    reply = response.choices[0].message.content

    return reply


def interpret_player_intent(client, player_input, current_location, player):
    system_prompt = """"
    you are to find the intent of the player that is most matching with the available actions below
    1. talk to npc
    2. move to location

    other actions are not allowed
    reply only numbers if actions matched, otherwise reply as you wish 
    """
    player_intent = [{"role": "user", "content": f"{player_input}"}]
    messages = [{"role": "system", "content": system_prompt}] + player_intent

    response = client.chat.completions.create(
        model='gpt-4',
        messages = messages
    )
    reply = response.choices[0].message.content

    if reply == "1":
        choice = input("Who do you want to talk to? Enter number: ")
        try:
            npc_index = int(choice) - 1
            npc = current_location.get_available_npcs()[npc_index]
        except (IndexError, ValueError):
            print("Invalid choice.")
            exit()

        chat_history = []
        while True:
            player_input = input("You: ")
            if player_input.lower() in ["exit", "quit"]:
                print("Exiting the program.")
                break

            reply, chat_history = talk_to_npc(client, npc, player, player_input, chat_history)
            print(f"{npc.npc_id}: {reply}")
        

def npc_intended(client, choose_npc_phrase):
    system_prompt = "you are to find the person the user wants to find and only return the name, do not add any other text, if there is multiple, return the name followed by a comma"
    choose_npc_phrase = [{"role": "user", "content": f"find the name from the phrase: {choose_npc_phrase}"}]
    messages = [{"role": "system", "content": system_prompt}] + choose_npc_phrase

    response = client.chat.completions.create(
        model='gpt-4',
        messages = messages
    )
    reply = response.choices[0].message.content

    return reply


def load_all_npcs(file_path="npc_memories.json"):
    with open(file_path, "r") as f:
        npc_list = json.load(f)

    npc_dict = {}
    for npc_data in npc_list:
        npc = NPC(npc_data)
        npc_dict[npc.npc_id.lower()] = npc

    return npc_dict


def talk_to_npc(client, npc: NPC, player: NPC, player_input, chat_history):
    npc_long_mem, npc_short_mem = npc.memory_summary()
    player_description = player.describe_as_seen_by_others()

    system_prompt = (
        f"{npc.summary()} "
        f"{npc.personality_desc()} "
        f"{npc_long_mem} "
        f"{npc_short_mem} "
        f"You are currently speaking to {player_description}. "
        f"Respond in character. Try to keep it short but natural."
    )

    chat_history.append({"role": "user", "content": player_input})
    messages = [{"role": "system", "content": system_prompt}] + chat_history

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )

    reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": reply})

    return reply, chat_history


def load_all_locations(file_path="locations.json"):
    import json

    with open(file_path, "r") as f:
        data = json.load(f)

    locations = {}

    for city_block in data:
        city = city_block["City"]
        for loc in city_block["Locations"]:
            location = Location(
                name=loc["name"],
                city=city,
                adjacent=loc["adjacent"]
            )
            locations[location.full_name] = location

    # Link adjacents
    for location in locations.values():
        location.adjacent = [
            locations[f"{location.city}, {adj_name}"]
            for adj_name in location.adjacent_names
            if f"{location.city}, {adj_name}" in locations
        ]

    return locations


def assign_npcs_to_locations(all_npcs, all_locations):
    for npc in all_npcs.values():
        loc_name = npc.location  # e.g., "Evergreen, Inn"
        if loc_name in all_locations:
            all_locations[loc_name].add_npc(npc)
        else:
            print(f"⚠️ Warning: Location '{loc_name}' not found for NPC '{npc.npc_id}'")
