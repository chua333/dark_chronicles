import json
import npcfunctions

from openai import OpenAI
from cred import open_ai_key


# initialize openai client first to save time
client = OpenAI(api_key=open_ai_key)


if __name__ == "__main__":
    choose_npc_phrase = input("who do you want to talk to?")
    npc_intended = npcfunctions.npc_intended(client, choose_npc_phrase)
    print(f"{npc_intended}")
    while True:
        player_input = input("You: ")
        if player_input.lower() in ["exit", "quit"]:
            print("Exiting the program.")
            break

        chat_history = []

        npc_data = npcfunctions.load_npcs(npc_intended=npc_intended)
        reply, chat_history = npcfunctions.talk_to_npc(client, npc_data, player_input, chat_history)
        print(f"{npc_data['name']}: {reply}")
