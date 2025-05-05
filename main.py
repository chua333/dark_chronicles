import json

from openai import OpenAI
from cred import open_ai_key


# initialize openai client first to save time
client = OpenAI(api_key=open_ai_key)


def npc_finder(choose_npc_phrase):
    system_prompt = "you are to find the name from the phrase and only return the name, do not add any other text, if there is multiple, return the name followed by a comma"
    choose_npc_phrase = [{"role": "user", "content": f"find the name from the phrase: {choose_npc_phrase}"}]
    messages = [{"role": "system", "content": system_prompt}] + choose_npc_phrase

    response = client.chat.completions.create(
        model='gpt-4',
        messages = messages
    )
    reply = response.choices[0].message.content

    return reply


def talk_to_npc(npc_summary, npc_personality, npc_long_mem, npc_short_mem, player_input, chat_history):
    system_prompt = f"{npc_summary}, {npc_personality}, {npc_long_mem}, {npc_short_mem}"

    chat_history.append({"role": "user", "content": player_input})

    messages = [{"role": "system", "content": system_prompt}] + chat_history

    response = client.chat.completions.create(
        model='gpt-4',
        messages = messages
    )

    reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": reply})

    return reply, chat_history


def load_npcs(file_path="npc_memories.json", npc_intended=None):
    with open(file_path, "r") as f:
        npc_list = json.load(f)

    for npc in npc_list:
        npc_name = npc["npc_id"]
        if npc_intended.lower() == npc_name:
            npc_summary = f"You are {npc['npc_id']}, a {npc['race']} {npc['role'] } in {npc['location']}"
            npc_personality = f"Your personality are {npc['personality']}"

            npc_long_mem = "You clearly remembered "
            for mem in npc.get("long_term_memory", []):
                npc_long_mem += mem["text"] + ", "

            npc_short_mem = "You briefly remember "
            for mem in npc.get("short_term_memory", []):
                npc_short_mem += mem["text"] + ", "

            npc_long_mem = npc_long_mem.strip(", ")
            npc_short_mem = npc_short_mem.strip(", ")

            return npc_name, npc_summary, npc_personality, npc_long_mem, npc_short_mem
        else:
            print(f"NPC {npc_name} not found.")


if __name__ == "__main__":
    choose_npc_phrase = input("who do you want to talk to?")
    npc_intended = npc_finder(choose_npc_phrase)
    print(f"{npc_intended}")
    # while True:
    #     player_input = input("You: ")
    #     if player_input.lower() == "exit" | player_input.lower() == "quit":
    #         print("Exiting the program.")
    #         break

    #     chat_history = []

    #     npc_name, npc_summary, npc_personality, npc_long_mem, npc_short_mem = load_npcs(npc_intended=npc_intended)
    #     reply, chat_history = talk_to_npc(npc_summary, npc_personality, npc_long_mem, npc_short_mem, player_input, chat_history)
    #     print(f"{npc_name}: {reply}")
