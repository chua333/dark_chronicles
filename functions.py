import json

from classes import NPC, Location

model = "gpt-4"


def npc_finder(client, choose_npc_phrase):
    system_prompt = "you are to find the name from the phrase and only return the name, do not add any other text, if there is multiple, return the name followed by a comma"
    choose_npc_phrase = [{"role": "user", "content": f"find the name from the phrase: {choose_npc_phrase}"}]
    messages = [{"role": "system", "content": system_prompt}] + choose_npc_phrase

    response = client.chat.completions.create(
        model=model,
        messages = messages
    )
    reply = response.choices[0].message.content

    return reply


def interpret_player_intent(client, player_input, current_location, player, people_count_flag):
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
        model=model,
        messages = messages
    )
    reply = response.choices[0].message.content

    if reply == "1":
        if people_count_flag == 0:
            print("😶 Are you dumb? There is nobody here, go somewhere else stupid.\n")
            return  # Don't exit, let player try another action

        choice = input("Who do you want to talk to? Enter number (or type 'back'): ")
        if choice.lower() == "back":
            print("Returning to main options...\n")
            return

        try:
            npc_index = int(choice) - 1
            npc = current_location.get_available_npcs()[npc_index]
        except (IndexError, ValueError):
            print("Invalid choice. Returning...\n")
            return

        chat_history = []
        while True:
            player_input = input("You: ")
            if player_input.lower() in ["exit", "quit"]:
                print("Exiting the program.")
                break

            reply, chat_history = talk_to_npc(client, npc, player, player_input, chat_history)
            print(f"{npc.npc_id}: {reply}")
        

def npc_intended(client, choose_npc_phrase):
    system_prompt = """"
    you are to find who the named characters in the phrase,
    you can return the name and title if there is one, do not add any other text if there's not needed,
    if there is multiple, return the name followed by a comma
    """
    choose_npc_phrase = [{"role": "user", "content": f"find the name from the phrase: {choose_npc_phrase}"}]
    messages = [{"role": "system", "content": system_prompt}] + choose_npc_phrase

    response = client.chat.completions.create(
        model=model,
        messages = messages
    )
    reply = response.choices[0].message.content

    return reply


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
        model=model,
        messages=messages
    )

    reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": reply})

    return reply, chat_history

