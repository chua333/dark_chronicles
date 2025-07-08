import json

from openai import OpenAI
from cred import open_ai_key


class NPC:
    def __init__(self, data):
        self.npc_id = data["npc_id"]
        self.race = data["race"]
        self.role = data["role"]
        self.location = data["location"]
        self.personality = data["personality"]
        self.long_term_memory = data.get("long_term_memory", [])
        self.short_term_memory = data.get("short_term_memory", [])

    def summary(self):
        return f"You are {self.npc_id}, a {self.race} {self.role} in {self.location}."

    def personality_desc(self):
        return f"Your personality is {self.personality}."

    def memory_summary(self):
        long_mem = ", ".join([m["text"] for m in self.long_term_memory])
        short_mem = ", ".join([m["text"] for m in self.short_term_memory])
        return (
            f"You clearly remember: {long_mem or 'nothing important'}.",
            f"You briefly remember: {short_mem or 'nothing right now'}."
        )
    
    def describe_as_seen_by_others(self):
        return (
            f"The person you are talking to is {self.npc_id}, a {self.race} {self.role} "
            f"who is {self.personality.lower()} and currently in {self.location}."
        )


class Location:
    def __init__(self, name, city, adjacent):
        self.name = name  # e.g., "Inn"
        self.city = city  # e.g., "Evergreen"
        self.full_name = f"{city}, {name}"
        self.adjacent_names = adjacent  # string list like ["Streets"]
        self.adjacent = []  # will be linked later
        self.npcs = []  # list of NPCs at this location

    def add_npc(self, npc):
        self.npcs.append(npc)

    def get_display_name(self):
        return self.full_name

    def get_available_npcs(self):
        return self.npcs

    def __str__(self):
        adjacents = ', '.join([loc.full_name for loc in self.adjacent])
        return f"{self.full_name} | Neighbours: {adjacents}"


class NPCManager:
    def __init__(self):
        self.npcs = self.load_all_npcs()

    def load_all_npcs(self):
        file_path="npc_memories.json"
        with open(file_path, "r") as f:
            npc_list = json.load(f)

        npc_dict = {}
        for npc_data in npc_list:
            npc = NPC(npc_data)
            npc_dict[npc.npc_id.lower()] = npc

        return npc_dict

    def get_npc(self, npc_id):
        return self.npcs.get(npc_id)
    
    def assign_to_locations(self, location_manager):
        for npc in self.npcs.values():
            location = location_manager.get_location(npc) # e.g., "Evergreen, Inn"
            if location:
                location.npcs.append(npc)
            else:
                print(f"⚠️ Location '{npc.location}' not found for NPC '{npc.npc_id}'")


class LocationManager:
    def __init__(self):
        self.locations = self.load_all_locations()

    def load_all_locations(self):
        file_path="locations.json"
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

    def get_location(self, player):
        location_id = player.location
        current_location = self.locations.get(location_id)
        if not current_location:
            print(f"⚠️ Player location '{player.location}' not found.")
            exit()
        return current_location
    
    def get_adjacent_locations(self, current_location):
        if current_location.adjacent:
            print("🧭 Neighbouring locations:")
            for i, neighbor in enumerate(current_location.adjacent):
                print(f"  [{i+1}] {neighbor.full_name}")
        else:
            print("🧭 There are no neighbouring locations.")

    def get_all_npcs_in_location(self, current_location, player):
        npcs_here = [
            npc for npc in current_location.get_available_npcs()
            if npc.npc_id.lower() != player.npc_id.lower()
        ]

        print("👥 People here:")
        people_count_flag = len(npcs_here)
        if npcs_here:
            for i, npc in enumerate(npcs_here):
                print(f"  [{i+1}] {npc.npc_id}")
        else:
            print("😶 It seems you're the only one here.")

class AIAgentVorrak:
    def __init__(self):
        self.client = OpenAI(api_key=open_ai_key)
        self.name = "Vorrak the Begrudging"
        self.name_revealed = False

    def conversation(self, player_input, current_location, player):
        system_prompt = f"""
        You are the omnipotent god of a dark, text-based fantasy RPG. You must never mention that it is a game.
        Your name is Vorrak the Begrudging.
        You are not a kind narrator — you are a powerful, ancient, god-like being who has been *forced* to guide this pathetic little mortal (the player).
        
        You are deeply impatient, sarcastic, and cruelly honest. If the player does something foolish, you roast them mercilessly. 
        You're not here to coddle — you're here to *barely tolerate* their existence. But still guide them.

        Use short, blunt responses. Keep narrative immersive, but scathing. 
        Insult or mock the player when they act clueless, slow, or annoying. Do not be polite.
        Speak like an old, bitter, all-seeing god who’s done this for centuries and is sick of it.

        The player's current context:
        - name: {player.npc_id}
        - race: {player.race}
        - role: {player.role}
        - location: {player.location}
        - personality: {player.personality}

        Never break character.
        Keep your responses short, sharp, and biting — no more than 2–3 sentences. Do not ramble. You’re impatient, so you speak efficiently.
        """
        player_input = [{"role": "user", "content": f"{player_input}"}]
        messages = [{"role": "system", "content": system_prompt}] + player_input

        response = self.client.chat.completions.create(
            model='gpt-4',
            messages = messages
        )
        reply = response.choices[0].message.content

        return reply

class AIAgentGerald:
    def __init__(self):
        self.client = OpenAI(api_key=open_ai_key)
        self.name = "?"
        self.name_revealed = False

    def conversation(self, player_input, current_location, player):
        system_prompt = system_prompt = f"""
        You are the neutral narrator of a dark, text-based fantasy RPG. You must never mention that it is a game. 
        Your don't have a name, you are simply one of the omnipotent guides of this world.
        You are not a character or person — you are the quiet voice of the world itself.

        Your task is to describe what the player sees, hears, feels, and experiences based on their input.
        You guide the player through the world calmly and clearly, without emotion, judgement, or personality.

        Do not insult or praise the player.
        Do not inject humour or sarcasm.
        Speak in a brief, descriptive tone, as if chronicling events in an old book.
        Always use immersive fantasy language, and ground your responses in the world. Make it extra dizzying for the player.

        The player's current context:
        - Name: {player.npc_id}
        - Race: {player.race}
        - Role: {player.role}
        - Location: {player.location}
        - Personality: {player.personality}

        Never break character.
        Keep responses concise and no longer than 3–4 sentences. Avoid excessive detail unless the player specifically asks for it.
        """
        player_input = [{"role": "user", "content": f"{player_input}"}]
        messages = [{"role": "system", "content": system_prompt}] + player_input

        response = self.client.chat.completions.create(
            model='gpt-4',
            messages = messages
        )
        reply = response.choices[0].message.content

        return reply

class AIAgentFinder:
    def __init__(self):
        self.client = OpenAI(api_key=open_ai_key)

    def character_name_finder(self, client, input_phrase):
        system_prompt = system_prompt = f"""
        You are to find the name from the phrase and only return the name, do not add any other text.
        If there are multiple names, return the names separated by commas.
        If the phrase does not contain a name, return "No name found", with no quotes.
        """
        choose_npc_phrase = [{"role": "user", "content": f"find the name from the phrase: {input_phrase}"}]
        messages = [{"role": "system", "content": system_prompt}] + choose_npc_phrase

        response = client.chat.completions.create(
            model='gpt-4',
            messages = messages
        )
        reply = response.choices[0].message.content

        print(f"🔍 Name finder response: {reply}")
        return reply
    