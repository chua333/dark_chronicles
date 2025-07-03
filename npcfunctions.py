import json

from characters import NPC


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


def load_npcs(file_path="npc_memories.json", npc_intended=None):
    with open(file_path, "r") as f:
        npc_list = json.load(f)

    for npc_data in npc_list:
        if npc_data["npc_id"].lower() == npc_intended.lower():
            npc = NPC(npc_data)
            long_mem, short_mem = npc.memory_summary()
            return {
                "name": npc.npc_id,
                "summary": npc.summary(),
                "personality": npc.personality_desc(),
                "long_term_memory": long_mem,
                "short_term_memory": short_mem,
            }

    raise ValueError(f"NPC '{npc_intended}' not found in file.")


def talk_to_npc(client, npc_data, player_input, chat_history):
    system_prompt = (
        f"{npc_data['summary']}, "
        f"{npc_data['personality']}, "
        f"{npc_data['long_term_memory']}, "
        f"{npc_data['short_term_memory']}, "
        f"Keep responses short (under 20 words) unless the player asks for more details."
    )

    chat_history.append({"role": "user", "content": player_input})
    messages = [{"role": "system", "content": system_prompt}] + chat_history

    response = client.chat.completions.create(
        model='gpt-4',
        messages=messages
    )

    reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": reply})

    return reply, chat_history
