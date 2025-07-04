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
